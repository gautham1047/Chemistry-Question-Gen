"""Chemical Reactions problems (11-12)."""
import random
from src.problem_registry import problem, CHEMICAL_REACTIONS
from src.problems._helpers import reaction_verb, reactant_name
from chemData import *
from src import *


@problem(11, "Solubility Rules", CHEMICAL_REACTIONS)
def solubility_rules():
    repeat = True
    cmpd = compound(getRandomCompound(5, 0, 1, 0, 0))
    while repeat or (cmpd.isSoluable() == "inconclusive"):
        repeat = False
        cmpd = compound(getRandomCompound(5, 0, 1, 0, 0))
        while type(cmpd.isSoluable()) != bool:
            cmpd = compound(getRandomCompound(5, 0, 1, 0, 0))
    question = f"Is {cmpd.equation} soluable?"
    if cmpd.isSoluable():
        ans = "yes"
    else:
        ans = "no"
    return question, ans


@problem(12, "Writing Chemical Equations", CHEMICAL_REACTIONS, accepts_rx_type=True)
def writing_chemical_equations(rx_type):
    rx = reaction(randomRx(rx_type))
    reactants = rx.SkeletonEquation()[0]
    printStr = reaction_verb(rx)
    for reactant in reactants:
        printStr += reactant_name(reactant, rx.balanceEq()) + " and "
    printStr = printStr[0:-5]

    question = printStr + ". What is the sum of the coefficients"
    coeffients = rx.balanceEq()
    sum = 0
    for i in coeffients:
        sum += i
    if "NR" in str(rx) and rx.typeRx in ["sr1", "sr2"]:
        sum = "n/a"
    return question, (str(rx) + "\nThe sum of the coefficients is " + str(sum))