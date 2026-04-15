"""Non-numbered helper functions."""
import random
from chemData import polyatomicIons


def polyatomic_ion_test(choices):
    """Standalone polyatomic ion quiz. Returns (question, answer)."""
    name = random.choice(choices)
    ion = polyatomicIons.get(name)
    charge = ion[-1]
    if ion != "NH4 1":
        charge = "-" + charge
    question = "What is the equation and charge of " + name + "?"
    answer = f"equation: {ion[:ion.index(' ')]}, charge: {charge}"
    return question, answer
