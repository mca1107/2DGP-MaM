from pico2d import *
import global_data as GD
resource_address = 'C:\\Users\\moonc\\OneDrive\\문서\\GitHub\\2DGP-MaM\\resource\\'
class Staging:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        if GD.stage_num == 1:
            self.image = load_image(resource_address + 'stage1\\' + 'staging.png')
    def update(self):
        pass
    def draw(self):
        draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.x - self.width // 2, self.y - self.height // 2, self.x + self.width // 2, self.y + self.height // 2