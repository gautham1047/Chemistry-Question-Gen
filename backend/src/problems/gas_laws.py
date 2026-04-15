"""Gas Laws problems (18-21)."""
import random
import math
from src.problem_registry import problem, GAS_LAWS
from src.problems._helpers import reaction_verb
from chemData import *
from src import *

@problem(18, "Average Kinetic Energy", GAS_LAWS)
def average_kinetic_energy():
    temp = randTemp()
    KE = round(1.5 * RkPa * temp[2] / 1000, 4)

    if (bool(random.getrandbits(1))):
        question = f"What is the average kinetic energy of a gas at {temp[0]} {temp[1]}?"
        return question, KE
    else:
        question = f"What is the temperature of a gas with an average kinetic energy of {KE} kJ/mol, in {temp[1]}?"
        return question, f"{temp[0]} {temp[1]}"

@problem(19, "Effusion Rates", GAS_LAWS)
def effusion_rates():
    cmpd1 = compound(getRandomCompound(0,1,1,1,0))
    cmpd2 = compound(getRandomCompound(0,1,1,1,0))

    mass1 = cmpd1.getMass()
    mass2 = cmpd2.getMass()

    if mass1 > mass2:
        bigger = cmpd1
        smaller = cmpd2
        rateFactor = math.sqrt(mass1/mass2)
    else:
        bigger = cmpd2
        smaller = cmpd1
        rateFactor = math.sqrt(mass2/mass1)

    qType = random.randint(0,2)

    if qType == 0:
        question = f"How much faster is {smaller.name} than {bigger.name}?"
        return question, rateFactor
    elif qType == 1:
        lines = [f"If {smaller.name} is {rateFactor} times faster than the other gas, what is the other gas?"]

        options = []
        for i in range(0,4):
            option = compound(getRandomCompound())
            while option.getMass() == bigger.getMass():
                option = compound(getRandomCompound())
            options.append(option)

        options.insert(random.randint(0,3), bigger)

        for i, j in enumerate(options):
            if j.type == "diatomic":
                gaseous = ""
            else:
                gaseous = " gaseous"
            lines.append(f"{i+1}.{gaseous} {j.name}")

        return "\n".join(lines), f"{bigger.name}, since it has a molar mass of {bigger.getMass()}"
    elif qType == 2:
        cmpd1 = compound(getRandomCompound(0,1,1,1,0))
        cmpd2 = compound(getRandomCompound(0,0,0,1,0))

        rate1 = .025 * random.randint(0,20)
        rate2 = rate1 * math.sqrt(cmpd2.getMass() / cmpd1.getMass())

        question = f"{cmpd1.name} effuses with a rate of {rate2}, and an unknown homonuclear diatomic gas effuses through the same opening at {rate1}. What is the other gas?"
        return question, cmpd2.name

