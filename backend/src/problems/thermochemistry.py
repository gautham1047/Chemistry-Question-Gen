"""Thermochemistry problems (15-17)."""
import random
from src.problem_registry import problem, THERMOCHEMISTRY
from src.problems._helpers import reaction_verb, mole_conversions, reactant_name
from chemData import *
from src import *


@problem(15, "Heat of Physical Change", THERMOCHEMISTRY)
def heat_of_physical_change():
    water = bool(random.getrandbits(1))
    water = False
    if water:
        cmpd = compound("H2O")
    else:
        cmpd = compound(random.choice(list(heatOfPhysicalChanges.keys())))
    fp, bp, heatOfFusion, heatOfVaporization, sSpecificHeat, lSpecificHeat, gSpecificHeat = heatOfPhysicalChanges.get(cmpd.equation)
    startTemp = random.randint(-100, 150)
    try:
        if cmpd.equation == "H2O":
            lowerBound = max(startTemp - 100, -273)
            upperBound = startTemp + 100
        elif cmpd.equation in ["CH3COCH3", "NH3", "C6H6", "C2H5OH", "CH3OH"]:
            lowerBound = max(startTemp - 100, fp)
            upperBound = startTemp + 100
        else:
            lowerBound = max(startTemp - 100, bp)
            upperBound = startTemp + 100
        finalTemp = random.randint(int(lowerBound), upperBound)
    except:
        raise Exception(f"Error with getting final temperature. \nstartTemp: {startTemp}\ncmpd: {cmpd.equation}")

    shString = "A"
    if cmpd.equation == "H2O":
        shString += "s a solid, the specific heat is " + str(sSpecificHeat) + ", and a"
    if cmpd.equation in ["H2O", "CH3COCH3", "NH3", "C6H6", "C2H5OH", "CH3OH"]:
        shString += "s a liquid, the specific heat is " + str(lSpecificHeat) + ", and a"
    shString += "s a gas, the specific heat is " + str(gSpecificHeat) + "."

    moles = .25 * random.randint(1, 40)
    cmpd.setTemp(startTemp)
    heat = cmpd.raiseTemp(finalTemp, moles, fp, bp, heatOfFusion, heatOfVaporization, sSpecificHeat, lSpecificHeat, gSpecificHeat)
    if finalTemp > startTemp:
        strVar1 = "heated"
        strVar2 = "must be supplied"
    else:
        strVar1 = "cooled"
        strVar2 = "is released"

    choice = random.randint(0, 4)
    unitsArr = ["moles", "L", "particles", "atoms", "g"]
    choices = mole_conversions(cmpd, moles)
    question = f"If {choices[choice]} {unitsArr[choice]} of {cmpd.name} is {strVar1} from {startTemp} C to {finalTemp} C, how much heat {strVar2}? {shString}"
    return question, str(abs(heat)) + " kJ"


@problem(16, "Coffee Cup Calorimetry", THERMOCHEMISTRY)
def coffee_cup_calorimetry():
    metals = list(specificHeats.keys())[5:]
    metals.remove("mercury")
    metal1 = random.choice(metals)
    metals.remove(metal1)
    m2Exists = random.getrandbits(1)
    metal2 = random.choice(metals)
    metals.remove(metal2)
    cExists = random.getrandbits(1)
    container = random.choice(metals)

    tempMetals = random.randint(50, 150)
    m1Mass = random.randint(10, 50)
    m2Mass = m2Exists * random.randint(10, 50)
    m1SH = specificHeats.get(metal1)
    m2SH = m2Exists * specificHeats.get(metal2)

    tempWater = random.randint(20, 40)
    wMass = random.randint(25, 100)
    wSH = 4.18
    cMass = cExists * random.randint(100, 1000)
    cSH = cExists * specificHeats.get(container)

    Cm = m1Mass * m1SH + m2Mass * m2SH
    Cw = wMass * wSH + cMass * cSH

    finalTemp = round((Cm * tempMetals + Cw * tempWater) / (Cm + Cw), 4)

    options = [f"The mass of {metal1} is {m1Mass} g", f"(c = {m1SH})", ". "]
    answers = [m1Mass, m1SH, -1]
    if m2Exists:
        options.extend([f"The mass of {metal2} is {m2Mass} g", f"(c = {m2SH})", ". "])
        answers.extend([m2Mass, m2SH, -1])
    options.extend([f"The mass of water is {wMass} g", ". "])
    answers.extend([wMass, -1])
    if cExists:
        options.extend([f"The mass of the {container} container is {cMass} g", f"(c = {cSH})", ". "])
        answers.extend([cMass, cSH, -1])

    options.extend([f"The initial temperature of the metal(s) is {tempMetals} C.", f"The intial temperature of the water is {tempWater} C.", f"The final temperature is {finalTemp} C."])
    answers.extend([tempMetals, tempWater, finalTemp])

    missing = -1
    while missing == -1:
        missingNum = random.randint(0, len(answers) - 1)
        missing = answers[missingNum]
    if "(c = " in options[missingNum]:
        missingQ = "What is the specific heat of the " + options[missingNum - 1].split(" ")[-4]
        options.pop(missingNum)
    elif "The mass of " in options[missingNum]:
        missingQ = "What is " + " ".join(options[missingNum].lower().split(" ")[:-3])
        options[missingNum] = "Some " + options[missingNum].lower().split(" ")[3] + " is added to the calorimeter"
    else:
        missingQ = "What is " + " ".join(options.pop(missingNum).lower().split(" ")[:-3])
    question = ""
    for i in options:
        question += i + " "
    question = question.replace(" .", ".")
    question = question.replace("..", ".")
    question = question.replace("  ", " ")
    question += missingQ + "?"
    return question, missing


