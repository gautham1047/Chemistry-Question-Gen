"""Electron Configuration problems (22-32)."""
import random
import math
from src.problem_registry import problem, ELECTRON_CONFIGURATION
from chemData import *
from src import *


@problem(22, "Electron configuration", ELECTRON_CONFIGURATION)
def electron_config():
    number = random.randint(1,118)
    el = elements[number]
    question = f"What is the electron configuration of {el[1]}?"
    config = electronConfig(number)
    return question, config[2]

@problem(23, "Nobel Gas Shorthand", ELECTRON_CONFIGURATION)
def noble_gas_shorthand():
    number = random.randint(1,118)
    el = elements[number]
    question = f"What is the noble gas shorthand for {el[1]}?"
    config = electronConfig(number)
    return question, config[1]

@problem(24, "Paramagnetic vs Diamagnetic", ELECTRON_CONFIGURATION)
def paramagnetic_vs_diamagnetic():
    number = random.randint(1,118)
    el = elements[number]
    question = f"Is {el[1]} paramagnetic or diamagetic?"
    if number in range(58,71) or number in range(90,103):
        question += "\nAssume one electron goes into a d orbital."
    if isParamagnetic(number):
        return question, f"{el[1]} is paramagnetic."
    else: return question, f"{el[1]} is diamagnetic."

@problem(25, "Quantum Numbers", ELECTRON_CONFIGURATION)
def quantum_numbers_problem():
    elNum = random.randint(1,118)
    qNums = quantumNumbers(elNum)
    question = f"What are the quantum numbers for the last electron to be filled in {elements[elNum][1]}?"
    return question, f"n = {qNums[0]}, l = {qNums[1]}, ml = {qNums[2]}, ms = {qNums[3]}"

@problem(26, "Basic Waves", ELECTRON_CONFIGURATION)
def basic_waves():
    f = round_sig(random.randint(int(3e6), int(3e22)))
    l = round_sig(c / f)
    E = round_sig(h * f)
    qs = [f"The frequency is {'{:e}'.format(f)}.", f"The wave length is {'{:e}'.format(l)}.", f"The energy of the wave is {'{:e}'.format(E)}."]
    ans = ["frequency", "wave length", "energy"]
    qChoice = random.randint(0,2)
    aChoice = random.randint(0,2)
    while qChoice == aChoice:
        aChoice = random.randint(0,2)
    question = f"{qs[qChoice]} What is the {ans[aChoice]}?"
    return question, qs[aChoice]

@problem(27, "Bohr's Law", ELECTRON_CONFIGURATION)
def bohrs_law():
    nf = random.randint(1,10)
    ni = random.randint(1,10)
    while ni == nf: ni = random.randint(1,10)

    E = round_sig(abs(k * (nf ** -2 - ni ** -2)))
    f = round_sig(E / h)
    l = round_sig(c / f)

    rOrA = "releaed" if ni > nf else "absorbed"

    options = random.choice([("frequency (Hz) of the photon wave that is " + rOrA, '{:e}'.format(f)), ("wavelength (m) of the photon wave that is " + rOrA, '{:e}'.format(l)), ("energy (J) of the photon wave that is " + rOrA, '{:e}'.format(E))])

    choices = [options, ("final energy level", nf), ("initial energy level", ni)]

    firstChoice = random.choice(choices)
    choices.remove(firstChoice)
    secondChoice = random.choice(choices)
    choices.remove(secondChoice)

    question = f"The {firstChoice[0]} is {firstChoice[1]}, and the {secondChoice[0]} is {secondChoice[1]}. What is the {choices[0][0]}?"
    return question, choices[0][1]

