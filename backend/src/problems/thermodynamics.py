"""Thermodynamics problems (63)."""
import random
from src.problem_registry import problem, THERMODYNAMICS
from chemData import *
from src import *

@problem(63, "More Thermodynamics", THERMODYNAMICS)
def more_thermodynamics():
    while rx := reaction(randomRx()):
        if rx.checkRxForThermo(): break

    choice = random.randint(0,2)
    chosen = ["enthalpy", "gibbs free energy", "entropy"][choice]

    data = [f"The {chosen} of {cmpd} is {thermoData.get(thermCompound(cmpd.equation + '(' + phase + ')'))[choice]}. " for cmpd, phase in zip(rx.allCompounds(), rx.phases)]

    question = f"Consider the reaction {rx.phaseStr()}. {''.join(data)}What is the {chosen} of the reaction?"
    return question, rx.thermoProfile(choice)
