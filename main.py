# todo : make Merge law depend on particle dimensions (maybe not good idea)
# todo : make color of merged particles be the color of the biggest one
# todo : zoom during execution


from math import sqrt
from random import randint, random
from typing import Tuple, List, Callable

from graphical_engine import Universe, GraphicalParticle
from physics import Particle, Law, distance_between, Number


class Atom(GraphicalParticle):
    color_options = {
        "dynamic": lambda self: (
            255,
            min(abs((self.velocity[0] + self.velocity[1] + 1) ** 6), 255),
            min(abs((self.velocity[0] + self.velocity[1] + 1) ** 6), 255),
        ),
        "random": lambda self: self._color,
    }

    def __init__(
        self, universe: Universe, mass: Number, position: List[Number], velocity: List[Number], color_option="random"
    ):
        super().__init__(universe, mass, position, velocity)
        self.color_option = color_option
        if self.color_option == "random":
            self._color = randint(0, 255), randint(0, 255), randint(0, 255)

    @property
    def color(self) -> Tuple[Number, Number, Number]:
        return self.color_options[self.color_option](self)

    @property
    def dimension(self) -> Number:
        return sqrt(self.mass)


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


def main(
    particle_nbr: Number,
    special_particles: Callable[..., List[GraphicalParticle]],
    particles_init_mass: Callable[..., Number],
    particles_init_position_range: Callable[[Universe], List[Number]],
    particles_init_velocity: Callable[..., List[Number]],
    laws: List[Law],
    draw_trajectory: bool,
    sync_time: bool,
    zoom_level: Number,
):
    universe = Universe(zoom_level=zoom_level, draw_trajectory=draw_trajectory, sync_time=sync_time)
    for _ in range(particle_nbr):
        universe.add_unit(
            Atom(universe, particles_init_mass(), particles_init_position_range(universe), particles_init_velocity())
        )
    for particle in special_particles(universe):
        universe.add_unit(particle)
    for law in laws:
        universe.laws.append(law)
    universe.loop()


options = {
    "mass": {"1": lambda: 1, "1to10": lambda: randint(1, 10)},
    "position": {
        "in_screen": lambda u: [randint(-u.width / 2, u.width / 2), randint(-u.height / 2, u.height / 2)],
        "in_twice_screen": lambda u: [randint(-u.width, u.width), randint(-u.height, u.height)],
        "in_half_screen": lambda u: [randint(-u.width / 4, u.width / 4), randint(-u.height / 4, u.height / 4)],
        "in_2_3rd_of_screen": lambda u: [randint(-u.width / 3, u.width / 3), randint(-u.height / 3, u.height / 3)],
    },
    "velocity": {
        "0": lambda: [0, 0],
        "-0.01": lambda: [-0.01, -0.01],
        "rand_0.5": lambda: [(random() - 0.5), (random() - 0.5)],
        "rand_0.002": lambda: [randint(-1, 1) / 500, randint(-1, 1) / 500],
    },
    "special_particles": {
        "centered_big_star": lambda u: [Atom(u, 4000, [0, 0], [0, 0])],
        "none": lambda u: [],
        "centered_small_star": lambda u: [Atom(u, 4000, [0, 0], [0, 0])],
        "four_star": lambda u: [
            Atom(u, 500, [100, 100], [0, 0]),
            Atom(u, 500, [-100, 100], [0, 0]),
            Atom(u, 500, [100, -100], [0, 0]),
            Atom(u, 500, [-100, -100], [0, 0]),
        ],
    },
    "laws": {"realistic": [Gravity(), Merge()], "pure_gravity": [Gravity()]},
}


if __name__ == "__main__":
    main(
        100,
        options["special_particles"]["none"],
        options["mass"]["1"],
        options["position"]["in_screen"],
        options["velocity"]["0"],
        # options["velocity"]["rand_0.5"],
        options["laws"]["realistic"],
        draw_trajectory=False,
        sync_time=False,
        zoom_level=1,
    )
