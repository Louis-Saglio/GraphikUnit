from math import sqrt
from random import randint
from typing import Tuple, List

from graphical_engine import GraphicalParticle, Universe
from physics import Number


class Atom(GraphicalParticle):
    color_options = {
        "dynamic": lambda self: (
            255,
            min(abs((self.velocity[0] + self.velocity[1] + 1) ** 6), 255),
            min(abs((self.velocity[0] + self.velocity[1] + 1) ** 6), 255),
        ),
        "random": lambda self: self._color,
    }

    def __init__(
        self, universe: Universe, mass: Number, position: List[Number], velocity: List[Number], color_option="random"
    ):
        super().__init__(universe, mass, position, velocity)
        self.color_option = color_option
        if self.color_option == "random":
            self._color = randint(0, 255), randint(0, 255), randint(0, 255)

    @property
    def color(self) -> Tuple[Number, Number, Number]:
        return self.color_options[self.color_option](self)

    @property
    def dimension(self) -> Number:
        return sqrt(self.mass)
