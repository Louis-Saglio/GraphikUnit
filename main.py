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
        return sqrt(self.mass), sqrt(self.mass)


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


class Merge(Law):
    def compute_force(self, particle: Particle, other_particle: Particle) -> Tuple[Number, Number]:
        if distance_between(particle.position, other_particle.position) < 3:
            particle.is_alive = False
            other_particle.mass += particle.is_alive
            total_mass = particle.mass + other_particle.mass
            p_share = particle.mass / total_mass
            o_share = other_particle.mass / total_mass
            other_particle.velocity = [
                particle.velocity[0] * p_share + other_particle.velocity[0] * o_share,
                particle.velocity[1] * p_share + other_particle.velocity[1] * o_share,
            ]
            return 0, 0
        return 0, 0


class Gravity(Law):
    g = 0.1

    def compute_force(self, particle: Particle, other_particle: Particle) -> Tuple[Number, Number]:
        distance = distance_between(particle.position, other_particle.position)
        force = self.g * particle.mass * other_particle.mass / distance ** 2
        return (
            (other_particle.position[0] - particle.position[0]) * force / distance,
            (other_particle.position[1] - particle.position[1]) * force / distance,
        )


if __name__ == "__main__":
    universe = Universe()
    for _ in range(500):
        universe.add_unit(
            Atom(
                1,
                # randint(1, 10) / 10,
                # [randint(-universe.width * 2, universe.width * 2), randint(-universe.height * 2, universe.height * 2)],
                # [randint(-universe.width / 3, universe.width / 3), randint(-universe.height / 3, universe.height / 3)],
                [randint(-universe.width / 2, universe.width / 2), randint(-universe.height / 2, universe.height / 2)],
                [randint(-1, 1) / 30, randint(-1, 1) / 30],
                # [random() * - 0.5, random() - 0.5],
            )
        )
    # universe.add_unit(Atom(30, [0, 0], [0, 0]))
    universe.laws.append(Gravity())
    universe.laws.append(Merge())
    universe.loop()
