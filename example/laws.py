from typing import Tuple

from physics import Law, Particle, Number
from utils import distance_between


class Merge(Law):
    UMD = 3  # universal minimum distance

    def compute_force(self, particle: Particle, other_particle: Particle) -> Tuple[Number, Number]:
        if distance_between(particle.position, other_particle.position) < self.UMD:
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
