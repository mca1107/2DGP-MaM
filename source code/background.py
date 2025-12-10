from pico2d import *
import global_data as GD
resource_address = 'C:\\Users\\moonc\\OneDrive\\문서\\GitHub\\2DGP-MaM\\resource\\'
class Background:
    def __init__(self):
        if GD.stage_num == 0 or GD.stage_num == 1:
            self.image = load_image(resource_address + 'stage1\\' + 'background.png')
    def update(self):
        pass
    def draw(self):
        self.image.clip_draw(0, 0, 480, 320, 1536 // 2, 960 // 2, 1536, 960)