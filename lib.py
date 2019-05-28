from __future__ import annotations

from abc import ABC
from math import sqrt
from tkinter import Tk
from typing import Any, Iterable
from typing import Tuple, Union, List

import pygame

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
        return (self.intensity, self.direction, self.origin == other.intensity, other.direction, other.origin)


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


class Motherboard:
    def __init__(self, width: Number = None, height: Number = None):
        if width is None or height is None:
            screen = Tk()
        self.height = height or screen.winfo_screenheight()
        self.width = width or screen.winfo_screenwidth()
        self._units: List[Unit] = []
        self._window = pygame.display.set_mode((self.width, self.height))
        self.laws: List[Law] = []

    def add_unit(self, unit: Unit):
        self._units.append(unit)

    def erase_units(self) -> None:
        for unit in self._units:
            pygame.draw.rect(
                self._window,
                (0, 0, 0),
                (
                    unit.position[0] + (self._window.get_width() / 2) - (unit.dimensions[0] / 2),
                    unit.position[1] + (self._window.get_height() / 2) - (unit.dimensions[1] / 2),
                    unit.dimensions[0],
                    unit.dimensions[1],
                ),
            )

    def render_units(self) -> None:
        for unit in self._units:
            pygame.draw.rect(
                self._window,
                unit.color,
                (
                    unit.position[0] + (self._window.get_width() / 2) - (unit.dimensions[0] / 2),
                    unit.position[1] + (self._window.get_height() / 2) - (unit.dimensions[1] / 2),
                    unit.dimensions[0],
                    unit.dimensions[1],
                ),
            )

    def loop(self):
        run = True
        total_time = 0
        while run:
            try:
                # time.sleep(0.01)
                self.erase_units()
                for unit in self._units:
                    unit.run(total_time)
                for law in self.laws:
                    law.apply(self._units)
                self.render_units()
                if total_time % 3 == 0:
                    pygame.display.flip()
                # pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                total_time += 1
            except KeyboardInterrupt:
                run = False


class Unit:
    @property
    def position(self) -> Tuple[Number, Number]:
        raise NotImplementedError

    @property
    def dimensions(self) -> Tuple[Number, Number]:
        raise NotImplementedError

    @property
    def color(self) -> Any:
        raise NotImplementedError

    def run(self, total_time: int, **kwargs):
        raise NotImplementedError

    @position.setter
    def position(self, value):
        raise NotImplementedError

    def distance_with(self, other: Unit):
        return sqrt((self.position[0] - other.position[0]) ** 2 + (self.position[1] - other.position[1]) ** 2)


class Law:
    def apply(self, units: Iterable[Unit]):
        raise NotImplementedError


class MovableUnitMixin(Unit, ABC):
    def move_toward(self, direction: Tuple[Number, Number], distance: Number):
        self.position = compute(Force(self.position, direction, distance))
