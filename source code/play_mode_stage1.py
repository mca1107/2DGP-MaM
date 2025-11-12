from pico2d import *
import stop_mode
import game_framework

resource_address = 'C:\\Users\\moonc\\OneDrive\\문서\\GitHub\\2DGP-MaM\\resource\\'
image = None
running = True
def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.push_mode(stop_mode)
        # elif ?: # 스테이지 클리어 시 다음 스테이지로 넘어감
        #     game_framework.change_mode(?)
def init():
    global image, running
    image = load_image(resource_address + 'stage1_image.png')
def finish():
    global image
    del image
def update():
    pass
def draw():
    clear_canvas()
    image.draw(768, 480)
    update_canvas()
def pause(): pass
def resume(): pass