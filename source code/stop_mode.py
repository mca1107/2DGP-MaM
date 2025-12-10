from pico2d import *
from player_UI import Button, Panel
import global_data as GD
import game_framework, game_world
import play_mode

running = True
def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.pop_mode()
def init():
    panel = Panel(GD.game_width // 2, GD.game_height // 2, 'Info', True)
    game_world.add_object(panel, 5)
    button = Button(640, 610, 'Quit', True)
    game_world.add_object(button, 5)
    game_world.add_collision_pair('mouse:button', None, button)
def update():
    game_world.update()
    game_world.handle_collisions()
def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
def finish():
    game_world.clear()
def pause(): pass
def resume(): pass