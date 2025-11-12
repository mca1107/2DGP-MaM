from pico2d import *
import game_framework
import global_data as GD
import play_mode_stage1

resource_address = 'C:\\Users\\moonc\\OneDrive\\문서\\GitHub\\2DGP-MaM\\resource\\'
image = None
running = True
def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(play_mode_stage1)
            GD.stage_num = 1
def init():
    global image, running
    image = load_image(resource_address + 'title_image.png')
def finish():
    global image
    del image
def update():
    pass
def draw():
    clear_canvas()
    image.draw(1536 // 2, 960 // 2)
    update_canvas()
def pause(): pass
def resume(): pass