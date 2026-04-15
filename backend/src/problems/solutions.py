"""Solutions problems (46-56)."""
import random
from src.problem_registry import problem, SOLUTIONS
from src.problems._helpers import reaction_verb, reactant_name
from chemData import *
from src import *


@problem(46, "Solubility Calculations", SOLUTIONS)
def solubility_calculations():
    while True:
        cmpd = compound(random.choice(list(solubilities)))
        temp = random.randint(0,3)
        if solubilities.get(cmpd.equation)[temp] != None: break

    temps = [0, 20, 50, 100]
    amnt = random.randint(1,20) * 25
    mol = solubilities.get(cmpd.equation)[temp] * amnt / 100 / cmpd.getMass()
    n = randUnit(cmpd, mol)
    question = f"How much {cmpd.getNameFromEq()} is soluble in {amnt} g of H2O at {temps[temp]} degrees C ({n[1]})?"
    return question, n[0]

@problem(47, "Determining Saturation", SOLUTIONS)
def determining_saturation():
    while True:
        cmpd = compound(random.choice(list(solubilities)))
        temp = random.randint(0,3)
        if solubilities.get(cmpd.equation)[temp] != None: break

    temps = [0, 20, 50, 100]
    amnt = random.randint(1,20) * 25
    theoretical = solubilities.get(cmpd.equation)[temp] * amnt / 100
    changeBool = random.randint(-1,1)
    accAmnt = theoretical + changeBool * .05 * random.randint(1,10) * theoretical

    question = f"Is a solution of {accAmnt} of {cmpd.getNameFromEq()} super-/un-/saturated in {amnt} g of H2O at {temps[temp]} degrees C?"
    return question, ["unsaturated", "saturated", "supersaturated"][changeBool + 1]

@problem(48, "Dilution", SOLUTIONS)
def dilution():
    initialMol = random.randint(1,40) / 20
    while (finalMol := random.randint(1,40) / 200) == initialMol: pass
    initialVol = random.randint(1,40) / 20
    finalVol = initialMol * initialVol / finalMol
    temp = [(initialMol, "initial molarity", "M"), (initialVol, "initial volume", "L"), (finalMol, "final molarity", "M"), (finalVol, "final volume", "L")]
    other = temp.pop(random.randint(0,3))
    question = ""
    for t in temp: question += f"The {t[1]} is {t[0]} {t[2]}. "
    question += f"What is the {other[1]}?"
    return question, f"{other[0]} {other[2]}"

@problem(49, "Solutions Unit Conversions (Aqueous)", SOLUTIONS)
def solution_conversions_aqueous():
    moles_solute = random.randint(1,40) / 20
    total_volume = random.randint(1,150) / 50
    sol = solution(compound(), moles_solute = moles_solute, total_volume = total_volume)

    while True:
        choices = [(f"There are {sol.moles_solute} moles of solute.", "How many moles of the solute are there?"), (f"There are {sol.moles_solvent} moles of solvent.", "How many moles of the solvent are there?"),
               (f"It's volume is {sol.volume} L.", "What is the total volume"), (f"Its molarity is {round_sig(sol.molarity())} M", "What is the molarity?"),
               (f"Its molality is {round_sig(sol.molality())} m.", "What is the molality?"), (f"The mole fraction of the solute is {round_sig(sol.moleFractions())}.", "What is the mole fraction of the solute?"),
               (f"The mole fraction of the solvent is {round_sig(sol.moleFractions(False))}.", "What is the mole fraction of the solvent?"), (f"The percent m/v of the solution is {round_sig(sol.pMV())}%.", "What is the percent m/v?")]

        inds = set()
        choice_one = random.choice(choices)
        inds.add(choices.index(choice_one))
        choices.remove(choice_one)
        choice_two = random.choice(choices)
        inds.add(choices.index(choice_two))
        choices.remove(choice_two)
        chosen_answer = random.choice(choices)
        inds.add(choices.index(chosen_answer))

        b = True
        for i in [{5,6}, {3,4}, {3,7}, {4,7}, {1,2}]:
            if inds & i == i: b = False

        if b: break

    question = f"Consider an aqueous solution of {sol.solute.getNameFromEq()}. Remember that the density of water is 1 g/mL and ignore the solute's volume. {choice_one[0]} {choice_two[0]} {chosen_answer[1]}"
    return question, chosen_answer[0]

