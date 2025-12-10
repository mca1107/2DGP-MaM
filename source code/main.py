from pico2d import *
import game_framework
import global_data as GD
import title_mode as start_mode
open_canvas(GD.game_width, GD.game_height)
game_framework.run(start_mode)
close_canvas()