"""Non-numbered helper functions."""
import random
from chemData import polyatomicIons


_RX_VERBS = {
    "s1": "Combine ", "s2": "Combine ", "s3": "Combine ",
    "d1": "Decompose ", "d2": "Decompose ", "d3": "Decompose ",
    "c": "Combust ",
    "complete combustion": "Completely Combust ",
    "incomplete combustion": "Incompletley Combust ",
}


_NITRIC_DILUTE_COEFFS = [[3, 8, 3, 2, 4], [8, 3, 3, 2, 4]]
_NITRIC_CONCENTRATED_COEFFS = [[4, 1, 1, 2, 2], [1, 4, 1, 2, 2]]


def reactant_name(cmpd, coefficients):
    """Return a compound's display name, with nitric-acid dilution inferred from coefficients."""
    name = cmpd.getName()
    if name == "nitric acid":
        coefficients = list(coefficients)
        if coefficients in _NITRIC_DILUTE_COEFFS:
            return "dilute nitric acid"
        if coefficients in _NITRIC_CONCENTRATED_COEFFS:
            return "concentrated nitric acid"
    return name


def reaction_verb(rx):
    """Return the opening verb phrase for a reaction prompt based on rx.typeRx."""
    return _RX_VERBS.get(rx.typeRx, "Write the reaction between ")


MOLAR_VOLUME_STP = 22.4
AVOGADRO = 6.02e23

MOLE_UNIT_LABELS = [" moles of ", " L of ", " particles of ", " atoms of ", " grams of "]
MOLE_UNIT_SHORT = ["moles", "L", "particles", "atoms", "g"]


def mole_conversions(cmpd, moles):
    """Convert moles of a compound to [moles, liters@STP, particles, atoms, grams]."""
    return [
        moles,
        moles * MOLAR_VOLUME_STP,
        moles * AVOGADRO,
        cmpd.getAtoms(moles),
        cmpd.getMass(moles),
    ]


def polyatomic_ion_test(choices):
    """Standalone polyatomic ion quiz. Returns (question, answer)."""
    name = random.choice(choices)
    ion = polyatomicIons.get(name)
    charge = ion[-1]
    if ion != "NH4 1":
        charge = "-" + charge
    question = "What is the equation and charge of " + name + "?"
    answer = f"equation: {ion[:ion.index(' ')]}, charge: {charge}"
    return question, answer