@problem(20, "Gas Laws", GAS_LAWS)
def gas_laws_problem():  
    goodQuestion = False
    valuesRanges = [[0,4], [.5, 100], [0,1], [100,450]]
    while not goodQuestion:
        P = randPressure()
        V = randVolume()
        cmpd = compound(getRandomCompound())
        n = random.randint(1,40) / 40
        moles = randUnit(cmpd, n)
        T = randTemp()

        idealGasLawList = [P[2], V[2], n, T[2]]

        missing = random.randint(0,3)

        if missing < 1:
            other = (missing + 1) % 2
            missingValue = (idealGasLawList[2] * Ratm * idealGasLawList[3]) /  idealGasLawList[other]
        else:
            other = (missing - 1) % 2 + 2
            missingValue = (idealGasLawList[0] * idealGasLawList[1]) / (idealGasLawList[other] * Ratm)

        missingRange = valuesRanges[missing]

        if missingValue > missingRange[0] and missingValue < missingRange[1]:
            goodQuestion = True

    idealGasLawList[missing] = missingValue

    qType = bool(random.getrandbits(1))

    units = ["atm", "L", "moles", "K"]
    if qType:
        missingIndex = random.randint(0,3)
        sentences = [f"The pressure if {getPressure(idealGasLawList[0], P[1])} {P[1]}. ", f"The volume of {cmpd.name} is {getVolume(idealGasLawList[1], V[1])} {V[1]}. ",
                     f"There are/is {moles[0]} {moles[1]} of {cmpd.name}. ", f"The temperature is {getTemp(idealGasLawList[3], T[1])} {T[1]}. "]

        questionParts = ["What is the pressure?", f"What is the volume of {cmpd.name}?", f"How many moles of {cmpd.name} are there?", f"What is the temperature?"][missingIndex]

        for i in [0,1,2,3]:
            if i == missingIndex: continue
            questionParts = sentences[i] + questionParts

        return questionParts, str(idealGasLawList[missingIndex])+ " "+ units[missingIndex]
    else:
        givenIndex = random.randint(0,3)
        otherIndex = givenIndex
        while otherIndex == givenIndex:
            otherIndex = random.randint(0,3)

        if givenIndex == 0: final = randPressure()
        elif givenIndex == 1: final = randVolume()
        elif givenIndex == 2:
            finalMoles = random.randint(1,40) * 1/40
            final = randUnit(cmpd, finalMoles)
        elif givenIndex == 3: final = randTemp()

        sentences = [f"The initial pressure if {getPressure(idealGasLawList[0], P[1])} {P[1]}. ", f"The initial volume of {cmpd.name} is {getVolume(idealGasLawList[1], V[1])} {V[1]}. ",
                     f"Initally, there are/is {moles[0]} {moles[1]} of {cmpd.name}. ", f"The initial temperature is {getTemp(idealGasLawList[3], T[1])} {T[1]}. "]

        finalIdealGasLawList = idealGasLawList.copy()
        finalIdealGasLawList[givenIndex] = final[2]

        if otherIndex < 2:
            otherOtherIndex = (otherIndex + 1) % 2
            finalIdealGasLawList[otherIndex] = finalIdealGasLawList[2] * finalIdealGasLawList[3] * Ratm / finalIdealGasLawList[otherOtherIndex]
        else:
            otherOtherIndex = (otherIndex -1) % 2 + 2
            finalIdealGasLawList[otherIndex] = finalIdealGasLawList[0] * finalIdealGasLawList[1] / (finalIdealGasLawList[otherOtherIndex] * Ratm)

        questionSentences = [sentences[givenIndex], sentences[otherIndex]]

        pressure = randPressureUnit(finalIdealGasLawList[0])
        volume = randVolumeUnit(finalIdealGasLawList[1])
        moles = randUnit(cmpd, finalIdealGasLawList[2])
        temp = randTempUnit(finalIdealGasLawList[3])

        newSentences = [f"The final pressure is {pressure[0]} {pressure[1]}. ", f"The final volume is {volume[0]} {volume[1]}. ",
                        f"If we add/take away moles to keep all the other factors constant, the final amount of {cmpd.name} is {moles[0]} {moles[1]}. ",
                        f"The final temperature is {temp[0]} {temp[1]}. "]

        questionSentences.extend([newSentences[givenIndex], newSentences[otherIndex]])

        answers = [idealGasLawList[givenIndex], idealGasLawList[otherIndex], finalIdealGasLawList[givenIndex], finalIdealGasLawList[otherIndex]]
        quants = ["pressure", "volume", "moles", "temperature"]
        answerChoices = [f"What is the initial {quants[givenIndex]}?", f"What is the initial {quants[otherIndex]}?",
                         f"What is the final {quants[givenIndex]}?", f"What is the final {quants[otherIndex]}?"]

        missingIndex = random.randint(0,3)

        questionStr = ""
        for i,sentence in enumerate(questionSentences):
            if i == missingIndex: continue
            questionStr += sentence

        questionStr += answerChoices[missingIndex]

        if missingIndex % 2 == 0: unitsIndex = givenIndex
        else: unitsIndex = otherIndex

        return questionStr, str(answers[missingIndex]) + " "+ units[unitsIndex]

