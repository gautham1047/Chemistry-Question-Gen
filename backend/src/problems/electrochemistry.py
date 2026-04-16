"""Electrochemistry problems (69-72)."""
import random
from src.problem_registry import problem, ELECTROCHEMISTRY
from chemData import *
from src import *


@problem(69, "Oxidation Numbers", ELECTROCHEMISTRY)
def oxidation_numbers():
    cmpd = randomCmpd()
    oNums = cmpd.oxidation_numbers()
    oStr = ', '.join([f"{el}: {oNums[el]}" for el in oNums])

    question = f"What are the oxidation numbers of {cmpd}"
    return question, oStr

@problem(70, "Balancing Redox (WIP)", ELECTROCHEMISTRY)
def balancing_redox():
    return "Balancing Redox (WIP)", "WIP"

@problem(71, "Reaction Potential (WIP)", ELECTROCHEMISTRY)
def reaction_potential():
    return "Reaction Potential (WIP)", "WIP"

@problem(72, "Electroplating", ELECTROCHEMISTRY)
def electroplating():
    while (cmpd := randomCmpd(1,0,0,0,0)):
        if len(cmpd.compound) != 2: break

    metal, mCharge = ionizeTernaryIonic(cmpd.equation)[0]
    metal = compound(metal)
    current = random.randint(1,100) / 20 + .5
    time = random.randint(100,999) * 100

    mass = round_sig(metal.getMass(current * time / (F * mCharge)))
    options = [(f"A current of {current} C/t is applied", "What is the current", current, "C/t"),
               (f"The current is applied for {time} s", "How long is the current applied", time, "s"),
                (f"{mass} g of {metal} is deposited", f"How much {metal} is deposited", mass, "g")]
    chosen = random.choice(options)
    options.remove(chosen)

    question = f"{options[0][0]}. {options[1][0]}. {chosen[1]}?"
    return question, f"{chosen[2]} {chosen[3]}"
