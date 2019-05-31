from __future__ import annotations

import time
from tkinter import Tk
from typing import List, Tuple

import pygame

from physics import Particle, Law, Number


class GraphicalParticle(Particle):
    def __init__(self, universe: Universe, mass: Number, position: List[Number], velocity: List[Number]):
        super().__init__(mass, position, velocity)
        self.universe = universe
        self.old_graphical_position = [0, 0]
        self.present_graphical_position = [0, 0]

    @property
    def color(self) -> Tuple[Number, Number, Number]:
        raise NotImplementedError

    @property
    def dimensions(self) -> Tuple[Number, Number]:
        raise NotImplementedError

    @property
    def graphical_dimensions(self):
        return (
            max(1, self.dimensions[0] / self.universe.zoom_level),
            max(1, self.dimensions[1] / self.universe.zoom_level),
        )

    @property
    def graphical_position(self):
        self.old_graphical_position = self.present_graphical_position
        self.present_graphical_position = (
            (self.position[0] / self.universe.zoom_level + (self.universe.width / 2) - (self.dimensions[0] / 2)),
            (self.position[1] / self.universe.zoom_level + (self.universe.height / 2) - (self.dimensions[1] / 2)),
        )
        return self.present_graphical_position


class Universe:
    def __init__(
        self,
        width: Number = None,
        height: Number = None,
        zoom_level: Number = 1,
        draw_trajectory=False,
        sync_time=False,
    ):
        self.zoom_level = zoom_level  # 1 is normal, 2 is twice un-zoomed, 0.5 is twice zoomed
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
        for particle in self._units:
            if particle.is_alive or True:
                gd = particle.graphical_dimensions
                pygame.draw.rect(
                    self._window,
                    (0, 0, 0),
                    (
                        particle.old_graphical_position[0],
                        particle.old_graphical_position[1],
                        gd[0],
                        gd[1],
                    ),
                )

    def render_units(self) -> None:
        for particle in self._units:
            if particle.is_alive:
                gd = particle.graphical_dimensions
                pygame.draw.rect(
                    self._window,
                    particle.color,
                    (particle.graphical_position[0], particle.graphical_position[1], gd[0], gd[1]),
                    # there is a bug which makes caching particle.graphical_position in a variable
                    # which causes some dead particles be displayed
                )

    def apply_laws(self):
        for law in self.laws:
            for particle in self._units:
                if particle.is_alive:
                    for other_particle in self._units:
                        if other_particle.is_alive and particle != other_particle:
                            particle.apply_force(law.compute_force(particle, other_particle))

    def update_particle_positions(self):
        for unit in self._units:
            if unit.is_alive:
                unit.exist()

    def loop(self):
        run = True
        total_time = 0
        while run:
            try:
                if not self.draw_trajectory:
                    self.erase_units()
                self.render_units()
                self.apply_laws()
                self.update_particle_positions()

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                total_time += 1
                if self.sync_time:
                    time.sleep(0.01)

            except KeyboardInterrupt:
                run = False
