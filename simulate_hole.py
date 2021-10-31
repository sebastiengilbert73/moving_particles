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
    displayDelay
):
    logging.info("simulate_hole.py main()")

    # Create the particles
    particles_list = []
    for particle_ndx in range(numberOfParticles):
        color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
        part = Particle(color=color, position=(random.random(), random.random()))
        particles_list.append(part)

    UpdateAndDisplayArena(imageSizeHW, particles_list, displayDelay)

    for stepNdx in range(1, numberOfTimeSteps + 1):
        for p in particles_list:
            p.Move(method='random', sigma=0.01)
        UpdateAndDisplayArena(imageSizeHW, particles_list, displayDelay)


def UpdateAndDisplayArena(imageSizeHW, particles_list, displayDelay):
    arena_img = np.zeros((imageSizeHW[0], imageSizeHW[1], 3), dtype=np.uint8)
    for part in particles_list:
        (x, y) = ( round(part.position[0] * arena_img.shape[1]), round(part.position[1] * arena_img.shape[0] ))
        if x >= 0 and x < arena_img.shape[1] and y >= 0 and y < arena_img.shape[0]:
            arena_img[y, x] = part.color
    cv2.imshow("arena", arena_img)
    cv2.waitKey(displayDelay)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--numberOfParticles', help="The number of simulated particles. Default: 1000", type=int, default=1000)
    parser.add_argument('--imageSizeHW', help="The image size (height, width). Default: '(512, 512)'", default='(512, 512)')
    parser.add_argument('--numberOfTimeSteps', help="The number of time steps. Default: 100", type=int, default=100)
    parser.add_argument('--randomSeed', help="The random seed. Default 0", type=int, default=0)
    parser.add_argument('--displayDelay', help="The delay (in ms) for displaying the image. Default: 10", type=int, default=10)
    args = parser.parse_args()

    random.seed(args.randomSeed)
    imageSizeHW = ast.literal_eval(args.imageSizeHW)
    main(
        args.numberOfParticles,
        imageSizeHW,
        args.numberOfTimeSteps,
        args.displayDelay
    )