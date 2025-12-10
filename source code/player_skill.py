from pico2d import *
import game_framework, game_world
resource_address = 'C:\\Users\\moonc\\OneDrive\\문서\\GitHub\\2DGP-MaM\\resource\\player\\effect\\'

TIME_PER_ACTION_normal = 0.2
ACTION_PER_TIME_normal = 1.0 / TIME_PER_ACTION_normal
FRAMES_PER_ACTION_normal = 4
TIME_PER_ACTION_blue = 0.3
ACTION_PER_TIME_blue = 1.0 / TIME_PER_ACTION_blue
FRAMES_PER_ACTION_blue = 8
TIME_PER_ACTION_white = 1.0
ACTION_PER_TIME_white = 1.0 / TIME_PER_ACTION_white
FRAMES_PER_ACTION_white = 3
TIME_PER_ACTION_black = 1.4
ACTION_PER_TIME_black = 1.0 / TIME_PER_ACTION_black
FRAMES_PER_ACTION_black = 7

class PlayerSkill:
    images = None
    def load_image(self):
        if PlayerSkill.images is None:
            PlayerSkill.images = {}
            PlayerSkill.images['Normal'] = [load_image(resource_address + "Normal" + " (%d)" % i + ".png") for i in range(1, 5)]
            PlayerSkill.images['Blue'] = [load_image(resource_address + "Blue" + " (%d)" % i + ".png") for i in range(1, 9)]
            PlayerSkill.images['White'] = [load_image(resource_address + "White" + " (%d)" % i + ".png") for i in range(1, 4)]
            PlayerSkill.images['Black'] = [load_image(resource_address + "Black" + " (%d)" % i + ".png") for i in range(1, 8)]
    def __init__(self, x, y, dir, skill_num):
        self.x = x
        self.y = y
        self.dir = dir
        self.num = skill_num
        if self.num == 0:
            self.damage = 1
        elif self.num == 3:
            self.damage = 2
        elif self.num == 5:
            self.damage = 4
        else:
            self.damage = 0
        self.frame = 0
        self.frame_num = 0
        self.load_image()
    def draw(self):
        if self.dir == 1:
            if self.num == 0:
                PlayerSkill.images['Normal'][int(self.frame)].draw(self.x + 30, self.y - 30, 94, 112)
            elif self.num == 2:
                PlayerSkill.images['Blue'][int(self.frame)].draw(self.x, self.y - 30, 50, 100)
            elif self.num == 3:
                PlayerSkill.images['White'][int(self.frame)].draw(self.x + 60, self.y - 30, 160, 80)
            elif self.num == 5:
                PlayerSkill.images['Black'][int(self.frame)].draw(self.x + 300, self.y + 40, 300, 300)
        elif self.dir == -1:
            if self.num == 0:
                PlayerSkill.images['Normal'][int(self.frame)].composite_draw(0, 'h', self.x - 30, self.y - 30, 94, 112)
            elif self.num == 2:
                PlayerSkill.images['Blue'][int(self.frame)].composite_draw(0, 'h', self.x, self.y - 30, 50, 100)
            elif self.num == 3:
                PlayerSkill.images['White'][int(self.frame)].composite_draw(0, 'h', self.x - 60, self.y -30, 160, 80)
            elif self.num == 5:
                PlayerSkill.images['Black'][int(self.frame)].composite_draw(0, 'h', self.x - 300, self.y + 40, 300, 300)
    def update(self):
        if self.num == 0:
            if self.frame_num >= FRAMES_PER_ACTION_normal -1:
                game_world.remove_object(self)
                self.frame_num = 0
                self.frame = 0
            self.frame = (self.frame + FRAMES_PER_ACTION_blue * ACTION_PER_TIME_blue * game_framework.frame_time) % FRAMES_PER_ACTION_blue
            self.frame_num = int(self.frame)
        elif self.num == 2:
            if self.frame_num >= FRAMES_PER_ACTION_blue -1:
                game_world.remove_object(self)
                self.frame_num = 0
                self.frame = 0
            self.frame = (self.frame + FRAMES_PER_ACTION_blue * ACTION_PER_TIME_blue * game_framework.frame_time) % FRAMES_PER_ACTION_blue
            self.frame_num = int(self.frame)
        elif self.num == 3:
            if self.frame_num >= FRAMES_PER_ACTION_white -1:
                game_world.remove_object(self)
                self.frame_num = 0
                self.frame = 0
            self.frame = (self.frame + FRAMES_PER_ACTION_white * ACTION_PER_TIME_white * game_framework.frame_time) % FRAMES_PER_ACTION_white
            self.x += 400 * self.dir * game_framework.frame_time
            self.frame_num = int(self.frame)
        elif self.num == 5:
            if self.frame_num >= FRAMES_PER_ACTION_black -1:
                game_world.remove_object(self)
                self.frame_num = 0
                self.frame = 0
            self.frame = (self.frame + FRAMES_PER_ACTION_black * ACTION_PER_TIME_black * game_framework.frame_time) % FRAMES_PER_ACTION_black
            self.frame_num = int(self.frame)
    def get_bb(self):
        if self.dir == 1:
            if self.num == 0:
                return self.x, self.y - 85, self.x + 80, self.y + 20
            elif self.num == 2:
                return self.x - 50, self.y - 85, self.x + 30, self.y + 20
            elif self.num == 3:
                return self.x - 10, self.y - 55, self.x + 140, self.y
            elif self.num == 5:
                return self.x + 200, self.y - 80, self.x + 400, self.y + 120
        elif self.dir == -1:
            if self.num == 0:
                return self.x - 80, self.y - 85, self.x, self.y + 20
            elif self.num == 2:
                return self.x - 30, self.y - 85, self.x + 50, self.y + 20
            elif self.num == 3:
                return self.x - 140, self.y - 55, self.x + 10, self.y
            elif self.num == 5:
                return self.x - 400, self.y - 80, self.x - 200, self.y + 120
    def handle_collision(self, group, other):
        pass