from pico2d import *
from background import Background
from foothold import Staging, Floor
from player import Player
from normal_enemy import NormalEnemy
from player_UI import Button, Panel, Icon, Bar
import global_data as GD
import game_framework, game_world
import stop_mode
import random

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

    stagings = [
        Staging(768, 80, 1536, 160),
        Staging(400, 400, 300, 100),
        Staging(1100, 600, 400, 100),
    ]
    game_world.add_objects(stagings, 2)

    floors = [
        Floor(0, 1536, 160),
        Floor(250, 550, 450),
        Floor(900, 1300, 650),
    ]
    game_world.add_objects(floors, 2)
    for floor in floors:
        game_world.add_collision_pair('player:floor', None, floor)
        game_world.add_collision_pair('enemy:floor', None, floor)

    player = Player(200, 320)
    game_world.add_object(player, 3)
    game_world.add_collision_pair('player:floor', player, None)
    game_world.add_collision_pair('player:enemy', player, None)

    N_enemies = [
        NormalEnemy(800, 240, 'Mushroom_Red', random.choice([1, -1])),
        NormalEnemy(1200, 700, 'Mushroom_Green', random.choice([1, -1])),
        NormalEnemy(400, 500, 'Mushroom_Blue', random.choice([1, -1])),
    ]
    game_world.add_objects(N_enemies, 4)
    for enemy in N_enemies:
        game_world.add_collision_pair('enemy:floor', enemy, None)
        game_world.add_collision_pair('player:enemy', None, enemy)
        game_world.add_collision_pair('attack:enemy', None, enemy)

    button = Button(60, 900, 'Pause', True)
    game_world.add_object(button, 5)
    game_world.add_collision_pair('mouse:button', None, button)

    icons = [
        Icon(GD.game_width - 420, 60, 0, True),
        Icon(GD.game_width - 330, 60, 1, True),
        Icon(GD.game_width - 240, 60, 2, True),
        Icon(GD.game_width - 150, 60, 3, True),
        Icon(1092, 914, 4, True),
        Icon(GD.game_width - 60, 60, 5, True),
    ]
    game_world.add_objects(icons, 5)

    bars = [
        Bar(1328, 914, 'HP', 10, player),
        Bar(1328, 852, 'MP', 10, player),
    ]
    game_world.add_objects(bars, 5)
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