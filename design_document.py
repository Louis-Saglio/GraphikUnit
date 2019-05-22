from random import randint, random
from typing import Any, Tuple

from main import Motherboard, Number, MovableUnitMixin

map_ = Motherboard(1500, 1000)


class CustomUnit(MovableUnitMixin):

    def __init__(self, initial_position, goal, speed):
        self._position = initial_position
        self._color = randint(0, 255), randint(0, 255), randint(0, 255)
        self.goal = goal
        self.speed = speed

    @property
    def position(self) -> Tuple[Number, Number]:
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def dimensions(self) -> Tuple[Number, Number]:
        return 5, 5

    @property
    def color(self) -> Any:
        return self._color

    def run(self):
        self.move_toward(self.goal, self.speed)
        if randint(0, 49) == 0:
            self.goal = randint(-745, 745), randint(-495, 495)
            self.speed = random() * 5


for _ in range(10):
    map_.add_unit(CustomUnit((randint(-745, 745), randint(-495, 495)), (randint(-745, 745), randint(-495, 495)), random() * 5))

map_.loop()
