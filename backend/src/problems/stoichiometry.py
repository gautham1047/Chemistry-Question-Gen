"""Stoichiometry problems (13-14)."""
import random
from src.problem_registry import problem, STOICHIOMETRY
from src.problems._helpers import reaction_verb, mole_conversions, reactant_name
from chemData import *
from src import *


@problem(13, "Basic Stoichiometry", STOICHIOMETRY, accepts_rx_type=True)
def basic_stoichiometry(rx_type):
    rx = reaction(randomRx(rx_type))
    reactants = rx.reactants()
    products = rx.products()
    cmpds = reactants + products
    startCmpd = random.choice(cmpds)
    printStr = reaction_verb(rx)
    for cmpd, _ in reactants:
        printStr += reactant_name(cmpd, rx.balanceEq()) + " and "
    question = printStr[0:-5] + ". "

    startList = [" moles of ", " L of ", " particles of ", " atoms of ", " grams of "]
    startMoles = .25 * random.randint(1, 40)
    resultsList = mole_conversions(startCmpd[0], startMoles)
    start = random.randint(0, 4)

    question += "There are " + str(resultsList[start]) + startList[start] + startCmpd[0].getName() + "."

    finalCmpd = random.choice(cmpds)
    while finalCmpd[0] == startCmpd[0]:
        finalCmpd = random.choice(cmpds)
    finalMoles = startMoles / startCmpd[1] * finalCmpd[1]
    endList = ["How many moles of ", "What is the volume of ", "How many particles of ", "How many atoms of ", "What is the mass of "]
    if finalCmpd in reactants:
        end2List = [" are needed for ", " in ", " are needed for ", " are needed for ", " in "]
    else:
        end2List = [" are created in ", " in ", " are created in ", " are created in ", " in "]
    resultsList = mole_conversions(finalCmpd[0], finalMoles)
    end = random.randint(0, 4)
    question += " " + endList[end] + str(finalCmpd[0].getName()) + end2List[end] + "this reaction?"

    return question, str(resultsList[end]) + startList[end] + finalCmpd[0].equation


@problem(14, "Percent Yield/Limiting Reagent", STOICHIOMETRY, accepts_rx_type=True)
def percent_yield_limiting_reagent(rx_type):
    rx = reaction(randomRx(rx_type))
    reactants = rx.reactants()
    products = rx.products()
    cmpds = reactants + products
    startCmpd = random.choice(reactants)

    printStr = reaction_verb(rx)
    for j, (cmpd, _) in enumerate(reactants):
        if rx.typeRx == "special" and j == 1:
            printStr += rx.misc[2] + " "
        printStr += cmpd.getName()
        printStr += " and "

    question = printStr[0:-5] + ". "

    startList = [" moles of ", " L of ", " particles of ", " atoms of ", " grams of "]
    startMoles = .25 * random.randint(1, 40)
    resultsList = mole_conversions(startCmpd[0], startMoles)
    start = random.randint(0, 4)

    question += "There are " + str(resultsList[start]) + startList[start] + startCmpd[0].getName() + "."
    percentYeild = round(random.random(), 4)

    finalCmpd = random.choice(cmpds)
    while finalCmpd == startCmpd and not (finalCmpd in products and startCmpd in products):
        finalCmpd = random.choice(cmpds)
    finalMoles = startMoles / startCmpd[1] * finalCmpd[1]
    percentYeildOrActualYield = random.randint(0, 1)
    percentYeildBool = False
    if finalCmpd in products:
        percentYeildBool = True
    elif startCmpd in products:
        percentYeildBool = True

    resultsList = mole_conversions(finalCmpd[0], finalMoles)
    conversions = ["moles", "L", "particles", "atoms", "g"]
    end = random.randint(0, 4)

    if not percentYeildBool:
        trueFactor = round(.5 * random.random() + .75, 4)
        trueFinalMoles = finalMoles * trueFactor
        trueResultsList = mole_conversions(finalCmpd[0], trueFinalMoles)
        trueEnd = random.randint(0, 4)
        try:
            lastCmpd = random.choice(products)
        except IndexError:
            pass
        if trueFinalMoles * startCmpd[1] > startMoles * finalCmpd[1]:
            lastMoles = startMoles / startCmpd[1] * lastCmpd[1]
        else:
            lastMoles = trueFinalMoles / finalCmpd[1] * lastCmpd[1]
        lastResultsList = mole_conversions(lastCmpd[0], lastMoles)
        lastEnd = random.randint(0, 4)

        question += f" There are {trueResultsList[trueEnd]} {conversions[trueEnd]} of {finalCmpd[0].getName()}. What is the limiting reageant, and how much {lastCmpd[0].getName()} is there ({conversions[lastEnd]})?"
        if trueFactor > 1:
            limitingReagent = startCmpd[0].equation
            percentYeild = 1 / trueFactor
        else:
            limitingReagent = finalCmpd[0].equation
            percentYeild = trueFactor
        return question, f"Limiting reageant: {limitingReagent}. Theoretical Yeild: {round(lastResultsList[lastEnd], 4)} {conversions[lastEnd]} of {lastCmpd[0].getName()}."
    elif percentYeildOrActualYield == 0:
        question += " The percent yeild is " + str(round(100 * percentYeild, 4)) + "%. What is the acutal yeild (" + conversions[end] + ") of " + finalCmpd[0].getName() + "?"
        return question, str(round(resultsList[end] * percentYeild, 4)) + " " + conversions[end]
    else:
        question += " The actual yeild is " + str(round(resultsList[end] * percentYeild, 4)) + " " + conversions[end] + " of " + finalCmpd[0].getName() + ". What is the percent yeild?"
        return question, str(round(100 * percentYeild, 4)) + "%"