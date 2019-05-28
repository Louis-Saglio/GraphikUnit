from __future__ import annotations

from math import sqrt
from typing import Tuple, List

from lib import Number


class Particle:
    def __init__(self, mass: Number, position: List[Number], velocity: List[Number]):
        self.mass = mass
        self.position = position
        self.velocity = velocity

    def apply_force(self, force: Tuple[Number, Number]):
        for i in range(len(force)):
            self.velocity[i] += force[i]

    def exist(self):
        for i in range(len(self.position)):
            self.position[i] += self.velocity[i]


class Law:
    def compute_force(self, particle: Particle, other_particle: Particle) -> Tuple[Number, Number]:
        raise NotImplementedError


def distance_between(position, other_position):
    return sqrt((position[0] - other_position[0]) ** 2 + (position[1] - other_position[1]) ** 2)
