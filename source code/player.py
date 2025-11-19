from pico2d import *
from sdl2 import *
from state_machine import StateMachine
from player_skill import PlayerSkill
import global_data as GD
import game_framework, game_world
resource_address = 'C:\\Users\\moonc\\OneDrive\\문서\\GitHub\\2DGP-MaM\\resource\\player\\'

time_out = lambda e: e[0] == 'TIMEOUT'
def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
def d_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d
def d_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d
def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a
def a_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a
def s_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s
def shift_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LSHIFT and GD.ability_monster1 == True
def e_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_e
def q_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_q
def r_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_r
def Mleft_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONDOWN and e[1].button == SDL_BUTTON_LEFT
def interaction_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_f # and 플레이어가 상호작용 오브젝트와 닿은 상태
def interaction_up(e):
    return # 상호작용이 끝나면 자동으로 종료
def pause_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_ESCAPE # and 일시정지 상태가 이닌 경우
def pause_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_ESCAPE # and 일시정지 상태인 경우
def get_floor_y(player):
    max_floor_y = 0
    for staging in game_world.collision_pairs['player:staging'][1]:
        if on_staging(player, staging) == True and staging.y + staging.height // 2 > max_floor_y:
            max_floor_y = staging.y + staging.height // 2
    return max_floor_y
def get_another_floor(player):
    another_floor = False
    for staging in game_world.collision_pairs['player:staging'][1]:
        if on_staging(player, staging) == True and game_world.collide_rect_to_rect(player, staging) == False:
            another_floor = True
    return another_floor
def on_staging(player, staging):
    px1, py1, px2, py2 = player.get_bb()
    sx1, sy1, sx2, sy2 = staging.get_bb()
    if px2 > sx1 and px1 < sx2 and py1 >= sy2:
        return True
    else:
        return False

COOLTIME_ATTACK = 0.5
COOLTIME_DEFENSE = 1.0
COOLTIME_SKILL1 = 1.0
COOLTIME_SKILL2 = 2.0
JUMP_HEIGHT = 300.0  # 최대 점프 높이 (pixel)
MAX_HP = 100
MAX_MP = 100

GRAVITY = 9.8  # 중력 가속도 (m/s²)
# player move speed
PIXEL_PER_METER = (10.0 / 2.0) # 10 pixel == 1 meter
RUN_SPEED_KMPH = 60.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
# player action_idle speed
TIME_PER_ACTION_idle = 1.0 # 한 번 쉬는데 걸리는 시간 1.0초
ACTION_PER_TIME_idle = 1.0 / TIME_PER_ACTION_idle
FRAMES_PER_ACTION_idle = 2 # 한 번 쉬는데 필요한 프레임 2장
# player action_run speed
TIME_PER_ACTION_run = 0.5 # 한 걸음 걷는데 걸리는 시간 0.5초
ACTION_PER_TIME_run = 1.0 / TIME_PER_ACTION_run
FRAMES_PER_ACTION_run = 6 # 한 걸음 걷는데 필요한 프레임 6장

class Player:
    images = None
    def load_image(self):
        if Player.images == None:
            Player.images = {}
            Player.images['Idle'] = [load_image(resource_address + "Idle" + " (%d)" % i + ".png") for i in range(1, 3)]
            Player.images['Run'] = [load_image(resource_address + "Run" + " (%d)" % i + ".png") for i in range(1, 7)]
    def __init__(self):
        self.player = self
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.x, self.y = 768, 960
        self.floor_y = get_floor_y(self)
        self.y = self.floor_y + 75
        self.tiptoe = self.get_bb()[1]
        self.jumping_up = False
        self.jumping_down = False
        self.cur_jump_height = 0
        self.hp, self.mp = MAX_HP, MAX_MP
        self.attack_start = 0
        self.attack_end = COOLTIME_ATTACK
        self.defense_start = 0
        self.defense_end = COOLTIME_DEFENSE
        self.skill1_start = 0
        self.skill1_end = COOLTIME_SKILL1
        self.skill2_start = 0
        self.skill2_end = COOLTIME_SKILL2
        self.load_image()
        self.STOP = Stop(self)
        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.DASH = Dash(self)
        self.state_machine = StateMachine(
            self.IDLE,
            { self.STOP : {interaction_up: self.IDLE, pause_up: self.IDLE},
              self.IDLE : {Mleft_down: self.IDLE, space_down: self.IDLE, s_down: self.IDLE, e_down: self.IDLE, q_down: self.IDLE, r_down: self.IDLE, d_down: self.RUN, d_up: self.RUN, a_down: self.RUN, a_up: self.RUN, interaction_down: self.STOP, pause_down: self.STOP},
              self.RUN : {Mleft_down: self.RUN, space_down: self.RUN, s_down: self.RUN, e_down: self.RUN, q_down: self.RUN, d_down: self.IDLE, d_up: self.IDLE, a_down: self.IDLE, a_up: self.IDLE, shift_down: self.DASH},
              self.DASH : {Mleft_down: self.DASH, space_down: self.DASH, s_down: self.DASH, e_down: self.DASH, q_down: self.DASH, time_out: self.RUN, d_up: self.IDLE, a_up: self.IDLE}}
        )
    def jump(self):
        if self.jumping_up == False and self.jumping_down == False and self.tiptoe <= self.floor_y:
            self.jumping_up = True
            self.cur_jump_height = 0
    def skill(self, skill_num):
        player_skill = PlayerSkill(self.x, self.y, self.face_dir, skill_num)
        game_world.add_object(player_skill, 2)
    def update(self):
        self.state_machine.update()
    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))
    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())
    def get_bb(self):
        if self.face_dir == 1:
            return self.x - 40, self.y - 75, self.x + 20, self.y + 10 # 60*85
        elif self.face_dir == -1:
            return self.x - 20, self.y - 75, self.x + 40, self.y + 10
    def handle_collision(self, group, other):
        if group == 'player:staging' and on_staging(self, other) == True: # 충돌 상대가 플랫폼이고, 플랫폼 위에 있을 경우
            self.floor_y = other.y + other.height // 2