@problem(17, "Bomb Calorimetry", THERMOCHEMISTRY, accepts_rx_type=True)
def bomb_calorimetry(rx_type):
    rx = randomRx(rx_type)
    reactants = rx.reactants()
    products = rx.products()

    printStr = reaction_verb(rx)

    heatList = []
    indexList = []
    index = 0
    for reactant in reactants:
        reactant = findHeatOfFormation(reactant[0].equation)
        heatList.append(reactant)
        if reactant[2] == "special":
            indexList.append(index)
        index += 1
    for product in products:
        product = findHeatOfFormation(product[0].equation)
        product[1] = -1 * product[1]
        heatList.append(product)
        if product[2] == "special":
            indexList.append(index)
        index += 1

    mole = random.randint(1, 40) / 40
    cmpds = reactants + products
    factorList = [mole * random.randint(1, 5) / random.randint(1, 5) for i in reactants]
    limitingMoles = min(factorList)
    for i in products:
        factorList.append(limitingMoles)
    moles = []
    coefficients = []
    for i, cmpd in enumerate(cmpds):
        moles.append(factorList[i] * cmpd[1])
        coefficients.append(cmpd[1])

    for i, reactant in enumerate(reactants):
        reactant = reactant[0]
        if i in indexList:
            reactant = heatList[i][0]
            printStr += reactant + " and "
            indexList.pop(0)
        else:
            coeffs = [i[1] for i in reactants + products]
            printStr += reactant_name(reactant, coeffs) + " and "
    printStr = printStr[0:-5] + ". "

    if indexList != []:
        for i in indexList:
            newCmpd = heatList[i][0]
            printStr += f"{newCmpd} is formed. "

    for i, cmpd in enumerate(reactants):
        name = heatList[i][0]
        if "(g" not in name and "(l" not in name and "," not in name and "(s" not in name:
            name = compound(name).getName()
        amount = randUnit(cmpd[0], moles[i])
        amount = str(amount[0]) + " " + amount[1]
        printStr += f"There is {amount} of {name}. "

    for cmpd in heatList:
        validHeat = True
        if cmpd[2] in ["small", "special"] or int(cmpd[1]) == 0:
            validHeat = False
        if validHeat:
            name = cmpd[0]
            name = compound(name).getName()
            heatOfCurrentCmpd = cmpd[1]
            if cmpd in products:
                heatOfCurrentCmpd *= -1
            printStr += f"The heat of formation of {name} is {heatOfCurrentCmpd} kJ. "

    heatOfReaction = 0
    for i, cmpd in enumerate(heatList):
        heatOfReaction += cmpd[1] * limitingMoles * coefficients[i]
    heatOfReaction *= 1000

    liquid = compound(random.choice(list(heatOfPhysicalChangesLiquid.keys())))
    fp, bp, heatOfFusion, heatOfVaporization, sSpecificHeat, lSpecificHeat, gSpecificHeat = heatOfPhysicalChangesLiquid.get(liquid.equation)
    massLiquid = random.randint(1000, 2500)
    initialTempWater = random.randint(20, 40)
    liquid.setTemp(initialTempWater)
    finalTemp = liquid.heat(heatOfReaction, massLiquid / liquid.getMass(), fp, bp, heatOfFusion, heatOfVaporization, sSpecificHeat, lSpecificHeat, gSpecificHeat)
    liquidEqs = {"CH3COCH3": "Acetone", "C6H6": "Benzene", "C2H5OH": "Ethanol", "CH3OH": "Methanol", "H2O": "Water", "C8H18": "Oil (C8H18)"}
    density = liquidDensitys.get(liquidEqs.get(liquid.equation))
    printStr += f"The density of {liquidEqs.get(liquid.equation).lower()} is {density} g/mL. "
    goodOptions = [f"{massLiquid / density} mL of ", f" at {initialTempWater} C", f" The final temperature is {finalTemp} C."]
    options = [massLiquid, initialTempWater, finalTemp]
    questions = [" What is the mass of the liquid?", " What is the initial temperature of the liquid?", " What is the final temperature of the liquid?"]
    choice = random.randint(0, 2)
    unit = [" g", " C", " C"][choice]
    goodOptions[choice] = ""
    printStr += f"They are combined in a bomb calorimeter with {goodOptions[0]}{liquidEqs.get(liquid.equation).lower()}{goodOptions[1]}.{goodOptions[2]}"
    printStr += questions[choice]
    if finalTemp in [0, 100]:
        printStr += " (give the range of values; the given answer should be in that range)"

    question = printStr + "\n"
    return question, str(options[choice]) + unit