@problem(21, "Gas Stoichiometry", GAS_LAWS, accepts_rx_type=True)
def gas_stoichiometry(rx_type):
    while True:
        bad = True
        while bad:
            rx = reaction(randomRx(rx_type))
            separatedCmpds = rx.formatRxList()
            reactants = separatedCmpds[0]
            products = separatedCmpds[1]
            numReactants = len(reactants)
            if numReactants > 1: bad = False

        printStr = reaction_verb(rx)
        for j, i in enumerate(reactants):
            if len(separatedCmpds) == 3 and  j == 1: printStr += separatedCmpds[2] + " "
            try:
                printStr += i[0].getNameFromEq()
            except: printStr += "error generating name"
            printStr += " and "

        question = printStr[0:-5] + ". Assume every molecular compound is a gas. "
        cmpds = reactants + products
        starterMoles = .25 * random.randint(1,40)
        moles = [starterMoles * round((1.5 * random.random() + .5), 2) for cmpd in reactants]

        limiting = min(moles)
        limitingIndex = moles.index(limiting)

        for i in products:
            moles.append(limiting)

        for i, mole in enumerate(moles):
            moles[i] = round(mole * cmpds[i][1], 2)

        leftoverMoles = [round(mole - limiting * cmpds[i][1], 2) for i, mole in enumerate(moles)]

        gasses = [cmpd[0].isMolecular() for cmpd in cmpds]

        if not any(gasses):
            continue

        pressure = randPressure()
        temp = randTemp()

        volumes = []
        allGasLawInfo = []

        for i in range(0,len(cmpds)):
            if gasses[i]:
                gasLawInfo = [randPressure(), moles[i], randTemp()]
                allGasLawInfo.append(gasLawInfo)
                volume = solveForVolume(gasLawInfo[0][2], gasLawInfo[1], gasLawInfo[2][2])
                volumes.append(volume)
            else:
                allGasLawInfo.append([0,0,0])
                volumes.append(0)

        totalVolume = 0
        for volume in volumes: totalVolume += volume

        numGassesInReactants = 0
        tempQ = ""
        for i, cmpd in enumerate(reactants):
            if not gasses[i]:
                currNumMoles = moles[i]
                currNumMoles = randUnit(cmpd[0], currNumMoles)
                tempQ += f"There is (are) {currNumMoles[0]} {currNumMoles[1]} of {cmpd[0].getNameFromEq()}"
                if currNumMoles[1] == "L": tempQ += " (treat it like a gas at STP). "
                else: tempQ += ". "
                continue
            volume = randVolumeUnit(volumes[i])
            pressure = allGasLawInfo[i][0]
            temp = allGasLawInfo[i][2]

            question += f"There is {volume[0]} {volume[1]} of {cmpd[0].getNameFromEq()} at {pressure[0]} {pressure[1]} and {temp[0]} {temp[1]}. "
            numGassesInReactants += 1

        if numGassesInReactants == 0:
            for i, cmpd in enumerate(products):
                i += numReactants
                if not gasses[i]: continue
                volume = randVolumeUnit(volumes[i])
                pressure = allGasLawInfo[i][0]
                temp = allGasLawInfo[i][2]
                currPrint = f"After the reaction, {volume[0]} {volume[1]} of {cmpd[0].name} at {pressure[0]} {pressure[1]} and {temp[0]} {temp[1]} is produced. "
                otherReactantIndex = (limitingIndex + 1) % 2
                limiting = randUnit(cmpds[limitingIndex][0], limiting)
                question += currPrint + f" There is excess {cmpds[otherReactantIndex][0].name}. How much of {cmpds[limitingIndex][0].name} is there ({limiting[1]})?"

                return question, f"{limiting[0]} {limiting[1]}"

        chosenProduct = random.choice(products)
        chosenIndex = cmpds.index(chosenProduct)
        productMoles = randUnit(chosenProduct[0], moles[chosenIndex])
        question += tempQ + f"How much {chosenProduct[0].getNameFromEq()} is there ({productMoles[1]})?"
        return question, f"{productMoles[0]} {productMoles[1]}"