@problem(50, "Solutions Unit Conversions (general)", SOLUTIONS)
def solution_conversions_general():
    moles_solute = random.randint(1,40) / 20
    total_volume = random.randint(1,150) / 50
    solvent = compound(random.choice(list(fpDepressionConstants)))
    sol = solution(compound(), moles_solute = moles_solute, total_volume = total_volume, solvent = solvent)

    while True:
        choices = [(f"There are {sol.moles_solute} moles of solute.", "How many moles of the solute are there?"), (f"There are {sol.moles_solvent} moles of solvent.", "How many moles of the solvent are there?"),
               (f"It's volume is {sol.volume} L.", "What is the total volume"), (f"Its molarity is {round_sig(sol.molarity())} M.", "What is the molarity?"),
               (f"Its molality is {round_sig(sol.molality())} m.", "What is the molality?"), (f"The mole fraction of the solute is {round_sig(sol.moleFractions())}.", "What is the mole fraction of the solute?"),
               (f"The mole fraction of the solvent is {round_sig(sol.moleFractions(False))}.", "What is the mole fraction of the solvent?"), (f"The percent m/v of the solution is {round_sig(sol.pMV())}%.", "What is the percent m/v?"),
               (f"The density of the solvent is {sol.solvent_density} g/mL.", "What is the density of the solvent?")]
        inds = set()
        choice_one = random.choice(choices)
        inds.add(choices.index(choice_one))
        choices.remove(choice_one)
        choice_two = random.choice(choices)
        inds.add(choices.index(choice_two))
        choices.remove(choice_two)
        choice_three = random.choice(choices)
        inds.add(choices.index(choice_three))
        choices.remove(choice_three)
        chosen_answer = random.choice(choices)
        inds.add(choices.index(chosen_answer))

        b = True
        for i in [{5,6}, {3,4}, {3,7}, {4,7}, {1,2}]:
            if inds & i == i: b = False

        if b: break

    question = f"Consider a solution, which is not necessarily aqueous, containing {sol.solute.getNameFromEq()} (solute). Ignore the solute's volume. {choice_one[0]} {choice_two[0]} {choice_three[0]} {chosen_answer[1]}"
    return question, chosen_answer[0]

@problem(51, "Colligative Properties", SOLUTIONS)
def colligative_properties():
    moles_solute = random.randint(1,40) / 20
    total_volume = random.randint(1,150) / 50
    bpOrFp = bool(random.getrandbits(1))

    if bpOrFp: solvent = random.choice(list(bpElevationConstants))
    else: solvent = random.choice(list(fpDepressionConstants))

    sol = solution(compound(getRandomCompound(3,0,1,0,2)), moles_solute= moles_solute, total_volume= total_volume, solvent= compound(solvent))
    word = ["boiling", "freezing"][int(bpOrFp)]

    while True:
        choices = [(f"There is/are {sol.moles_solute} moles of solute.", "How many moles of the solute are there?"), (f"There is/are {sol.moles_solvent} moles of solvent.", "How many moles of the solvent are there?"),
               (f"The solvent's volume is {sol.volume} L.", "What is the total volume"), (f"Its molarity is {round_sig(sol.molarity())} M", "What is the molarity?"),
               (f"The mole fraction of the solute is {round_sig(sol.moleFractions())}.", "What is the mole fraction of the solute?"), (f"The mole fraction of the solvent is {round_sig(sol.moleFractions(False))}.", "What is the mole fraction of the solvent?"),
               (f"The percent m/v of the solution is {round_sig(sol.pMV())}%.", "What is the percent m/v?"), (f"The density of the solvent is {sol.solvent_density} g/mL.", "What is the density of the solvent?")]

        inds = set()
        choice_one = random.choice(choices)
        inds.add(choices.index(choice_one))
        choices.remove(choice_one)
        choice_two = random.choice(choices)
        inds.add(choices.index(choice_two))
        choices.remove(choice_two)
        chosen_answer = random.choice(choices)
        inds.add(choices.index(chosen_answer))

        b = True
        for i in [{5,6}, {3,4}, {3,7}, {4,7}, {1,2}]:
            if inds & i == i: b = False

        if b: break

    question = f"Consider a solution, which is not necessarily aqueous, containing {sol.solute.getNameFromEq()} (solute). Ignore the solute's volume. {choice_one[0]} {choice_two[0]} What is the {word} point?"
    question += f" The molar mass of the solvent is {sol.solvent.getMass()} g/mol."
    if bpOrFp:
        question += f" The boiling point of the solvent is {miscBps.get(solvent)} and Kb is {bpElevationConstants.get(solvent)}"
        return question, round_sig(sol.boilingPoint(), 6)
    else:
        question += f" The freezing point of the solve is {miscFps.get(solvent)} and Kf is {bpElevationConstants.get(solvent)}"
        return question, round_sig(sol.freezingPoint(), 6)

