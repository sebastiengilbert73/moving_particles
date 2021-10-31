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
            theta = 2 * math.pi * random.random()
            sigma = kwargs['sigma']
            speed = self.gamma * self.speed +  (1 - self.gamma) * sigma * np.random.randn(2)
            self.position += speed
            self.speed = speed
        else:
            raise NotImplementedError("Particle.Move(): Not implemented method '{}'".format(method))

