"""Nuclear Chemistry problems (73)."""
import random
from src.problem_registry import problem, NUCLEAR_CHEMISTRY
from chemData import *
from src import *


@problem(73, "Nuclear Decay", NUCLEAR_CHEMISTRY)
def nuclear_decay():
    protons = random.randint(88, 118)
    neutrons = neutronList[protons] + random.randint(-2, 2)
    particles = {"alpha particle": [4, 2], "beta particle": [0, -1], "positron": [0, 1], "proton": [1, 1], "neutron": [1, 0]}

    match random.randint(1, 6):
        case 1 | 2 | 3: numParticles = 1
        case 4 | 5: numParticles = 2
        case 6: numParticles = 3

    parts = []
    for _ in range(numParticles):
        while t := random.choice(list(particles)):
            if t not in parts: break
        parts.append(t)

    parities = [1 if bool(random.getrandbits(1)) else -1 for _ in range(numParticles)]

    newEl = [protons, neutrons]
    for parity, nums in zip(parities, parts):
        newEl[0] += parity * particles[nums][0]
        newEl[1] += parity * particles[nums][1]

    origElement = elements[protons][2] + "-" + str(neutrons)
    newElement = elements[newEl[0]][2] + "-" + str(newEl[1])

    words = [action + " emission" if i < 0 else action + " absorption" for action, i in zip(parts, parities)]
    question = f"A particle of {origElement} undergoes {' and '.join(words)}. What particle is created?"
    return question, newElement