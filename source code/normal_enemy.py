from pico2d import *
from state_machine import StateMachine
import game_world

PIXEL_PER_METER = ?
RUN_SPEED_KMPH = ?
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = ?
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = ?
class Idle:
    def __init__(self, player):
        pass
    def enter(self, e):
        pass
    def exit(self, e):
        pass
    def do(self):
        pass
    def draw(self):
        pass
# class Hunt:
class NormalEnemy:
    def __init__(self):
        self.image = load_image(?)

        self.state_machine = StateMachine(
            self.IDLE,
            { }
        )
    def update(self):
        self.state_machine.update()
    def draw(self):
        self.state_machine.draw()