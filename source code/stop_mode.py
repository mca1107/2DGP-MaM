from pico2d import *
import play_mode
import game_framework

image = None
running = True
def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.pop_mode() # 원래 스테이지로 돌아가야 함
def init():
    global image, running
    # image = load_image(?)
def finish():
    global image
    del image
def update():
    pass
def draw():
    clear_canvas()
    image.draw(960, 540)
    update_canvas()
def pause(): pass
def resume(): pass