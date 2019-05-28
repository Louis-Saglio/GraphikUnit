from math import sqrt
from random import randint, random
from typing import Tuple, List

from graphical_engine import Universe, GraphicalParticle
from lib import Number
from physics import Particle, Law, distance_between


class Atom(GraphicalParticle):
    def __init__(self, mass: Number, position: List[Number], velocity: List[Number]):
        super().__init__(mass, position, velocity)
        self._color = randint(0, 255), randint(0, 255), randint(0, 255)

    @property
    def color(self) -> Tuple[Number, Number, Number]:
        return self._color

    @property
    def dimensions(self) -> Tuple[Number, Number]:
        return 2, 2


def compute(origin, direction, intensity):
    return (
        (
            origin[0]
            + (direction[0] - origin[0])
            * intensity
            / (sqrt((origin[0] - direction[0]) ** 2 + (origin[1] - direction[1]) ** 2))
        ),
        (
            origin[1]
            + (direction[1] - origin[1])
            * intensity
            / (sqrt((origin[0] - direction[0]) ** 2 + (origin[1] - direction[1]) ** 2))
        ),
    )


class Gravity(Law):
    g = 0.1

    def compute_force(self, particle: Particle, other_particle: Particle) -> Tuple[Number, Number]:
        distance = distance_between(particle.position, other_particle.position)
        force = sqrt(self.g * particle.mass * other_particle.mass) / distance ** 2
        return (
            (other_particle.position[0] - particle.position[0]) * force / distance,
            (other_particle.position[1] - particle.position[1]) * force / distance,
        )


if __name__ == "__main__":
    universe = Universe()
    for _ in range(200):
        universe.add_unit(
            Atom(
                4,
                # [randint(-universe.width * 2, universe.width * 2), randint(-universe.height * 2, universe.height * 2)],
                [randint(-universe.width / 2, universe.width / 2), randint(-universe.height / 2, universe.height / 2)],
                [random() * - 0.5, random() - 0.5],
            )
        )
    universe.laws.append(Gravity())
    universe.loop()
