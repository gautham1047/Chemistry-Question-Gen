"""Math Review problems (1)."""
import random
from src.problem_registry import problem, MATH_REVIEW
from chemData import *
from src import *


@problem(1, "SI Units", MATH_REVIEW)
def si_units():
    powers = [(unit, random.randint(-2, 3)) for unit in units]
    for i in powers:
        if i[1] == 0:
            powers.remove(i)
    start = [random.choice(list(prefixNumbers.keys())) for _ in powers]
    end = [random.choice(list(prefixNumbers.keys())) for _ in powers]

    startStr = ""
    startNum = 0
    for s, power in zip(start, powers):
        unit, p = power
        startNum += p * s
        startStr += prefixNumbers.get(s) + unit + "^" + str(p) + " "

    endStr = ""
    endNum = 0
    for e, power in zip(end, powers):
        unit, p = power
        endNum += p * e
        endStr += prefixNumbers.get(e) + unit + "^" + str(p) + " "

    question = "Start: " + startStr + "\nEnd: " + endStr + "\nYou have to multiply the start by 10^x, to get to the final unit. What is x?"
    finalFactor = startNum - endNum
    return question, finalFactor