class Stop:
    def __init__(self, player):
        pass
    def enter(self, e):
        pass
    def exit(self, e):
        pass
    def do(self):
        pass
    def draw(self):
        pass
class Idle:
    def __init__(self, player):
        self.player = player
    def enter(self, e):
        if time_out(e):
            self.player.frame = 0
    def exit(self, e):
        self.player.attack_end = get_time()
        self.player.defense_end = get_time()
        self.player.skill1_end = get_time()
        self.player.skill2_end = get_time()
        if space_down(e):
            self.player.jump()
        elif s_down(e):
            if get_another_floor(self.player) == True and self.player.tiptoe <= self.player.floor_y:
                self.player.y -= 1
        elif Mleft_down(e) and self.player.attack_end - self.player.attack_start >= COOLTIME_ATTACK:
            self.player.attack_start = get_time()
            self.player.skill(0)
        elif r_down(e) and GD.ability_monster2 == True and self.player.defense_end - self.player.defense_start >= COOLTIME_DEFENSE:
            self.player.defense_start = get_time()
            self.player.skill(2)
        elif e_down(e) and GD.ability_monster3 == True and self.player.skill1_end - self.player.skill1_start >= COOLTIME_SKILL1:
            self.player.skill1_start = get_time()
            self.player.skill(3)
        elif q_down(e) and GD.ability_monster5 == True and self.player.skill2_end - self.player.skill2_start >= COOLTIME_SKILL2:
            self.player.skill2_start = get_time()
            self.player.skill(5)
    def do(self):
        self.player.floor_y = get_floor_y(self.player)
        self.player.tiptoe = self.player.get_bb()[1]
        self.player.frame = (self.player.frame + FRAMES_PER_ACTION_idle * ACTION_PER_TIME_idle * game_framework.frame_time) % FRAMES_PER_ACTION_idle
        if self.player.jumping_up == True and self.player.jumping_down == False:
            self.player.cur_jump_height += 10
            self.player.y += 10
            if self.player.cur_jump_height >= JUMP_HEIGHT:
                self.player.jumping_up = False
                self.player.jumping_down = True
        elif self.player.jumping_up == False and self.player.jumping_down == True and self.player.tiptoe > self.player.floor_y:
            self.player.y -= GRAVITY * 40 * game_framework.frame_time
            self.player.tiptoe = self.player.get_bb()[1]
            if self.player.tiptoe < self.player.floor_y:
                self.player.y = self.player.floor_y + 75
                self.player.jumping_down = False
        elif self.player.jumping_up == False and self.player.jumping_down == False and self.player.tiptoe > self.player.floor_y:
            self.player.y -= GRAVITY * 40 * game_framework.frame_time
            self.player.tiptoe = self.player.get_bb()[1]
            if self.player.tiptoe < self.player.floor_y:
                self.player.y = self.player.floor_y + 75
    def draw(self):
        if self.player.face_dir == 1:
            Player.images['Idle'][int(self.player.frame)].draw(self.player.x, self.player.y, 150, 150)
        elif self.player.face_dir == -1:
            Player.images['Idle'][int(self.player.frame)].composite_draw(0, 'h', self.player.x, self.player.y, 150, 150)
