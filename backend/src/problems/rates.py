"""Rates problems (57-58)."""
import random
from copy import deepcopy
from src.problem_registry import problem, RATES
from chemData import *
from src import *


@problem(57, "Basic Concentration", RATES)
def basic_concentration():
    C_i = random.randint(1,400) / 400
    while (C_f := random.randint(1,400) / 400) == C_i: pass
    t = random.randint(1,40) / 20
    question = f"What is the rate if the concentration goes from {C_i} M to {C_f} M in {t} seconds."
    return question, round((C_i - C_f) / t, 2)

@problem(58, "Method of Initial Rates", RATES)
def method_of_initial_rates():
    rx = reaction(randomRx())
    while True:
        reactants = rx.formatRxList()[0]
        if rx.molecularity() == 1:
            rx = reaction(randomRx())
            continue
        break

    lines = [f"Consider the following reaction and data:\n{rx}\n"]

    rate_orders = []
    for _ in reactants:
        curr = random.randint(1,9)
        curr = int(curr > 5) + int(curr > 1)
        rate_orders.append(curr)

    k = round_sig(random.randint(1,100) / 10 * (10 ** (random.randint(-5,5))))

    names = ["[" + i[0].equation + "]" for i in reactants] + ["rate (mol/Ls)"]
    first_ex = [random.randint(1,20) / 200 for _ in reactants]
    rate_1 = k
    for i, conc in enumerate(first_ex): rate_1 *= conc ** (rate_orders[i-1])
    first_ex.append(round_sig(rate_1))
    expirements = [[""] + names, [1] + first_ex]
    used = []
    num = 1
    for _ in reactants:
        while (choice := random.randint(1,len(first_ex) - 1)) in used: pass
        used.append(choice)
        factor = random.randint(2,4) ** (random.randint(0,1) * 2 - 1)
        curr_ex = deepcopy(expirements[1])
        curr_ex[choice] = round_sig(curr_ex[choice] * factor)
        curr_ex[-1] = round_sig(curr_ex[-1] * (factor ** rate_orders[choice-1]))
        curr_ex[0] = (num := num + 1)
        expirements.append(curr_ex)

    for i in expirements: lines.append(str(i))

    rate_law = "k"
    for i, r in enumerate(reactants):
        i = rate_orders[i]
        if i != 0: rate_law += "[" + r[0].equation + "]" + str(2) * (int(i == 2))

    lines.append("\n What is the rate law for this reaction?")

    return "\n".join(lines), f"rate law: {rate_law}, k: {k}"
