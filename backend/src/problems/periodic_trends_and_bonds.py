"""Periodic Trends and Bonds problems (33-45)."""
import random
import math
from src.problem_registry import problem, PERIODIC_TRENDS_AND_BONDS
from chemData import *
from src import *


@problem(33, "Atomic Size", PERIODIC_TRENDS_AND_BONDS)
def atomic_size():
    el1 = element(elData = randElement("ntm"))
    el2 = element(elData = randElement("ntm"))

    question = f"Which atom is bigger: {el1.eq} or {el2.eq}?"
    compare = el1.compareSize(el2)

    if compare > 0: return question, el1.eq
    else: return question, el2.eq

@problem(34, "Ion Size", PERIODIC_TRENDS_AND_BONDS)
def ion_size():
    el1 = element(elData = randElement("ntm"), charge = random.randint(0,3))
    el2 = element(elData = randElement("ntm"), charge = random.randint(0,3))

    question = f"Which ion is bigger: {el1} or {el2}?"
    compare = el1.compareSize(el2)

    if compare > 0: return question, el1.eq
    else: return question, el2.eq

@problem(35, "Ionization Energy", PERIODIC_TRENDS_AND_BONDS)
def ionization_energy():
    el1 = element(elData = randElement("ntm"))
    el2 = element(elData = randElement("ntm"))

    question = f"Which atom has more Ionization Energy: {el1.eq} or {el2.eq}?"
    compare = el1.compareIE(el2)

    if compare > 0: return question, el1.eq
    else: return question, el2.eq

@problem(36, "Electronegativity", PERIODIC_TRENDS_AND_BONDS)
def electronegativity_trend():
    el1 = element(elData = randElement("ntm"))
    el2 = element(elData = randElement("ntm"))

    question = f"Which atom has more Ionization Energy: {el1.eq} or {el2.eq}?"
    compare = el1.compareIE(el2)

    if compare > 0: return question, el1.eq
    else: return question, el2.eq

@problem(37, "Electron Affinity", PERIODIC_TRENDS_AND_BONDS)
def electron_affinity():
    el1 = element(elData = randElement("ntm"))
    el2 = element(elData = randElement("ntm"))

    question = f"Which atom has more Ionization Energy: {el1.eq} or {el2.eq}?"
    compare = el1.compareEA(el2)

    if compare > 0: return question, el1.eq
    else: return question, el2.eq

@problem(38, "All Periodic Trends", PERIODIC_TRENDS_AND_BONDS)
def all_periodic_trends():
    fn = random.choice([atomic_size, ion_size, ionization_energy, electronegativity_trend, electron_affinity])
    return fn()

@problem(39, "Lattice Energy", PERIODIC_TRENDS_AND_BONDS)
def lattice_energy():
    metal = randElement("m")[2]
    nonmetal = randElement("n")[2]
    mCharge = findCharge(metal)
    nmCharge = findCharge(nonmetal)

    r = (random.random() * 1.7 + .3) * .1
    E = 2.31e-19 * mCharge * nmCharge / r
    choices = [('{:e}'.format(E), "lattice energy", "J"), (round(r, 5), "ionic bond length", "nm")]
    q = random.choice(choices)
    choices.remove(q)
    ans = choices[0]

    g = math.gcd(mCharge, nmCharge)
    mCoeff = nmCharge // g
    nmCoeff = mCharge // g
    eq = f"{metal}{'' if mCoeff == 1 else mCoeff}{nonmetal}{'' if nmCoeff == 1 else nmCoeff}"

    question = f"If the {q[1]} of {eq} is {q[0] } {q[2]}, what is the {ans[1]} in {ans[2]}"
    return question, f"{ans[0]} {ans[2]}"

@problem(40, "Lewis Dot Structure", PERIODIC_TRENDS_AND_BONDS)
def lewis_dot_structure():
    cmpd = randCmpdForBonds(1,2,1,6)
    question = f"What is the lewis dot structure for {cmpd.equation}"
    return question, print_matrix(cmpd.covalentBonds())

@problem(41, "VSEPR", PERIODIC_TRENDS_AND_BONDS)
def vsepr():
    cmpd = compound(randBMForBonds())
    VSEPRchoices = {0 : "electron domain", 1: "shape", 2 : "angle", 3 : "polarity", 4 : "hybridization of the central atom"}
    choice = random.choice(list(VSEPRchoices))
    question = f"What is the {VSEPRchoices.get(choice)} of {cmpd.equation}"
    return question, cmpd.VESPR()[choice]

@problem(42, "Bond Order", PERIODIC_TRENDS_AND_BONDS)
def bond_order():
    cmpd = randCmpdForBonds()
    question = f"What is the bond order of {cmpd.equation}"
    return question, cmpd.bondOrder()

@problem(43, "Sigma and Pi Bonds", PERIODIC_TRENDS_AND_BONDS)
def sigma_and_pi_bonds():
    cmpd = randCmpdForBonds()
    question = f"How many sigma bonds does {cmpd.equation} have? How many pi bonds?"
    return question, f"sigma bonds: {cmpd.sigmaBonds()}\npi bonds: {cmpd.piBonds()}"

@problem(44, "Bond Energies", PERIODIC_TRENDS_AND_BONDS)
def bond_energies():
    cmpd = randCmpdForBonds()
    question = f"What is the bond energy of {cmpd.equation}"
    return question, cmpd.bondEnergy()

@problem(45, "Enthalpy from Bond Energies", PERIODIC_TRENDS_AND_BONDS)
def enthalpy_from_bond_energies():
    rx = randomRx("bond")
    question = "What is the enthalpy of the following reaction:\n\n" + str(rx)
    return question, rx.enthalpyFromBonds()