@problem(28, "De Broglie for electrons", ELECTRON_CONFIGURATION)
def de_broglie_electrons():
    v = round_sig(random.randint(100, 100000))
    KE = round_sig(.5 * eMass * v ** 2)
    l = round_sig(h / (eMass * v))
    choices = [("de Broglie's wavelength", '{:e}'.format(l), "m"), ("kinetic energy", '{:e}'.format(KE), "J"), ("velocity", '{:e}'.format(v), "m/s")]

    questionChoice = random.choice(choices)
    choices.remove(questionChoice)
    answer = random.choice(choices)

    question = f"If the {questionChoice[0]} is {questionChoice[1]} {questionChoice[2]}, what is the {answer[0]} of the electron?"
    return question, str(answer[1]) + " " + answer[2]

@problem(29, "De Broglie in general", ELECTRON_CONFIGURATION)
def de_broglie_general():
    v = round_sig(random.randint(100, 100000))
    m = round_sig(.1 * random.randint(1,100))
    KE = round_sig(.5 * m * v ** 2)
    l = round_sig(h / (m * v))
    choices = [("de Broglie's wavelength", '{:e}'.format(l), "m"), ("kinetic energy", '{:e}'.format(KE), "J"), ("velocity", '{:e}'.format(v), "m/s"), ("mass", m, "kg")]

    first = random.choice(choices)
    choices.remove(first)
    second = random.choice(choices)
    choices.remove(second)

    answer = random.choice(choices)

    question = f"If the {first[0]} is {first[1]} {first[2]} and the {second[0]} is {second[1]} {second[2]}, what is the {answer[0]} of the object?"
    return question, str(answer[1]) + " " + answer[2]

@problem(30, "Heisenburg uncertainty principle", ELECTRON_CONFIGURATION)
def heisenberg_uncertainty():
    v = round_sig(random.randint(int(1e2), int(1e6)))
    x = round_sig(h / (4 * math.pi * v * eMass))
    KE = round_sig(.5 * eMass * v ** 2)
    choices = [("velocity", v, "m/s"), ("uncertainity in the position", x, "m"), ("kinetic energy", KE, "J")]
    questionChoice = random.choice(choices)
    choices.remove(questionChoice)
    answer = random.choice(choices)

    question = f"If the {questionChoice[0]} of the electron is {questionChoice[1]} {questionChoice[2]}, what is the {answer[0]}?"
    return question, str(answer[1]) + " " + answer[2]

@problem(31, "Identifying types of waves", ELECTRON_CONFIGURATION)
def identifying_wave_types():
    f = round_sig(random.randint(int(1e13), int(2e15)))
    l = round_sig(c / f)
    if f < 4.3e14: typeWave = "infrared light and you would use the Paschen Series"
    elif f < 1e15: typeWave = "visible light and you would use the Balmer Series"
    else: typeWave = "ultraviolet light and you would use the Lyman Series"

    choices = [("frequency", '{:e}'.format(f), "Hz"), ("wavelength", '{:e}'.format(l), "m")]
    choice = random.choice(choices)

    question = f"A wave has a {choice[0]} of {choice[1]} {choice[2]}, what is the type of wave, and series would you use?"
    return question, "The wave is " + typeWave

@problem(32, "Harder Bohr's Law", ELECTRON_CONFIGURATION)
def harder_bohrs_law():
    series = random.choice([(1e15, 2e15, 1, "UV"), (4.3e14, 1e15, 2, "visible"), (1e13, 4.3e14, 3, "infrared")])

    nf = series[2]
    ni = random.randint(nf + 1, 10)

    E = round_sig(abs(k * (nf ** -2 - ni ** -2)))
    f = round_sig(E / h)
    l = round_sig(c / f)

    options = [("frequency", '{:e}'.format(f), "Hz"), ("wavelength", '{:e}'.format(l), "m"), ("energy", '{:e}'.format(E), "J")]
    chosen = random.choice(options)

    question = f"The {chosen[0]} of the wave that is released when an electron falls is {chosen[1]} {chosen[2]}. What type of wave is it, and where did the wave start?"
    return question, f"It is a(n) {series[3]} wave, and it started at {ni}"
