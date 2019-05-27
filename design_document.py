from random import randint, random
from typing import Any, Tuple
from tkinter import Tk

from lib import Motherboard, Number, MovableUnitMixin


screen = Tk()

map_ = Motherboard(screen.winfo_screenwidth(), screen.winfo_screenheight())


class CustomUnit(MovableUnitMixin):
    def __init__(self, initial_position, goal, speed):
        self._position = initial_position
        self._color = randint(0, 255), randint(0, 255), randint(0, 255)
        self.goal = goal
        self.speed = speed

    @property
    def position(self) -> Tuple[Number, Number]:
        return self._position

    @property
    def dimensions(self) -> Tuple[Number, Number]:
        return 2, 2

    @property
    def color(self) -> Any:
        return self._color

    def run(self, total_time, **kwargs):
        self.move_toward(self.goal, self.speed)
        if randint(0, 49) == 0:
            self.goal = randint(-7450, 7450), randint(-4950, 4950)
            self.speed = random() * 5

    @position.setter
    def position(self, value):
        self._position = value


for _ in range(1_000):
    map_.add_unit(
        CustomUnit(
            (randint(-map_.width / 2, map_.width / 2), randint(-map_.height / 2, map_.height / 2)),
            (randint(-map_.width / 2, map_.width / 2), randint(-map_.height / 2, map_.height / 2)),
            random() * 5,
        )
    )

map_.loop()
