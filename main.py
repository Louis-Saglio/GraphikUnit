from __future__ import annotations

from typing import Tuple, Union, List, Any

import pygame

Number = Union[int, float]


class Motherboard:
    def __init__(self, width: Number, height: Number):
        self.height = height
        self.width = width
        self._units: List[Unit] = []
        self._window = pygame.display.set_mode((self.width, self.height))

    def add_unit(self, unit: Unit):
        self._units.append(unit)

    def render_units(self) -> None:
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

    def display(self):
        self.render_units()
        pygame.display.flip()


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


class MovableUnitMixin:
    def move_toward(self, x: Number, y: Number, distance: Number):
        pass
