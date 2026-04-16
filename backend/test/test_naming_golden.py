"""Golden-output test for compound naming.

Pinned during the getNameFromEq extraction (TODO A in REFACTOR_NOTES.md).
Any change to these outputs is a regression in user-visible question text —
fix the naming code, don't update this table without a deliberate decision.

Run: python test/test_naming_golden.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.compound import compound

GOLDEN = {
    # specials
    "H2O": "water",
    "NH3": "ammonia",
    "CH4": "methane",
    "C6H12O6": "glucose",
    # elements / diatomics
    "Na": "Sodium",
    "Cu": "Copper",
    "Fe": "Iron",
    "H2": "hydrogen gas",
    "N2": "nitrogen gas",
    "Cl2": "chlorine gas",
    # binary ionic (main group)
    "NaCl": "Sodium Chloride",
    "KBr": "Potassium Bromide",
    "MgO": "Magnesium Oxide",
    "Al2O3": "Aluminum Oxide",
    "CaCl2": "Calcium Chloride",
    # binary ionic (transition metal)
    "Fe2O3": "Iron (3) Oxide",
    "CuO": "Copper (2) Oxide",
    "FeCl3": "Iron (3) Chloride",
    "ZnCl2": "Zinc (2) Chloride",
    "PbO2": "Lead (2) Oxide",
    "SnCl4": "Tin (4) Chloride",
    # hydrohalic / binary acids
    "HCl": "hydrochloric acid",
    "HBr": "hydrobromic acid",
    "H2S": "hydrosulfuric acid",
    # ternary acids
    "H2SO4": "sulfuric acid",
    "HNO3": "nitric acid",
    "H3PO4": "phosphoric acid",
    "HClO4": "perchloric acid",
    # ternary ionic
    "Na2SO4": "Sodium sulfate",
    "KNO3": "Potassium nitrate",
    "CaCO3": "Calcium carbonate",
    "Ba(OH)2": "Barium hydroxide",
    "NaOH": "Sodium hydroxide",
    "Cu(NO3)2": "Copper (2) nitrate",
    "Fe(OH)3": "Iron (3) hydroxide",
    "AgNO3": "Silver (1) nitrate",
    "(NH4)2SO4": "ammonium sulfate",
    # known fall-throughs — covalent binaries and a few edge cases the old
    # method returns unchanged. Pinned so we notice if behavior changes.
    "CO2": "CO2",
    "SO3": "SO3",
    "N2O5": "N2O5",
    "P2O5": "P2O5",
    "HC2H3O2": "HC2H3O2",
    "NH4Cl": "NH4Cl",
    "H2CO3": "H2CO3",
}


def main():
    fails = []
    for formula, expected in GOLDEN.items():
        try:
            got = compound(formula).getName()
        except Exception as e:
            got = f"ERR {type(e).__name__}: {e}"
        if got != expected:
            fails.append((formula, expected, got))

    total = len(GOLDEN)
    print(f"{total - len(fails)}/{total} passing")
    for f, want, got in fails:
        print(f"  MISMATCH {f!r}: got {got!r}, want {want!r}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()