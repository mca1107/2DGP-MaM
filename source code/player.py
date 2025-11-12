from pico2d import *
from sdl2 import *
from state_machine import StateMachine
import game_framework, game_world

time_out = lambda e: e[0] == 'TIMEOUT'
def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT
def shift_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LSHIFT
def shift_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LSHIFT
def interaction_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_f # and 플레이어가 상호작용 오브젝트와 닿은 상태
def interaction_up(e):
    return # 상호작용이 끝나면 자동으로 종료
def pause_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_ESCAPE # and 일시정지 상태가 이닌 경우
def pause_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_ESCAPE # and 일시정지 상태인 경우

# player move speed
PIXEL_PER_METER = (10.0 / 2.0) # 10 pixel == 2 meter
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
# player action speed
TIME_PER_ACTION = 0.5 # 한 걸음 걷는데 걸리는 시간 0.5초
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6 # 한 걸음 걷는데 필요한 프레임 6장
animation_names = ['Run'] # Idle 애니메이션 추가
resource_address = 'C:\\Users\\moonc\\OneDrive\\문서\\GitHub\\2DGP-MaM\\resource\\player\\'
class Player:
    images = None
    def load_image(self):
        if Player.images == None:
            Player.images = {}
            for name in animation_names:
                Player.images[name] = [load_image(resource_address + name + " (%d)" % i + ".png") for i in range(1, 7)]
    def __init__(self):
        self.x, self.y = 768, 480
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.load_image()
        self.STOP = Stop(self)
        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.DASH = Dash(self)
        self.JUMP = Jump(self)
        self.state_machine = StateMachine(
            self.IDLE,
            { self.STOP : {interaction_up: self.IDLE, pause_up: self.IDLE},
              self.IDLE : {right_down: self.RUN, left_down: self.RUN, space_down: self.JUMP, interaction_down: self.STOP, pause_down: self.STOP},
              self.RUN : {right_up: self.IDLE, left_up: self.IDLE, shift_down: self.DASH, space_down: self.JUMP},
              self.DASH : {time_out: self.RUN, }}
        )
    def update(self):
        self.state_machine.update()
    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))
    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.x - 30, self.y - 50, self.x + 30, self.y + 10
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
        pass
    def exit(self, e):
        pass
    def do(self):
        pass
    def draw(self):
        pass
class Run:
    def __init__(self, player):
        self.player = player
    def enter(self, e):
        if right_down(e):
            self.player.dir = self.player.face_dir = 1
        elif left_down(e):
            self.player.dir = self.player.face_dir = -1
    def exit(self, e):
        pass
    def do(self):
        self.player.frame = (self.player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.player.x += self.player.dir * RUN_SPEED_PPS * game_framework.frame_time
    def draw(self):
        if self.player.face_dir == 1:
            Player.images['Run'][int(self.player.frame)].draw(self.player.x, self.player.y, 100, 100)
        elif self.player.face_dir == -1:
            Player.images['Run'][int(self.player.frame)].composite_draw(0, 'h', self.player.x, self.player.y, 100, 100)
class Dash:
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
class Jump:
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