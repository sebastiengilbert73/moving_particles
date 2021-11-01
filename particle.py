import math
import random
import numpy as np

class Particle:
    def __init__(self, color, position=np.array([0., 0.]), speed=np.array([0., 0.]), gamma=0.9):
        self.position = position
        self.speed = speed
        self.gamma = gamma
        self.color = color

    def Move(self, method='random', **kwargs):
        if method == 'random':
            sigma = kwargs['sigma']
            speed = self.gamma * self.speed +  (1 - self.gamma) * sigma * np.random.randn(2)
            self.position += speed
            self.speed = speed
        elif method == 'run_away_from_others':
            neighborhood_radius = kwargs['neighborhood_radius']
            particles_list = kwargs['particles_list']
            sigma = kwargs['sigma']
            neighbors_list = []
            unit_vector = None
            for other_particle in particles_list:
                distance = math.sqrt((other_particle.position[0] - self.position[0])**2 + (other_particle.position[1] - self.position[1])**2)
                if distance > 0 and distance <= neighborhood_radius:
                    neighbors_list.append(other_particle)
            if len(neighbors_list) == 0:
                theta = 2 * math.pi * random.random()
                unit_vector = np.array([math.cos(theta), math.sin(theta)])
            else:
                sum_x = 0
                sum_y = 0
                for neighbor in neighbors_list:
                    sum_x += neighbor.position[0] - self.position[0]
                    sum_y += neighbor.position[1] - self.position[1]
                unit_vector = [-sum_x/len(neighbors_list), -sum_y/len(neighbors_list)]
                unit_vector = 1.0 / math.sqrt(unit_vector[0]**2 + unit_vector[1]**2) * np.array(unit_vector)
            speed = self.gamma * self.speed + (1 - self.gamma) * sigma * unit_vector
            self.position += speed
            self.speed = speed
        else:
            raise NotImplementedError("Particle.Move(): Not implemented method '{}'".format(method))

def NumberOfParticlesInsideRadius(particles_list, monitoring_radius):
    number_of_particles_in_monitoring_radius = 0
    for part in particles_list:
        if math.sqrt((part.position[0] - 0.5)**2 + (part.position[1] - 0.5)**2) <= monitoring_radius:
            number_of_particles_in_monitoring_radius += 1
    return number_of_particles_in_monitoring_radius