"""Compound naming from parsed formula.

Single entry point: `name_from_atoms(atoms, equation)`. Takes the already-parsed
atoms list (`[[sym, count], ...]`) and the raw equation string. Returns the
human-readable name, or the equation itself if no rule matches (matching the
legacy `compound.getNameFromEq` fallback).

Behavior is preserved exactly from the original monolithic method in
compound.py; see test/test_naming_golden.py for the pinned outputs.
"""

from src.utils.parsing import (
    findElement,
    findCharge,
    findPolyatomicIon,
    ionizeTernaryIonic,
    acidNames,
    ionNames,
)


SPECIAL_CMPDS = {
    "NH3": "ammonia",
    "H2O": "water",
    "C2H6O": "ethanol",
    "CH3CH2OH": "ethanol",
    "C2H5OH": "ethanol",
    "CHCl3": "Chloroform",
    "CH3COCH3": "acetone",
    "C6H6": "benzene",
    "CH4": "methane",
    "CH3OH": "methanol",
    "C6H12O6": "glucose",
    "C12H22O11": "sucrose",
    "C6H6O": "phenol",
    "C6H5OH": "phenol",
    "C6H5NO2": "nitrobenzene",
    "C10H16O": "camphor",
}

DIATOMICS = {
    "H2": "hydrogen",
    "N2": "nitrogen",
    "O2": "oxygen",
    "F2": "flourine",
    "Cl2": "chlorine",
    "Br2": "bromine",
    "I2": "iodine",
}


def _unique_elements(atoms):
    seen = []
    for pair in atoms:
        if isinstance(pair, int):
            continue
        if pair[0] not in seen:
            seen.append(pair[0])
    return seen


def _name_element(atoms, equation):
    if equation in DIATOMICS:
        return DIATOMICS[equation] + " gas"
    return findElement(equation)[1]


def _name_hydrohalic_acid(equation):
    body = "".join(c for c in equation if c != "H" and not c.isdigit())
    return "hydro" + acidNames.get(body) + " acid"


def _name_binary_ionic(atoms, equation, unique_els):
    # ionic if any unique element is a metal/transition metal
    metal = None
    nonmetals = []
    for sym in unique_els:
        el = findElement(sym)
        if el[4] in ["m", "tm"]:
            metal = sym
        else:
            nonmetals.append(sym)
    if metal is None:
        return None

    metal_el = findElement(metal)
    metal_name = metal_el[1]
    nonmetal_name = ionNames.get(nonmetals[0])
    if metal_el[4] == "tm":
        try:
            m_charge = ionizeTernaryIonic(equation)[0][1]  # handles peroxide/azide
        except Exception:
            nonmetal = findElement(nonmetals[0])
            nm_charge = int(nonmetal[3][0])
            if nm_charge > 4:
                nm_charge = 8 - nm_charge
            m_charge = int(nm_charge * atoms[1][1] / atoms[0][1])
        tm_fix = f" ({m_charge}) "
    else:
        tm_fix = " "
    return metal_name + tm_fix + nonmetal_name


def _name_binary_molecular(equation):
    """Prefix-free fallback that only fires if the subscripts happen to match
    the ideal ionic charges. This preserves the original quirk where most
    covalent binaries (CO2, SO3, N2O5, P2O5) fall through to `return eq`.
    """
    el1 = equation[0]
    el2 = ""
    found_digit_or_upper = False
    coefficients = []
    for i in equation[1:]:
        if i.isdigit() or i.isupper():
            found_digit_or_upper = True
        elif not found_digit_or_upper:
            el1 += i
        if found_digit_or_upper and not i.isdigit():
            el2 += i
        if i.isdigit():
            coefficients.append(int(i))
    ideal_coefficients = [findCharge(el1), findCharge(el2)]
    if set(ideal_coefficients) == set(coefficients):
        e1 = findElement(el1)
        e2 = findElement(el2)
        if e1[7] > e2[7]:
            first_el, last_el = e2, e1
        else:
            first_el, last_el = e1, e2
        last_name = ionNames.get(last_el[2])
        return first_el[1] + " " + last_name
    return None


def _name_ternary_acid(equation):
    if equation[1].isdigit():
        index = 2
        charge = int(equation[1])
    else:
        index = 1
        charge = 1
    ion = equation[index:]
    name = findPolyatomicIon(ion, charge)
    name = name.replace("ite", "ous")
    name = name.replace("ate", "ic")
    name = name.replace("sulf", "sulfur")
    name = name.replace("sulfuride", "sulfide")
    name = name.replace("phosph", "phosphor")
    name = name.replace("cynanide", "hydrocyanic")
    name = name.replace("azide", "hydroazoic")
    return name + " acid"


def _name_ternary_ionic(equation):
    ionized = ionizeTernaryIonic(equation)
    ion = findPolyatomicIon(ionized[1][0], ionized[1][1])
    metal = ionized[0][0]
    if metal == "NH4":
        return "ammonium " + ion
    metal_el = findElement(metal)
    if metal_el[4] == "tm":
        tm_fix = f" ({ionized[0][1]}) "
    else:
        tm_fix = " "
    return metal_el[1] + tm_fix + ion


def name_from_atoms(atoms, equation):
    """Top-level name dispatch. Matches legacy `compound.getNameFromEq` output.

    Returns `equation` as a safe fallback if any internal lookup fails
    (e.g. `acidNames.get(body)` returning None for unusual formulas like H3O).
    The legacy monolithic method had the same safety net via its trailing
    bare-except; preserving it here means callers can always rely on a str.
    """
    try:
        return _dispatch(atoms, equation)
    except Exception:
        return equation


def _dispatch(atoms, equation):
    if equation in SPECIAL_CMPDS:
        return SPECIAL_CMPDS[equation]

    unique_els = _unique_elements(atoms)

    # single element (or legacy flat-shape sentinel: cmpd[1] is int)
    if len(atoms) == 1 or (len(atoms) > 1 and isinstance(atoms[1], int)):
        return _name_element(atoms, equation)

    # organics: fall through to raw formula
    if "C" in unique_els and "H" in unique_els:
        return equation

    if len(atoms) == 2 and "(" not in equation:
        # hydrohalic acid: H + single nonmetal
        if equation[0] == "H" and not equation[1].islower():
            return _name_hydrohalic_acid(equation)

        ionic_name = _name_binary_ionic(atoms, equation, unique_els)
        if ionic_name is not None:
            return ionic_name

        mol_name = _name_binary_molecular(equation)
        if mol_name is not None:
            return mol_name
        return equation

    # 3+ unique elements or parenthesized
    # ternary acid: leading H followed by an uppercase / digit
    if equation[0] == "H" and not equation[1].islower():
        return _name_ternary_acid(equation)

    try:
        return _name_ternary_ionic(equation)
    except Exception:
        pass
    return equation