@problem(52, "Molar Mass From bp/fp", SOLUTIONS)
def molar_mass_from_bp_fp():
    moles_solute = random.randint(1,40) / 20
    total_volume = random.randint(1,150) / 50
    bpOrFp = bool(random.getrandbits(1))

    if bpOrFp: solvent = random.choice(list(bpElevationConstants))
    else: solvent = random.choice(list(fpDepressionConstants))

    givenEmpirical = bool(random.getrandbits(1))

    solute = compound(getRandomCompound(0,0,0,0,1))
    if givenEmpirical: solute.multCompound(random.randint(1,5))
    sol = solution(solute, moles_solute= moles_solute, total_volume= total_volume, solvent= compound(solvent))

    question = ""
    if givenEmpirical:
        pComp = solute.percentComposition()
        question += "An unknown compound contains "
        for i in pComp: question += f"{round_sig(i[1], 4)}% {i[0]} "

    word = ["molar mass", "molecular formula"][int(givenEmpirical)]

    solvent_mass = sol.solvent.getMass(sol.moles_solvent)
    if bpOrFp: question += f"The boiling point of a molecular solvent is {miscBps.get(solvent)} and the Kb is {bpElevationConstants.get(solvent)}. If the boiling point of the solution is {round_sig(sol.boilingPoint())} when there is {sol.solute.getMass(sol.moles_solute)} g of solute in {round_sig(solvent_mass)} g of the solvent, what is the {word} of the solute?"
    else: question += f"The freezing point of a molecular solvent is {miscFps.get(solvent)} degrees C and Kf is {fpDepressionConstants.get(solvent)}. If the freezing point of the solution is {round_sig(sol.freezingPoint())} when there is {sol.solute.getMass(sol.moles_solute)} g of solute in {round_sig(solvent_mass)} g of solvent, what is the {word} of the solute?"

    if givenEmpirical: return question, solute.getEq()
    else: return question, solute.getMass()

@problem(53, "Henry's Law", SOLUTIONS)
def henrys_law():
    while True:
        cmpd = random.choice(list(solubilities))
        temp_index  = random.randint(0,3)
        temp = [0,20,50,100][temp_index]
        initial_s = solubilities.get(cmpd)[temp_index]
        if initial_s: break

    final_p = random.randint(1,150) / 50
    final_p = randPressureUnit(final_p)
    final_s = round_sig(initial_s * final_p[2])

    choices = [("final pressure", final_p[0], final_p[1]), ("final solubility", final_s, "g / 100 g H2O")]

    choice = random.choice(choices)
    choices.remove(choice)

    question = f"Consider {cmpd} at {temp} degrees C. What is the {choices[0][0]} if the {choice[0]} is {choice[1]} {choice[2]}?"
    return question, f"{choices[0][1]} {choices[0][2]}"

