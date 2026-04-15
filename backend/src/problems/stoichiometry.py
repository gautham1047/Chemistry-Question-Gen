"""Stoichiometry problems (13-14)."""
import random
from src.problem_registry import problem, STOICHIOMETRY
from chemData import *
from src import *


@problem(13, "Basic Stoichiometry", STOICHIOMETRY, accepts_rx_type=True)
def basic_stoichiometry(rx_type):
    rx = reaction(randomRx(rx_type))
    separatedCmpds = rx.formatRxList()
    cmpds = separatedCmpds[0] + separatedCmpds[1]
    startCmpd = random.choice(cmpds)
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
    question = printStr[0:-5] + ". "

    startList = [" moles of ", " L of ", " particles of ", " atoms of ", " grams of "]
    startMoles = .25 * random.randint(1, 40)
    resultsList = [startMoles, startMoles * 22.4, startMoles * 6.02e+23, startCmpd[0].getAtoms(startMoles), startCmpd[0].getMass(startMoles)]
    start = random.randint(0, 4)

    question += "There are " + str(resultsList[start]) + startList[start] + startCmpd[0].getNameFromEq() + "."

    finalCmpd = random.choice(cmpds)
    while finalCmpd[0] == startCmpd[0]:
        finalCmpd = random.choice(cmpds)
    finalCmpd[0].refresh()
    finalMoles = startMoles / startCmpd[1] * finalCmpd[1]
    endList = ["How many moles of ", "What is the volume of ", "How many particles of ", "How many atoms of ", "What is the mass of "]
    if finalCmpd in separatedCmpds[0]:
        end2List = [" are needed for ", " in ", " are needed for ", " are needed for ", " in "]
    else:
        end2List = [" are created in ", " in ", " are created in ", " are created in ", " in "]
    resultsList = [finalMoles, finalMoles * 22.4, finalMoles * 6.02e+23, finalCmpd[0].getAtoms(finalMoles), finalCmpd[0].getMass(finalMoles)]
    end = random.randint(0, 4)
    question += " " + endList[end] + str(finalCmpd[0].getNameFromEq()) + end2List[end] + "this reaction?"

    return question, str(resultsList[end]) + startList[end] + finalCmpd[0].equation


@problem(14, "Percent Yield/Limiting Reagent", STOICHIOMETRY, accepts_rx_type=True)
def percent_yield_limiting_reagent(rx_type):
    rx = reaction(randomRx(rx_type))
    separatedCmpds = rx.formatRxList()
    cmpds = separatedCmpds[0] + separatedCmpds[1]
    startCmpd = random.choice(separatedCmpds[0])
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
    for j, i in enumerate(reactants):
        if len(separatedCmpds) == 3 and j == 1:
            printStr += separatedCmpds[2] + " "
        printStr += i.getNameFromEq()
        printStr += " and "

    question = printStr[0:-5] + ". "

    startList = [" moles of ", " L of ", " particles of ", " atoms of ", " grams of "]
    startMoles = .25 * random.randint(1, 40)
    resultsList = [startMoles, startMoles * 22.4, startMoles * 6.02e+23, startCmpd[0].getAtoms(startMoles), startCmpd[0].getMass(startMoles)]
    start = random.randint(0, 4)

    question += "There are " + str(resultsList[start]) + startList[start] + startCmpd[0].getNameFromEq() + "."
    percentYeild = round(random.random(), 4)

    finalCmpd = random.choice(cmpds)
    while finalCmpd == startCmpd and not (finalCmpd in separatedCmpds[1] and startCmpd in separatedCmpds[1]):
        finalCmpd = random.choice(cmpds)
    finalCmpd[0].refresh()
    finalMoles = startMoles / startCmpd[1] * finalCmpd[1]
    percentYeildOrActualYield = random.randint(0, 1)
    percentYeildBool = False
    if finalCmpd in separatedCmpds[1]:
        percentYeildBool = True
    elif startCmpd in separatedCmpds[1]:
        percentYeildBool = True

    resultsList = [finalMoles, finalMoles * 22.4, finalMoles * 6.02e+23, finalCmpd[0].getAtoms(finalMoles), finalCmpd[0].getMass(finalMoles)]
    conversions = ["moles", "L", "particles", "atoms", "g"]
    end = random.randint(0, 4)

    if not percentYeildBool:
        trueFactor = round(.5 * random.random() + .75, 4)
        trueFinalMoles = finalMoles * trueFactor
        trueResultsList = [trueFinalMoles, trueFinalMoles * 22.4, trueFinalMoles * 6.02e+23, finalCmpd[0].getAtoms(trueFinalMoles), finalCmpd[0].getMass(trueFinalMoles)]
        trueEnd = random.randint(0, 4)
        try:
            lastCmpd = random.choice(separatedCmpds[1])
        except IndexError:
            pass
        if trueFinalMoles * startCmpd[1] > startMoles * finalCmpd[1]:
            lastMoles = startMoles / startCmpd[1] * lastCmpd[1]
        else:
            lastMoles = trueFinalMoles / finalCmpd[1] * lastCmpd[1]
        lastResultsList = [lastMoles, lastMoles * 22.4, lastMoles * 6.02e+23, lastCmpd[0].getAtoms(lastMoles), lastCmpd[0].getMass(lastMoles)]
        lastEnd = random.randint(0, 4)

        question += f" There are {trueResultsList[trueEnd]} {conversions[trueEnd]} of {finalCmpd[0].getNameFromEq()}. What is the limiting reageant, and how much {lastCmpd[0].getNameFromEq()} is there ({conversions[lastEnd]})?"
        if trueFactor > 1:
            limitingReagent = startCmpd[0].equation
            percentYeild = 1 / trueFactor
        else:
            limitingReagent = finalCmpd[0].equation
            percentYeild = trueFactor
        return question, f"Limiting reageant: {limitingReagent}. Theoretical Yeild: {round(lastResultsList[lastEnd], 4)} {conversions[lastEnd]} of {lastCmpd[0].getNameFromEq()}."
    elif percentYeildOrActualYield == 0:
        question += " The percent yeild is " + str(round(100 * percentYeild, 4)) + "%. What is the acutal yeild (" + conversions[end] + ") of " + finalCmpd[0].getNameFromEq() + "?"
        return question, str(round(resultsList[end] * percentYeild, 4)) + " " + conversions[end]
    else:
        question += " The actual yeild is " + str(round(resultsList[end] * percentYeild, 4)) + " " + conversions[end] + " of " + finalCmpd[0].getNameFromEq() + ". What is the percent yeild?"
        return question, str(round(100 * percentYeild, 4)) + "%"