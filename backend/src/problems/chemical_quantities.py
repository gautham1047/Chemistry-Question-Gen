"""Chemical Quantities problems (6-10)."""
import random
from src.problem_registry import problem, CHEMICAL_QUANTITIES
from src.problems._helpers import mole_conversions
from chemData import *
from src import *


@problem(6, "Molar Conversions", CHEMICAL_QUANTITIES)
def molar_conversions():
    myCompound = randomCmpd()
    name = myCompound.getName()
    if "/ " in name:
        name = name.split("/ ", 1)[1]
    startList = [" moles of ", " L of ", " particles of ", " atoms of ", " grams of "]
    endList = ["How many moles are in ", "What is the volume of ", "How many particles are in ", "How many atoms are in ", "What is the mass of "]
    moles = .25 * random.randint(1, 40)
    resultsList = mole_conversions(myCompound, moles)
    start = 1
    end = 1
    while start == end:
        start = random.randint(0, 4)
        end = random.randint(0, 4)

    question = endList[end] + str(resultsList[start]) + startList[start] + name
    return question, str(resultsList[end]) + " " + startList[end].split(" ", 2)[1]


@problem(7, "Calculate Percent Composition", CHEMICAL_QUANTITIES)
def percent_composition():
    myCompound = randomCmpd(3, 3, 3, 0, 0)
    compList = myCompound.percentComposition()
    question = "What is the percent composition of " + myCompound.getName()
    ans = ""
    for i in compList:
        ans += "\n" + i[0] + ": " + str(i[1])
    return question, ans


@problem(8, "Percent Composition to Equation", CHEMICAL_QUANTITIES)
def percent_comp_to_equation():
    myCompound = randomCmpd()
    compList = myCompound.percentComposition()
    mult = random.randint(1, 4)
    question = "What is molecular formula for a compound with a molar mass of " + str(mult * myCompound.getMolarMass()) + ", if the percent composition of the compound is: "
    percentComp = ""
    for i in compList:
        percentComp += "\n" + i[0] + ": " + str(i[1])
    question += percentComp
    myCompound.multCompound(mult)
    return question, myCompound.getEq()


@problem(9, "Mass of One Element in a Compound", CHEMICAL_QUANTITIES)
def mass_of_element_in_compound():
    myCompound = randomCmpd()
    mass = myCompound.getMass(.25 * random.randint(1, 8))
    elNum = random.randint(0, len(myCompound.compound) - 1)
    el = myCompound.compound[elNum][0]
    elMass = mass * myCompound.percentComposition()[elNum][1] / 100
    question = "What is the the mass of " + el + " in " + str(mass) + " g of " + myCompound.getName()
    return question, elMass


@problem(10, "Complex Percent Composition to Equation", CHEMICAL_QUANTITIES)
def complex_percent_comp_to_equation():
    myCompound = randomCmpd()
    compList = myCompound.percentComposition()
    mult = random.randint(1, 4)
    unit = "g"
    while unit == "g":
        value, unit, moles = randUnit(myCompound, mult)

    question = "How many " + unit + " are/is there in " + str(mult * myCompound.getMolarMass()) + " g of this compound, if the percent composition of the compound is: "
    percentComp = ""
    for i in compList:
        percentComp += "\n" + i[0] + ": " + str(round(i[1], 2)) + "%"
    question += percentComp
    return question, str(value) + " " + unit