@problem(54, "Reactions with Solubility Units", SOLUTIONS)
def reactions_with_solubility_units():
    while True:
        rx = reaction(randomRx(["double replacement", "special"]))
        separatedCmpds = rx.formatRxList()
        products = rx.SkeletonEquation()[1]
        reactants = rx.SkeletonEquation()[0]
        soluableProducts = [i for i in products if i.equation not in ["NO2", "NO", "H2O", "CO2", "NH3",]]
        if compound("NO2") in soluableProducts: soluableProducts.remove(compound("NO2"))
        if len(soluableProducts) != 0: break

    printStr = reaction_verb(rx)
    for reactant in reactants:
        printStr += reactant_name(reactant, rx.balanceEq()) + " and "
    question = printStr[0:-5] + ". "

    solutions_list : list[solution]= []
    minMol = 99
    minIndex = 0
    i = 0
    for cmpd in reactants:
        mol = random.randint(1,40) / 20
        if mol < minMol:
            minMol = mol
            minIndex = i
        i += 1

        molarity = random.randint(1,150) / 50
        volume = mol / molarity
        solutions_list.append(solution(cmpd, moles_solute = mol, total_volume = volume))

    for sol in solutions_list: question += f"You have {round_sig(sol.volume)} L of a {round_sig(sol.molarity())} M aqueous solution of {sol.solute.equation}. "
    finalProd = random.choice(soluableProducts)
    for i in separatedCmpds[1]:
        if i[0] == finalProd: prodCoeff = i[1]

    minCoeff = separatedCmpds[0][minIndex][1]
    prodMol = minMol / minCoeff * prodCoeff
    vol = random.randint(1,150) / 50
    prodSol = solution(finalProd, moles_solute = prodMol, total_volume= vol)
    question += f"All of the {finalProd.equation} is moved to its own {vol} L beaker of water. What is the molarity of this solution?"

    return question, round_sig(prodSol.molarity())

@problem(55, "Hydrates", SOLUTIONS)
def hydrates():
    hyd = hydrate(compound(getRandomCompound(1,0,0,0,0)).equation, random.randint(3,8))
    t = random.randint(0,4)
    if t == 0:
        el = random.choice(hyd.percentComposition())
        question = f"What is the percent by mass of {el[0]} in {hyd.equation}"
        return question, el[1]
    elif t == 1:
        question = f"What percent by mass of {hyd.equation} is water?"
        return question, round_sig(100 * hyd.percentWater())
    elif t == 2:
        eqToPrint = f"{hyd.anhydrous} 🞄 XH2O"
        question = f"If the molar mass of {eqToPrint} is {hyd.getMolarMass()} g/mol, what is X?"
        return question, hyd.numWater
    elif t == 3:
        eqToPrint = "X" + hyd.equation[int(hyd.equation[1].islower()) + 1:]
        question = f"If the molar mass of {eqToPrint} is {hyd.getMolarMass()} g/mol, what is X?"
        return question, hyd.equation[:int(hyd.equation[1].islower()) + 1]
    elif t == 4:
        eqToPrint = "X" + hyd.anhydrous[int(hyd.anhydrous[1].islower()) + 1:] + " 🞄 YH2O"
        question = f"If the molar mass of {eqToPrint} is {hyd.getMolarMass()} g/mol and the compound is {round_sig(100 * hyd.percentWater())}% water by mass, what is X and Y?"
        return question, "X: " + hyd.equation[:int(hyd.equation[1].islower()) + 1] + ", Y: " + str(hyd.numWater)

@problem(56, "Polar vs Nonpolar", SOLUTIONS)
def polar_vs_nonpolar():
    cmpd = compound(randCmpdForBonds())
    question = f"Is {cmpd.getNameFromEq()} polar?"
    return question, ["no", "yes"][int(cmpd.isPolar())]
