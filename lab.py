from __future__ import annotations

from math import sqrt
from typing import Tuple, Union, List

Number = Union[int, float]
Point = Tuple[Number, Number]


def divide(a, b):
    if b == 0:
        if a == 0:
            return 1
        return float("inf")
    return a / b


class Force:
    def __init__(self, origin: Point, direction: Point, intensity: Number):
        self.intensity = intensity
        self.direction = direction
        self.origin = origin

    def __eq__(self, other: Force):
        return self.intensity, self.direction, self.origin == other.intensity, other.direction, other.origin


def compute(force: Force):
    return (
        (
            force.origin[0]
            + (force.direction[0] - force.origin[0])
            * force.intensity
            / (sqrt((force.origin[0] - force.direction[0]) ** 2 + (force.origin[1] - force.direction[1]) ** 2))
        ),
        (
            force.origin[1]
            + (force.direction[1] - force.origin[1])
            * force.intensity
            / (sqrt((force.origin[0] - force.direction[0]) ** 2 + (force.origin[1] - force.direction[1]) ** 2))
        ),
    )


def sum_forces(forces: List[Force]):
    final_origin = [0, 0]
    final_direction = [0, 0]
    final_intensity = 0
    for force in forces:
        final_origin[0] += force.origin[0]
        final_origin[1] += force.origin[1]
        final_direction[0] += force.direction[0]
        final_direction[1] += force.direction[1]
        final_intensity += force.intensity
    return Force((final_origin[0], final_origin[1]), (final_direction[0], final_direction[1]), final_intensity)
