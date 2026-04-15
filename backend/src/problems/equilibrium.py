"""Equilibrium problems (59-62)."""
import random
from src.problem_registry import problem, EQUILIBRIUM
from chemData import *
from src import *

@problem(59, "Determining the Equilibrium Expression", EQUILIBRIUM)
def equilibrium_expression():
    rx = reaction("eq")
    question = f"Consider the following reaction: {rx.phaseStr()}. What is the equilbrium expression for this reaction?"
    return question, rx.eqExpressionStr()

@problem(60, "Missing Equilibrium Concentration", EQUILIBRIUM)
def missing_equilibrium_concentration():
    rx = reaction("eq", waterAsGas = True)
    prodEq, reactEq = rx.eqExpression()
    prodEq = [(p[0], conc) for p, conc in zip(prodEq, rx.prodEqConcs)]
    reactEq = [(r[0], conc) for r, conc in zip(reactEq, rx.reactEqConcs)]
    totEq = prodEq + reactEq
    totStr = [f" There is (are) {round_sig(conc)} M of {cmpd.__repr__()}." for cmpd, conc in totEq]
    missing_index = random.randint(0,len(totStr) - 1)
    missing_str = totStr.pop(missing_index)
    question = f"Consider the following reaction: {rx.phaseStr()}. The equilibrium constant is {'{:0.4e}'.format(rx.K_eq)}.{''.join(totStr)} What is the concentration of {totEq[missing_index][0].__repr__()}?"
    return question, missing_str[1:]

@problem(61, "Calculating K_eq", EQUILIBRIUM)
def calculating_keq():
    rx = reaction("eq", waterAsGas = True)
    prodEq, reactEq = rx.eqExpression()
    prodEq = [(p[0], conc) for p, conc in zip(prodEq, rx.prodEqConcs)]
    reactEq = [(r[0], conc) for r, conc in zip(reactEq, rx.reactEqConcs)]
    totStr = [f" There is (are) {round_sig(conc)} M of {cmpd.__repr__()}." for cmpd, conc in prodEq + reactEq]
    question = f"Consider the following reaction: {rx.phaseStr()}.{''.join(totStr)} What is the equilibrium constant?"
    return question, '{:0.4e}'.format(rx.K_eq)

@problem(62, "Calculating Equilibrium Concentrations from Initial", EQUILIBRIUM)
def equilibrium_from_initial():
    while True:
        rx = reaction("eq", waterAsGas = True)
        prodEq, reactEq = rx.eqExpression()
        intial_react_conc = random.randint(1,40) / 20 + .5
        prodConcs = [0 for _ in rx.prodEqConcs]
        reactConcs = [intial_react_conc for _ in rx.reactEqConcs]
        try:
            rx.eqConcsFromIntial(prodConcs, reactConcs)
            for i in (rx.prodEqConcs + rx.reactEqConcs):
                if i < 0: raise KeyError
        except KeyError: continue

        break

    prodEq = [(p[0], conc) for p, conc in zip(prodEq, rx.prodEqConcs)]
    reactEq = [(r[0], conc) for r, conc in zip(reactEq, rx.reactEqConcs)]

    question = f"Consider the following reaction: {rx.phaseStr()}. The equilibrium constant is {'{:0.4e}'.format(rx.K_eq)}. Intially, each reactant is at {intial_react_conc} M. What are the equilibrium concentrations?"
    return question, "".join([f"There is (are) {round_sig(conc)} M of {cmpd.__repr__()}. " for cmpd, conc in prodEq + reactEq])
