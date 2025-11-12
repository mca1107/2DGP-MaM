from pico2d import *
from player import Player
from background import Background
import game_framework, game_world
import stop_mode
import global_data as GD

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
        #     GD.stage_num 값 변화
        else:
            player.handle_event(event)
def init():
    global player
    background = Background()
    game_world.add_object(background, 0)
    player = Player()
    game_world.add_object(player, 1)
def finish():
    game_world.clear()
def update():
    game_world.update()
def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
def pause(): pass
def resume(): pass