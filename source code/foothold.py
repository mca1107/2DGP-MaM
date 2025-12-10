from pico2d import *
import global_data as GD
resource_address = 'C:\\Users\\moonc\\OneDrive\\문서\\GitHub\\2DGP-MaM\\resource\\'
class Staging:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        if GD.stage_num == 0 or GD.stage_num == 1:
            self.image = load_image(resource_address + "stage1\\" + "staging.png")
    def update(self):
        pass
    def draw(self):
        self.image.clip_draw(0, 0, 480, 137, self.x, self.y, self.width, self.height)
    def get_bb(self):
        return self.x - self.width // 2, self.y - self.height // 2, self.x + self.width // 2, self.y + self.height // 2
    def handle_collision(self, group, other):
        pass
class Floor:
    def __init__(self, x1, x2, y):
        self.x1, self.x2 = x1, x2
        self.y = y
    def update(self):
        pass
    def draw(self):
        pass
    def get_bb(self):
        return self.x1, self.y, self.x2, self.y
    def handle_collision(self, group, other):
        if group == 'player:floor':
            pass