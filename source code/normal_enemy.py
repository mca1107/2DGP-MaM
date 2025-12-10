from pico2d import *
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from state_machine import StateMachine
import global_data as GD
import game_framework, game_world
import player
resource_address = 'C:\\Users\\moonc\\OneDrive\\문서\\GitHub\\2DGP-MaM\\resource\\enemy\\normal_enemy\\'

def get_floor_y(enemy):
    max_floor_y = 0
    for floor in game_world.collision_pairs['enemy:floor'][1]:
        fx1, fy1, fx2, fy2 = floor.get_bb()
        if on_floor(enemy, floor) and fy1 > max_floor_y:
            max_floor_y = fy1
    return max_floor_y
def on_floor(enemy, floor):
    ex1, ey1, ex2, ey2 = enemy.get_bb()
    fx1, fy1, fx2, fy2 = floor.get_bb()
    if ex2 > fx1 and ex1 < fx2 and ey1 >= fy1:
        return True
    else:
        return False
def in_floor(enemy, floor):
    ex1, ey1, ex2, ey2 = enemy.get_bb()
    fx1, fy1, fx2, fy2 = floor.get_bb()
    if ex1 > fx1 and ex2 < fx2:
        return True
    else:
        return False

INVINCIBLE_TIME = 1.5

PIXEL_PER_METER = (10.0 / 2.0) # 10 pixel == 1 meter
RUN_SPEED_KMPH = 40.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

class NormalEnemy:
    images = None
    def load_image(self):
        if NormalEnemy.images == None:
            NormalEnemy.images = {}
            NormalEnemy.images['Mushroom_Red'] = [load_image(resource_address + "Mushroom\\" + "Red" + " (%d)" % i + ".png") for i in range(1, 5)]
            NormalEnemy.images['Mushroom_Green'] = [load_image(resource_address + "Mushroom\\" + "Green" + " (%d)" % i + ".png") for i in range(1, 5)]
            NormalEnemy.images['Mushroom_Blue'] = [load_image(resource_address + "Mushroom\\" + "Blue" + " (%d)" % i + ".png") for i in range(1, 5)]
    def __init__(self, x, y, enemy_type, dir):
        self.N_enemy = self
        self.x, self.y = x, y
        self.tx, self.ty = 0, 0
        self.type = enemy_type
        self.floor_y = get_floor_y(self)
        if self.type in ('Mushroom_Red', 'Mushroom_Green', 'Mushroom_Blue'):
            self.y = self.floor_y + 40
        self.frame = 0
        self.face_dir = dir
        self.hp = 5
        self.tiptoe = self.get_bb()[1]
        self.invincible_start = 0
        self.invincible_end = INVINCIBLE_TIME
        self.load_image()
    def update(self):
        if self.hp <= 0:
            delay(0.05)
            game_world.remove_object(self)
            return
        self.floor_y = get_floor_y(self)
        self.tiptoe = self.get_bb()[1]
        if self.tiptoe < self.floor_y:
            self.y += (self.floor_y - self.tiptoe)
            self.tiptoe = self.get_bb()[1]
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        for floor in game_world.collision_pairs['enemy:floor'][1]:
            if game_world.collide_rect_to_line(self, floor) == True and in_floor(self, floor) == False:
                self.face_dir *= -1
                self.x += self.face_dir * RUN_SPEED_PPS * game_framework.frame_time
    def draw(self):
        if self.face_dir == 1:
            if self.type == 'Mushroom_Red':
                NormalEnemy.images['Mushroom_Red'][int(self.frame)].draw(self.x, self.y)
            elif self.type == 'Mushroom_Green':
                NormalEnemy.images['Mushroom_Green'][int(self.frame)].draw(self.x, self.y)
            elif self.type == 'Mushroom_Blue':
                NormalEnemy.images['Mushroom_Blue'][int(self.frame)].draw(self.x, self.y)
        elif self.face_dir == -1:
            if self.type == 'Mushroom_Red':
                NormalEnemy.images['Mushroom_Red'][int(self.frame)].composite_draw(0, 'h', self.x, self.y)
            elif self.type == 'Mushroom_Green':
                NormalEnemy.images['Mushroom_Green'][int(self.frame)].composite_draw(0, 'h', self.x, self.y)
            elif self.type == 'Mushroom_Blue':
                NormalEnemy.images['Mushroom_Blue'][int(self.frame)].composite_draw(0, 'h', self.x, self.y)
    def get_bb(self):
        if self.type in ('Mushroom_Red', 'Mushroom_Green', 'Mushroom_Blue'):
            return self.x - 40, self.y - 40, self.x + 40, self.y + 40  # 80*80
        return self.x - 40, self.y - 40, self.x + 40, self.y + 40
    def handle_collision(self, group, other):
        if group == 'attack:enemy':
            self.invincible_end = get_time()
            if self.invincible_end - self.invincible_start >= INVINCIBLE_TIME:
                self.invincible_start = get_time()
                self.hp -= other.damage
    def distance_less_than(self, x1, y1, x2, y2, r):
        return (x1 - x2) ** 2 + (y1 - y2) ** 2 < (PIXEL_PER_METER * r) ** 2
    def if_player_nearby(self, distance):
        if self.distance_less_than(self.x, self.y, GD.player.x, GD.player.y, distance):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
    def get_player_location(self):
        self.tx = GD.player.x
        self.ty = GD.player.y
        return BehaviorTree.SUCCESS
    def get_foothold_location(self):
        margin = 40
        cur_floor = None
        floors = game_world.collision_pairs['enemy:floor'][1]
        for floor in floors:
            if in_floor(self, floor) or on_floor(self, floor):
                cur_floor = floor
                break
        if cur_floor:
            fx1, fy1, fx2, fy2 = cur_floor.get_bb()
            if self.face_dir >= 0:
                tx_candidate = fx2 - margin
            else:
                tx_candidate = fx1 + margin
            ty_candidate = fy1 + margin
            self.tx = tx_candidate
            self.ty = ty_candidate
            return BehaviorTree.SUCCESS
        self.tx = self.x + self.face_dir * 60
        self.ty = self.floor_y + margin
        return BehaviorTree.SUCCESS
    def move_to_location(self):
        if self.distance_less_than(self.x, self.y, self.tx, self.ty, 0.5):
            return BehaviorTree.SUCCESS
        if self.tx > self.x:
            self.face_dir = 1
        else:
            self.face_dir = -1
        dx = self.face_dir * RUN_SPEED_PPS * game_framework.frame_time
        self.x += dx
        for floor in game_world.collision_pairs['enemy:floor'][1]:
            if game_world.collide_rect_to_line(self, floor) and not in_floor(self, floor):
                self.x -= dx
                self.face_dir *= -1
                return BehaviorTree.FAIL
        return BehaviorTree.RUNNING
    def build_behavior_tree(self):
        c1 = Condition("플레이어가 근처에 있는가?", self.if_player_nearby, 30)
        a1 = Action("플레이어 위치 좌표 가져오기", self.get_player_location)
        a2 = Action("지정 위치로 이동하기", self.move_to_location)
        a3 = Action("현재 플랫폼의 가장자리 좌표 가져오기", self.get_foothold_location)
        chase_player_if_detect = Sequence("플레이어 감지하면 추적", a1, a2)
        detecting_player_if_nearby = Sequence("플레이어가 근처에 있으면 감지", c1, chase_player_if_detect)
        wandering_if_far = Sequence("플레이어가 근처에 없으면 배회", a3, a2)
        root = detecting_or_wander = Selector("감지 또는 배회", detecting_player_if_nearby, wandering_if_far)
        self.bt = BehaviorTree(root)

