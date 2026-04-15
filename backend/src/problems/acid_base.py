"""Acid-Base problems (64-68)."""
import random
from src.problem_registry import problem, ACID_BASE
from chemData import *
from src import *

@problem(64, "pH Conversions", ACID_BASE)
def ph_conversions():
    molarity = random.random() * (10 ** random.randint(-14,0))
    a = acid("HCl", molarity)
    answers = [("pH", a.pH()), ("pOH", a.pOH()), ("H+ concentration", a.HConc()), ("OH- Concentration", a.OHConc())]
    chosen = random.choice(answers)
    answers.remove(chosen)

    ans = random.choice(answers)
    question = f"If the {chosen[0]} is {round_sig(chosen[1])}, what is the {ans[0]}?"
    return question, round_sig(ans[1])

@problem(65, "pH from Molarity", ACID_BASE)
def ph_from_molarity():
    molarity = random.random() * (10 ** random.randint(-14,0))
    isAcid = bool(random.getrandbits(1))
    if isAcid:
        eq = random.choice(list(KaDict.keys()))
        ab = acid(eq, molarity=molarity)
    else:
        eq = random.choice(list(KbDict.keys()))
        ab = base(eq, molarity=molarity)
    one = random.choice([("pH", ab.pH()), ("pOH", ab.pOH()), ("H+ concentration", ab.HConc()), ("OH- Concentration", ab.OHConc())])
    one = list(one)
    one[1] = round_sig(one[1])
    answers = [one, (f"K{'a' if isAcid else 'b'}", "large" if ab.K_eq > 9e199 else round_sig(ab.K_eq)), ("molarity", round_sig(molarity))]

    answer = random.choice(answers)
    answers.remove(answer)

    question = f"What is the {answer[0]} of a solution of {eq} where the {answers[0][0]} is {answers[0][1]} and the {answers[1][0]} is {answers[1][1]}?"
    return question, answer[1] if isinstance(answer[1], str) else round_sig(answer[1])

@problem(66, "pH with Common Ion Effect", ACID_BASE)
def ph_common_ion_effect():
    molarity = random.random() * (10 ** random.randint(-14,0))
    isAcid = bool(random.getrandbits(1))
    addedMolarity = random.randint(1,75) / 100 + .25
    if isAcid:
        eq = random.choice(list(KaDict.keys()))
        ab = acid(eq, molarity)
        metal = elements[random.choice(list(metalsDict))][2]
        mCharge = findCharge(metal)
        nm = [ab.c_base.equation, ab.c_base.charge]
        commonIon = ionicCompoundFromElements(m = [metal, mCharge], n = nm)
        cFactor = mCharge
    else:
        eq = random.choice(list(KbDict.keys()))
        ab = base(eq, molarity)
        nm = randPolyatomic()
        metal = [ab.c_acid.equation, ab.c_base.charge]
        commonIon = ionicCompoundFromElements(m = metal, n = nm)
        cFactor = nm[1]

    ab.addCommonIon(addedMolarity)

    one = random.choice([("pH", ab.pH()), ("pOH", ab.pOH()), ("H+ concentration", ab.HConc()), ("OH- Concentration", ab.OHConc())])
    one = list(one)
    one[1] = round_sig(one[1])
    answers = [one, (f"K{'a' if isAcid else 'b'}", "large" if ab.K_eq > 9e199 else round_sig(ab.K_eq)), ("molarity", round_sig(molarity))]

    answer = random.choice(answers)
    answers.remove(answer)

    question = f"What is the {answer[0]} of a solution of {eq} where the {answers[0][0]} is {answers[0][1]} and the {answers[1][0]} is {answers[1][1]}, if there is {round_sig(addedMolarity / cFactor)} M of {commonIon} in the solution?"
    return question, answer[1]

@problem(67, "Neutralization/Tritation Reactions", ACID_BASE)
def neutralization_titration():
    strongAcids = ["HCl", "HI", "HBr", "HClO4", "HClO3", "HNO3", "H2SO4"]
    strongBases = ["LiOH", "NaOH", "KOH", "RbOH", "CsOH", "Ca(OH)2", "Sr(OH)2", "Ba(OH)2"]
    a = acid(random.choice(strongAcids), moles = random.randint(1,40) / 200 + .05, volume = random.randint(10,40) / 200)
    b = base(random.choice(strongBases), moles = random.randint(1,40) / 200 + .05, volume = random.randint(10,40) / 200)
    n = neutralization(a,b)

    n_ab = n.leftover_ab
    moles = n.salt_moles

    try:
        one = [("pH", n_ab.pH(), ""), ("pOH", n_ab.pOH(), ""), ("H+ concentration", n_ab.HConc(), ""), ("OH- Concentration", n_ab.OHConc(), "")]
    except ValueError:
        one = []
    two = [('leftover moles of salt',  moles, "mol(s)"), ('number of particles in the salt', moles * 6.02e+23, "particles"), ("number of atoms in the salt", n.salt.getAtoms(moles), "atoms"), ("mass of the salt", n.salt.getMass(moles), "g")]
    answer = random.choice(one + two)

    question = f"When {a} is tritrated with {b}, what is the resulting {answer[0]} at equilibrium?"
    return question, str(answer[1]) + " " + answer[2]

@problem(68, "Solubility Products", ACID_BASE)
def solubility_products():
    cmpd = compound(random.choice(list(KspDict)))

    cIon = random.randint(0,2)
    mConc = 0
    nConc = 0
    cStr = ""

    s_rx = cmpd.solubility_rx(mConc, nConc)
    reactants, _ = s_rx.eqExpression()

    if cIon == 1:
        mConc = random.randint(1,40) / 200 + .05
        cStr = f" if there is {mConc} M of {reactants[0][0]} in the solution"
    if cIon == 2:
        nConc = random.randint(1,40) / 200 + .05
        cStr = f" if there is {nConc} M of {reactants[1][0]} in the solution"

    options = [(product[0], conc) for product, conc in zip(reactants, s_rx.prodEqConcs)]
    chosen = random.choice(options)

    question = f"If the K_sp of {cmpd} is {cmpd.K_sp}, what is the concentration of the {chosen[0]} ion{cStr}."
    return question, '{:e}'.format(chosen[1])
