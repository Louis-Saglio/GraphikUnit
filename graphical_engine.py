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
    def dimension(self) -> Number:
        raise NotImplementedError

    @property
    def graphical_dimension(self):
        return max(1, self.dimension / self.universe.zoom_level)

    @property
    def graphical_position(self):
        self.old_graphical_position = self.present_graphical_position
        self.present_graphical_position = (
            (self.position[0] / self.universe.zoom_level) + (self.universe.width / 2),
            (self.position[1] / self.universe.zoom_level) + (self.universe.height / 2),
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
                gd = round(particle.graphical_dimension)
                pygame.draw.circle(
                    self._window,
                    (0, 0, 0),
                    (round(particle.old_graphical_position[0]), round(particle.old_graphical_position[1])),
                    gd,
                    gd,
                )

    def render_units(self) -> None:
        for particle in self._units:
            if particle.is_alive:
                gp = particle.graphical_position
                pygame.draw.circle(
                    self._window,
                    particle.color,
                    (round(gp[0]), round(gp[1])),
                    round(particle.graphical_dimension),
                    round(particle.graphical_dimension),
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
                #
                # if total_time % 5000 == 0:
                #     self.zoom_level += 1

            except KeyboardInterrupt:
                run = False
        print(total_time)
