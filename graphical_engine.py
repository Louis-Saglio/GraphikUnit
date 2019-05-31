import time
from tkinter import Tk
from typing import List, Tuple

import pygame

from physics import Particle, Law, Number


class GraphicalParticle(Particle):
    @property
    def color(self) -> Tuple[Number, Number, Number]:
        raise NotImplementedError

    @property
    def dimensions(self) -> Tuple[Number, Number]:
        raise NotImplementedError


class Universe:
    def __init__(self, width: Number = None, height: Number = None, draw_trajectory=False, sync_time=False):
        self.sync_time = sync_time
        self.draw_trajectory = draw_trajectory
        if width is None or height is None:
            screen = Tk()
        self.height = height or screen.winfo_screenheight()
        self.width = width or screen.winfo_screenwidth()
        self._units: List[GraphicalParticle] = []
        self._window = pygame.display.set_mode((self.width, self.height))
        self.laws: List[Law] = []

    def add_unit(self, particle: GraphicalParticle):
        self._units.append(particle)

    def erase_units(self) -> None:
        for unit in self._units:
            if unit.is_alive:
                unit_x = unit.position[0] + (self.width / 2) - (unit.dimensions[0] / 2)
                unit_y = unit.position[1] + (self.height / 2) - (unit.dimensions[1] / 2)
                pygame.draw.rect(self._window, (0, 0, 0), (unit_x, unit_y, unit.dimensions[0], unit.dimensions[1]))

    def render_units(self) -> None:
        for unit in self._units:
            if unit.is_alive:
                unit_x = unit.position[0] + (self.width / 2) - (unit.dimensions[0] / 2)
                unit_y = unit.position[1] + (self.height / 2) - (unit.dimensions[1] / 2)
                pygame.draw.rect(self._window, unit.color, (unit_x, unit_y, unit.dimensions[0], unit.dimensions[1]))

    def loop(self):
        run = True
        total_time = 0
        while run:
            try:
                if self.sync_time:
                    time.sleep(0.01)
                if not self.draw_trajectory:
                    self.erase_units()
                for unit in self._units:
                    if unit.is_alive:
                        unit.exist()
                for law in self.laws:
                    for particle in self._units:
                        if particle.is_alive:
                            for other_particle in self._units:
                                if other_particle.is_alive and particle != other_particle:
                                    particle.apply_force(law.compute_force(particle, other_particle))
                self.render_units()
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                total_time += 1
            except KeyboardInterrupt:
                run = False