class Run:
    def __init__(self, player):
        self.player = player
    def enter(self, e):
        if d_down(e) or a_up(e):
            self.player.dir = self.player.face_dir = 1
        elif a_down(e) or d_up(e):
            self.player.dir = self.player.face_dir = -1
    def exit(self, e):
        self.player.attack_end = get_time()
        self.player.skill1_end = get_time()
        self.player.skill2_end = get_time()
        if space_down(e):
            self.player.jump()
        elif s_down(e):
            if get_another_floor(self.player) == True and self.player.tiptoe <= self.player.floor_y:
                self.player.y -= 1
        elif Mleft_down(e) and self.player.attack_end - self.player.attack_start >= COOLTIME_ATTACK:
            self.player.attack_start = get_time()
            self.player.skill(0)
        elif e_down(e) and GD.ability_monster3 == True and self.player.skill1_end - self.player.skill1_start >= COOLTIME_SKILL1:
            self.player.skill1_start = get_time()
            self.player.skill(3)
        elif q_down(e) and GD.ability_monster5 == True and self.player.skill2_end - self.player.skill2_start >= COOLTIME_SKILL2:
            self.player.skill2_start = get_time()
            self.player.skill(5)
    def do(self):
        self.player.floor_y = get_floor_y(self.player)
        self.player.tiptoe = self.player.get_bb()[1]
        self.player.frame = (self.player.frame + FRAMES_PER_ACTION_run * ACTION_PER_TIME_run * game_framework.frame_time) % FRAMES_PER_ACTION_run
        self.player.x += self.player.dir * RUN_SPEED_PPS * game_framework.frame_time
        if self.player.jumping_up == True and self.player.jumping_down == False:
            self.player.cur_jump_height += 10
            self.player.y += 10
            if self.player.cur_jump_height >= JUMP_HEIGHT:
                self.player.jumping_up = False
                self.player.jumping_down = True
        elif self.player.jumping_up == False and self.player.jumping_down == True and self.player.tiptoe > self.player.floor_y:
            self.player.y -= GRAVITY * 40 * game_framework.frame_time
            self.player.tiptoe = self.player.get_bb()[1]
            if self.player.tiptoe < self.player.floor_y:
                self.player.y = self.player.floor_y + 75
                self.player.jumping_down = False
        elif self.player.jumping_up == False and self.player.jumping_down == False and self.player.tiptoe > self.player.floor_y:
            self.player.y -= GRAVITY * 40 * game_framework.frame_time
            self.player.tiptoe = self.player.get_bb()[1]
            if self.player.tiptoe <= self.player.floor_y:
                self.player.y = self.player.floor_y + 75
    def draw(self):
        if self.player.face_dir == 1:
            Player.images['Run'][int(self.player.frame)].draw(self.player.x, self.player.y, 150, 150)
        elif self.player.face_dir == -1:
            Player.images['Run'][int(self.player.frame)].composite_draw(0, 'h', self.player.x, self.player.y, 150, 150)
class Dash:
    def __init__(self, player):
        self.player = player
    def enter(self, e):
        if shift_down(e):
            self.player.wait_time = get_time()
    def exit(self, e):
        self.player.attack_end = get_time()
        self.player.skill1_end = get_time()
        self.player.skill2_end = get_time()
        if space_down(e):
            self.player.jump()
        elif s_down(e):
            if get_another_floor(self.player) == True and self.player.tiptoe <= self.player.floor_y:
                self.player.y -= 1
        elif Mleft_down(e) and self.player.attack_end - self.player.attack_start >= COOLTIME_ATTACK:
            self.player.attack_start = get_time()
            self.player.skill(0)
        elif e_down(
                e) and GD.ability_monster3 == True and self.player.skill1_end - self.player.skill1_start >= COOLTIME_SKILL1:
            self.player.skill1_start = get_time()
            self.player.skill(3)
        elif q_down(
                e) and GD.ability_monster5 == True and self.player.skill2_end - self.player.skill2_start >= COOLTIME_SKILL2:
            self.player.skill2_start = get_time()
            self.player.skill(5)
    def do(self):
        self.player.floor_y = get_floor_y(self.player)
        self.player.tiptoe = self.player.get_bb()[1]
        self.player.x += self.player.dir * RUN_SPEED_PPS * game_framework.frame_time * 4
        if get_time() - self.player.wait_time > 0.5:
            self.player.state_machine.handle_state_event(('TIMEOUT', None))
        if self.player.jumping_up == True and self.player.jumping_down == False:
            self.player.cur_jump_height += 10
            self.player.y += 10
            if self.player.cur_jump_height >= JUMP_HEIGHT:
                self.player.jumping_up = False
                self.player.jumping_down = True
        elif self.player.jumping_up == False and self.player.jumping_down == True and self.player.tiptoe > self.player.floor_y:
            self.player.y -= GRAVITY * 40 * game_framework.frame_time
            self.player.tiptoe = self.player.get_bb()[1]
            if self.player.tiptoe < self.player.floor_y:
                self.player.y = self.player.floor_y + 75
                self.player.jumping_down = False
        elif self.player.jumping_up == False and self.player.jumping_down == False and self.player.tiptoe > self.player.floor_y:
            self.player.y -= GRAVITY * 40 * game_framework.frame_time
            self.player.tiptoe = self.player.get_bb()[1]
            if self.player.tiptoe < self.player.floor_y:
                self.player.y = self.player.floor_y + 75
    def draw(self):
        if self.player.face_dir == 1:
            Player.images['Run'][3].draw(self.player.x, self.player.y, 150, 150)
        elif self.player.face_dir == -1:
            Player.images['Run'][3].composite_draw(0, 'h', self.player.x, self.player.y, 150, 150)