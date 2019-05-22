from __future__ import annotations

import time
from abc import ABC
from typing import Tuple, Union, List, Any

import pygame

from lab import compute

Number = Union[int, float]


class Motherboard:
    def __init__(self, width: Number, height: Number):
        self.height = height
        self.width = width
        self._units: List[Unit] = []
        self._window = pygame.display.set_mode((self.width, self.height))

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
        while True:
            try:
                time.sleep(0.01)
                self.erase_units()
                for unit in self._units:
                    unit.run()
                self.render_units()
                pygame.display.flip()
            except KeyboardInterrupt:
                break


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

    def run(self):
        raise NotImplementedError


class MovableUnitMixin(Unit, ABC):
    def move_toward(self, direction: Tuple[Number, Number], distance: Number):
        self.position = compute(self.position, direction, distance)
