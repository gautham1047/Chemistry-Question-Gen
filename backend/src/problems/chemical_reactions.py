"""Chemical Reactions problems (11-12)."""
import random
from src.problem_registry import problem, CHEMICAL_REACTIONS
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
    printStr = ["Combine ", "Decompose ", "Combust ", "Completely Combust ", "Incompletley Combust ", "Write the reaction between "]
    if rx.typeRx in ["s1", "s2", "s3"]:
        printStr = printStr[0]
    elif rx.typeRx in ["d1", "d2", "d3"]:
        printStr = printStr[1]
    elif rx.typeRx == "c":
        printStr = printStr[2]
    elif rx.typeRx == "complete combustion":
        printStr = printStr[3]
    elif rx.typeRx == "incomplete combustion":
        printStr = printStr[4]
    else:
        printStr = printStr[5]
    for reactant in reactants:
        reactantName = reactant.getNameFromEq()
        coeffientList = rx.balanceEq()
        if reactantName == "nitric acid":
            if coeffientList in [[3, 8, 3, 2, 4], [8, 3, 3, 2, 4]]:
                reactantName = "dilute nitric acid"
            elif coeffientList in [[4, 1, 1, 2, 2], [1, 4, 1, 2, 2]]:
                reactantName = "concentrated nitric acid"
        printStr += reactantName + " and "
    printStr = printStr[0:-5]

    question = printStr + ". What is the sum of the coefficients"
    coeffients = rx.balanceEq()
    sum = 0
    for i in coeffients:
        sum += i
    if "NR" in str(rx) and rx.typeRx in ["sr1", "sr2"]:
        sum = "n/a"
    return question, (str(rx) + "\nThe sum of the coefficients is " + str(sum))