class Idle:
    def __init__(self, normal_enemy):
        self.N_enemy = normal_enemy
    def enter(self, e):
        pass
    def exit(self, e):
        pass
    def do(self):
        self.N_enemy.frame = (self.N_enemy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.N_enemy.x += self.N_enemy.face_dir * RUN_SPEED_PPS * game_framework.frame_time
        for floor in game_world.collision_pairs['enemy:floor'][1]:
            if game_world.collide_rect_to_line(self.N_enemy, floor) and in_floor(self.N_enemy, floor) == False:
                self.N_enemy.face_dir *= -1
                self.N_enemy.x += self.N_enemy.face_dir * RUN_SPEED_PPS * game_framework.frame_time
    def draw(self):
        if self.N_enemy.face_dir == 1:
            if self.N_enemy.type == 'Mushroom_Red':
                NormalEnemy.images['Mushroom_Red'][int(self.N_enemy.frame)].draw(self.N_enemy.x, self.N_enemy.y)
            elif self.N_enemy.type == 'Mushroom_Green':
                NormalEnemy.images['Mushroom_Green'][int(self.N_enemy.frame)].draw(self.N_enemy.x, self.N_enemy.y)
            elif self.N_enemy.type == 'Mushroom_Blue':
                NormalEnemy.images['Mushroom_Blue'][int(self.N_enemy.frame)].draw(self.N_enemy.x, self.N_enemy.y)
        elif self.N_enemy.face_dir == -1:
            if self.N_enemy.type == 'Mushroom_Red':
                NormalEnemy.images['Mushroom_Red'][int(self.N_enemy.frame)].composite_draw(0, 'h', self.N_enemy.x, self.N_enemy.y)
            elif self.N_enemy.type == 'Mushroom_Green':
                NormalEnemy.images['Mushroom_Green'][int(self.N_enemy.frame)].composite_draw(0, 'h', self.N_enemy.x, self.N_enemy.y)
            elif self.N_enemy.type == 'Mushroom_Blue':
                NormalEnemy.images['Mushroom_Blue'][int(self.N_enemy.frame)].composite_draw(0, 'h', self.N_enemy.x, self.N_enemy.y)

class Hunt:
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