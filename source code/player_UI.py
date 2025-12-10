from pico2d import *
import game_framework, game_world
import global_data as GD
import player
resource_address = 'C:\\Users\\moonc\\OneDrive\\문서\\GitHub\\2DGP-MaM\\resource\\player\\UI\\'

class Button:
    images = None
    def load_image(self):
        if Button.images == None:
            Button.images = {}
            Button.images['Pause'] = [load_image(resource_address + "Btn_pause" + " (%d)" % i + ".png") for i in range(1, 3)]
            Button.images['Quit'] = [load_image(resource_address + "Btn_quit" + " (%d)" % i + ".png") for i in range(1, 3)]
    def __init__(self, x, y, btn_type, visible):
        self.x, self.y = x, y
        self.frame = 0
        self.type = btn_type
        self.visible = visible
        self.load_image()
    def draw(self):
        if self.visible == True:
            if self.type == 'Pause':
                Button.images['Pause'][int(self.frame)].draw(self.x, self.y)
            elif self.type == 'Quit':
                Button.images['Quit'][int(self.frame)].draw(self.x, self.y, 120, 120)
    def update(self):
        pass
    def get_bb(self):
        if self.type == 'Pause':
            return self.x - 40, self.y - 40, self.x + 40, self.y + 40
        elif self.type == 'Quit':
            return self.x - 60, self.y - 60, self.x + 60, self.y + 60
    def handle_collision(self, group, other):
        if group == 'mouse:button' and self.frame == 0:
            if self.type == 'Pause':
                self.frame = 1
                # 게임 일시정지 모드로 전환, 정보 창 띄움
            elif self.type == 'Quit':
                self.frame = 1
class Panel:
    images = None
    def load_image(self):
        if Panel.images == None:
            Panel.images = {}
            Panel.images['Info'] = load_image(resource_address + "Panel_info.png")
            Panel.images['Talk'] = load_image(resource_address + "Panel_talk.png")
    def __init__(self, x, y, pnl_type, visible):
        self.x, self.y = x, y
        self.type = pnl_type
        self.visible = visible
        self.load_image()
    def draw(self):
        if self.visible == True:
            if self.type == 'Info':
                Panel.images['Info'].draw(self.x, self.y, 500, 500)
            elif self.type == 'Talk':
                Panel.images['Talk'].draw(self.x, self.y, 500, 500)
    def update(self):
        pass
    def get_bb(self):
        if self.type == 'Info':
            return self.x - 250, self.y - 250, self.x + 250, self.y + 250
        elif self.type == 'Talk':
            return self.x - 400, self.y - 150, self.x + 400, self.y + 150
    def handle_collision(self, group, other):
        pass
class Icon:
    images = None
    def load_image(self):
        if Icon.images == None:
            Icon.images = {}
            Icon.images['Normal'] = [load_image(resource_address + "Icon_normal" + " (%d)" % i + ".png") for i in range(1, 3)]
            Icon.images['Orange'] = [load_image(resource_address + "Icon_orange" + " (%d)" % i + ".png") for i in range(1, 3)]
            Icon.images['Blue'] = [load_image(resource_address + "Icon_blue" + " (%d)" % i + ".png") for i in range(1, 3)]
            Icon.images['White'] = [load_image(resource_address + "Icon_white" + " (%d)" % i + ".png") for i in range(1, 3)]
            Icon.images['Pink'] = [load_image(resource_address + "Icon_pink" + " (%d)" % i + ".png") for i in range(1, 3)]
            Icon.images['Black'] = [load_image(resource_address + "Icon_black" + " (%d)" % i + ".png") for i in range(1, 3)]
    def __init__(self, x, y, icon_num, visible):
        self.x, self.y = x, y
        self.frame = 0
        self.num = icon_num
        self.visible = visible
        self.load_image()
    def draw(self):
        if self.visible == True:
            if self.num == 0:
                Icon.images['Normal'][int(self.frame)].draw(self.x, self.y)
            elif self.num == 1:
                Icon.images['Orange'][int(self.frame)].draw(self.x, self.y)
            elif self.num == 2:
                Icon.images['Blue'][int(self.frame)].draw(self.x, self.y)
            elif self.num == 3:
                Icon.images['White'][int(self.frame)].draw(self.x, self.y)
            elif self.num == 4:
                Icon.images['Pink'][0].draw(self.x, self.y, 70, 70)
                Icon.images['Pink'][1].draw(self.x, self.y - 62, 70, 70)
            elif self.num == 5:
                Icon.images['Black'][int(self.frame)].draw(self.x, self.y)
    def update(self):
        pass
    def get_bb(self):
        return self.x - 40, self.y - 40, self.x + 40, self.y + 40
    def handle_collision(self, group, other):
        pass
class Bar:
    images = None
    def load_image(self):
        if Bar.images == None:
            Bar.images = {}
            Bar.images['Bar_background'] = load_image(resource_address + "Bar_background.png")
            Bar.images['HP_frame'] = load_image(resource_address + "HP_bar_frame.png")
            Bar.images['HP_space'] = load_image(resource_address + "HP_bar_space.png")
            Bar.images['MP_frame'] = load_image(resource_address + "MP_bar_frame.png")
            Bar.images['MP_space'] = load_image(resource_address + "MP_bar_space.png")
    def __init__(self, x, y, bar_type, space_num, player):
        self.player = player
        self.x, self.y = x, y
        self.type = bar_type
        if self.type == 'HP':
            self.hp_num = space_num
        elif self.type == 'MP':
            self.mp_num = space_num
        self.load_image()
    def draw(self):
        if self.type == 'HP':
            Bar.images['Bar_background'].draw(self.x, self.y, 356, 32)
            for i in range(0, self.hp_num):
                Bar.images['HP_space'].draw(self.x - 110 + i * 30, self.y, 29, 24)
            Bar.images['HP_frame'].draw(self.x, self.y, 376, 52)
        if self.type == 'MP':
            Bar.images['Bar_background'].draw(self.x, self.y, 356, 32)
            for i in range(0, self.mp_num):
                Bar.images['MP_space'].draw(self.x - 110 + i * 30, self.y, 29, 24)
            Bar.images['MP_frame'].draw(self.x, self.y, 376, 52)
    def update(self):
        self.hp_num = self.player.hp
        self.mp_num = self.player.mp