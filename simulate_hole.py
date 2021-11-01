import logging
import argparse
import cv2
import numpy as np
import random
import ast
import math
from particle import Particle

logging.basicConfig(level=logging.DEBUG, format='%(asctime)-15s %(message)s')

def main(
    numberOfParticles,
    imageSizeHW,
    numberOfTimeSteps,
    displayDelay,
    moveMethod,
    moveRandomSigma,
    killRadius,
    monitoringRadius
):
    logging.info("simulate_hole.py main()")

    # Create the particles
    particles_list = []
    for particle_ndx in range(numberOfParticles):
        color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
        part = Particle(color=color, position=(random.random(), random.random()))
        particles_list.append(part)

    # Kill the particles in a given radius
    particles_list = KillParticles(particles_list, center=(0.5, 0.5), radius=killRadius)

    UpdateAndDisplayArena(imageSizeHW, particles_list, displayDelay, killRadius, monitoringRadius,
                          timestep=0)

    for stepNdx in range(1, numberOfTimeSteps + 1):
        for p in particles_list:
            if moveMethod == 'random':
                p.Move(method='random', sigma=moveRandomSigma)
            elif moveMethod == 'run_away_from_others':
                p.Move(method='run_away_from_others', sigma=moveRandomSigma, particles_list=particles_list, neighborhood_radius=0.03)
        UpdateAndDisplayArena(imageSizeHW, particles_list, displayDelay, killRadius, monitoringRadius,
                              timestep=stepNdx)


def UpdateAndDisplayArena(imageSizeHW, particles_list, displayDelay, kill_radius, monitoring_radius, timestep):
    arena_img = np.zeros((imageSizeHW[0], imageSizeHW[1], 3), dtype=np.uint8)
    center = (arena_img.shape[1]//2, arena_img.shape[0]//2)
    number_of_particles_in_monitoring_radius = 0
    for part in particles_list:
        (x, y) = ( round(part.position[0] * arena_img.shape[1]), round(part.position[1] * arena_img.shape[0] ))
        if x >= 0 and x < arena_img.shape[1] and y >= 0 and y < arena_img.shape[0]:
            arena_img[y, x] = part.color
        if math.sqrt((part.position[0] - 0.5)**2 + (part.position[1] - 0.5)**2) <= monitoring_radius:
            number_of_particles_in_monitoring_radius += 1

    cv2.circle(arena_img, center, round(kill_radius * arena_img.shape[1]), (0, 0, 255))
    cv2.circle(arena_img, center, round(monitoring_radius * arena_img.shape[1]),
               (255, 0, 0))
    cv2.putText(arena_img, "{}: {}".format(timestep, number_of_particles_in_monitoring_radius), (10, 30),
                cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 0, 0))
    cv2.imshow("arena", arena_img)
    cv2.waitKey(displayDelay)


def KillParticles(particles_list, center, radius):
    eliminated_particles = []
    for part in particles_list:
        distance = math.sqrt((part.position[0] - center[0])**2 + (part.position[1] - center[1])**2)
        if distance > radius:
            eliminated_particles.append(part)
    return eliminated_particles



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--numberOfParticles', help="The number of simulated particles. Default: 1000", type=int, default=1000)
    parser.add_argument('--imageSizeHW', help="The image size (height, width). Default: '(512, 512)'", default='(512, 512)')
    parser.add_argument('--numberOfTimeSteps', help="The number of time steps. Default: 300", type=int, default=300)
    parser.add_argument('--randomSeed', help="The random seed. Default 0", type=int, default=0)
    parser.add_argument('--displayDelay', help="The delay (in ms) for displaying the image. Default: 10", type=int, default=10)
    parser.add_argument('--moveMethod', help="The particle Move() method. Default: 'random'", default='random')
    parser.add_argument('--moveRandomSigma', help="The Move() random sigma, for move amplitude. Default: 0.01", type=float, default=0.01)
    parser.add_argument('--killRadius', help="The radius, around (0.5, 0.5) where all the particles are killed. Default: 0.2", type=float, default=0.2)
    parser.add_argument('--monitoringRadius', help="The radius within which we count the particles. Default: 0.1", type=float, default=0.1)
    args = parser.parse_args()

    random.seed(args.randomSeed)
    imageSizeHW = ast.literal_eval(args.imageSizeHW)
    main(
        args.numberOfParticles,
        imageSizeHW,
        args.numberOfTimeSteps,
        args.displayDelay,
        args.moveMethod,
        args.moveRandomSigma,
        args.killRadius,
        args.monitoringRadius
    )