"""Chemical Nomenclature problems (2-5)."""
import random
from src.problem_registry import problem, CHEMICAL_NOMENCLATURE
from chemData import *
from src import *


@problem(2, "Average atomic mass", CHEMICAL_NOMENCLATURE)
def average_atomic_mass():
    indexAverageMass = random.randint(0, 100) + random.random()
    isotopeList = []

    for i in range(0, 5):
        newIsotope = round(indexAverageMass - i + (random.random() / 50), 3)
        isotopeList.append(newIsotope)

    relativeAdundanceList = []
    for i in range(0, 5):
        newRelativeAdundance = random.randint(0, 100)
        relativeAdundanceList.append(newRelativeAdundance)
    s = 0
    for i in relativeAdundanceList:
        s = s + i
    newRelativeAdundanceList = []
    for i in relativeAdundanceList:
        i = round(100 * i / s, 2)
        newRelativeAdundanceList.append(i)

    for i in newRelativeAdundanceList:
        s = s + i

    if s != 100:
        sum = 0
        for i in newRelativeAdundanceList:
            sum = sum + i
        newRelativeAdundanceDifference = 100 - sum + newRelativeAdundanceList[4]
        newRelativeAdundanceList[4] = round(newRelativeAdundanceDifference, 2)

    lines = ["Isotopes: \n\n   Mass     Abdundance"]
    totalMass = 0
    for i, isotope in enumerate(isotopeList):
        lines.append(str(i + 1) + ". " + str(isotope) + "    " + str(newRelativeAdundanceList[i]))
        totalMass = totalMass + round(isotope * newRelativeAdundanceList[i], 2)
    averageMass = round(totalMass / 100, 2)
    lines.append("\nWhat is the average atomic mass of this element?")

    return "\n".join(lines), averageMass


@problem(3, "Missing Isotope Percentage", CHEMICAL_NOMENCLATURE)
def missing_isotope_percentage():
    percentageOne = round(100 * random.random(), 0)
    percentageTwo = 100 - percentageOne
    massOne = round(100 * random.random(), 2)
    massTwo = round(massOne + 2 * (0.5 - random.randint(0, 1)) + .5 * random.random(), 2)
    averageMass = round((massOne * percentageOne + massTwo * percentageTwo) / 100, 2)
    question = "Find the relative abundance of isotope A, which is " + str(massOne) + " amu, when the mass of isotope B is " + str(massTwo) + " amu, and the average atomic mass is " + str(averageMass)
    return question, percentageOne


@problem(4, "Formula to Name", CHEMICAL_NOMENCLATURE)
def formula_to_name():
    myCompound = randomCmpd()
    name = myCompound.getName()
    if "/ " in name:
        name = name.split("/", 1)[1]
    question = "What is the equation for " + name
    return question, myCompound.equation


@problem(5, "Name to Formula", CHEMICAL_NOMENCLATURE)
def name_to_formula():
    myCompound = randomCmpd()
    question = "What is the name of " + myCompound.equation
    return question, myCompound.name