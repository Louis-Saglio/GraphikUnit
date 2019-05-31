from math import sqrt
from random import randint, random
from typing import Tuple, List

from graphical_engine import Universe, GraphicalParticle
from physics import Particle, Law, distance_between, Number


class Atom(GraphicalParticle):
    def __init__(self, mass: Number, position: List[Number], velocity: List[Number]):
        super().__init__(mass, position, velocity)
        self._color = randint(0, 255), randint(0, 255), randint(0, 255)

    @property
    def color(self) -> Tuple[Number, Number, Number]:
        total_velocity = self.velocity[0] + self.velocity[1]
        return 255, min(abs((total_velocity + 1) ** 6), 255), min(abs((total_velocity + 1) ** 6), 255)

    @property
    def dimensions(self) -> Tuple[Number, Number]:
        dim = sqrt(self.mass + 1)
        return dim, dim


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
            total_mass = particle.mass + other_particle.mass
            p_share = particle.mass / total_mass
            o_share = other_particle.mass / total_mass
            other_particle.mass += particle.mass
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
    for _ in range(200):
        universe.add_unit(
            Atom(
                # 1,
                randint(1, 10) / 5,
                # [randint(-universe.width * 2, universe.width * 2), randint(-universe.height * 2, universe.height * 2)],
                # [0, 0],
                # [randint(-universe.width / 4, universe.width / 4), randint(-universe.height / 4, universe.height / 4)],
                # [randint(-universe.width, universe.width), randint(-universe.height, universe.height)],
                [randint(-universe.width / 2, universe.width / 2), randint(-universe.height / 2, universe.height / 2)],
                # [randint(-1, 1) / 500, randint(-1, 1) / 500],
                # [(random() - 0.5) * 1, (random() - 0.5) * 1],
                [-0.01, -0.01],
            )
        )
    # universe.add_unit(Atom(500, [100, 100], [0, 0]))
    # universe.add_unit(Atom(500, [-100, -100], [0, 0]))
    # universe.add_unit(Atom(500, [-100, 100], [0, 0]))
    # universe.add_unit(Atom(500, [100, -100], [0, 0]))
    # universe.add_unit(Atom(4000, [0, 0], [0, 0]))
    # universe.add_unit(Atom(1, [450, 200], [-0.05, -0.05]))
    # universe.add_unit(Atom(1, [900, 400], [-0.05, -0.05]))
    universe.laws.append(Gravity())
    universe.laws.append(Merge())
    universe.loop()
