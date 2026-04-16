import random, math
from chemData import *
from src.utils.parsing import findCharge, ionizeTernaryIonic, ionicCompoundFromElements
from src.registry import make_compound, make_reaction

def randUnit(cmpd, moles): # cmpd must be a compound object; returns [value, unit]
    try:
        values = [moles, moles * 22.4, moles * 6.02e23, cmpd.getAtoms(moles), cmpd.getMass(moles)]
    except:
        raise Exception(f"{cmpd} must be a compound object")

    units = ["moles", "L", "particles", "atoms", "g"]

    i = random.randint(0,4)

    return [values[i], units[i], moles]

def randTempUnit(tempK):
    temps = ["K", "C", "F"]
    unit = random.choice(temps)
    if unit == "K":
        return [tempK, unit, tempK]
    elif unit == "C":
        return [tempK - 273, "degrees " + unit, tempK]
    else:
        return [(tempK-273) * 9 / 5 + 32, "degrees " + unit, tempK]

def randPressureUnit(pressureAtm):
    pressures = ["atm", "kPa", "torr"]
    unit = random.choice(pressures)
    if unit == "atm":
        return [pressureAtm, unit, pressureAtm]
    if unit == "kPa":
        return [pressureAtm * 101.3, unit, pressureAtm]
    if unit == "torr":
        return [pressureAtm * 760, unit, pressureAtm]

def randVolumeUnit(volumeL):
    volumes = ["L", "m^3", "mL"]
    unit = random.choice(volumes)
    if unit == "L":
        return [volumeL, unit, volumeL]
    if unit == "m^3":
        return [volumeL / 1000, unit, volumeL]
    if unit == "mL":
        return [volumeL * 1000, unit, volumeL]

def randTemp():
    return randTempUnit(random.randint(100,450))

def randPressure():
    return randPressureUnit(round(4 * random.random(), 3))

def randVolume():
    return randVolumeUnit(.5 * random.randint(1,200))

# ── Random compound generation ──────────────────────────────────────

chanceList = [3,3,3,1,0]

def _pick_compound_type(polyChance, acidChance, biChance, diChance, hChance):
    """Build a weighted list of type letters and pick one."""
    choices = (["p"] * int(polyChance) + ["a"] * int(acidChance) +
               ["b"] * int(biChance) + ["d"] * int(diChance) + ["h"] * int(hChance))
    if not choices:
        choices = ["p", "a", "b", "d", "h"]
    return random.choice(choices)

def _gen_diatomic():
    """Return [name, equation, type] for a random diatomic element."""
    diatomicAtoms = ["H", "N", "O", "F", "Cl", "Br", "I"]
    diatomicNames = ["Hydrogen", "Nitrogen", "Oxygen", "Flourine", "Chlorine", "Bromine", "Iodine"]
    index = random.randint(0, len(diatomicAtoms) - 1)
    return [diatomicNames[index] + " Gas", diatomicAtoms[index] + "2", "diatomic"]

def _gen_hydrocarbon():
    """Return [name, equation, type] for a random hydrocarbon."""
    derivative = bool(random.getrandbits(1))
    if derivative:
        Cn1 = random.randint(1,3)
        O = random.choice(["CO", "COO"])
        Cn2 = random.randint(1,3)
        eq = f"C{Cn1 if Cn1 != 1 else ''}H{2*Cn1+1}{O}C{Cn2 if Cn2 != 1 else ''}H{Cn2*2+1}"
        return [eq, eq, "hydrocarbon"]

    Cn = random.randint(1,5)
    if Cn == 1: Hn = 4
    else: Hn = random.choice([2 * Cn + 2, 2 * Cn, 2 * Cn - 2])
    eq = f"C{Cn if Cn != 1 else ''}H{Hn}"
    return [eq, eq, "hydrocarbon"]

def _pick_binary_elements():
    """Pick two valid elements for a binary compound. Returns (el1, el2, mIndex)."""
    while True:
        num1 = random.randint(1,108)
        el1 = elements[num1]
        num2 = random.randint(1,108)
        el2 = elements[num2]
        if (el1[4] == "m" or el1[4] == "tm") and (el2[4] == "m" or el2[4] == "tm"):
            continue
        if el1[6] == "Noble Gas" or el2[6] == "Noble Gas" or el1 == el2:
            continue
        if el1[6] in ("Actinide", "Lanthanide") or el2[6] in ("Actinide", "Lanthanide"):
            continue

        if el1[4] == "s" and el2[4] == "s":
            mIndex = 0
        elif el1[4] in ("m", "tm"):
            mIndex = 1
        elif el2[4] in ("m", "tm"):
            mIndex = 2
        else:
            mIndex = 0

        return el1, el2, mIndex

def _gen_binary_molecular(el1, el2):
    """Return [name, equation, type] for a binary molecular compound."""
    if int(el2[3][0]) < 4:
        amount1 = int(el2[3][0])
    else: amount1 = 8-int(el2[3][0])
    if int(el1[3][0]) < 4:
        amount2 = int(el1[3][0])
    else: amount2 = 8-int(el1[3][0])

    amount1 = amount1 // math.gcd(amount1, amount2)
    amount2 = amount2 // math.gcd(amount1,amount2)

    prefix1 = prefixes.get(amount1)
    prefix2 = prefixes.get(amount2)
    if prefix1 == "mono":
        prefix1 = ""

    name = prefix1 + el1[1].lower() + " " + prefix2 + (ionNames.get(el2[2])).lower()
    name = name.replace("ao", "o").replace("oo", "o").replace("aa","a")

    eq_a1 = "" if int(amount1) == 1 else str(amount1)
    eq_a2 = "" if int(amount2) == 1 else str(amount2)
    equation = el1[2] + eq_a1 + el2[2] + eq_a2

    return [name, equation, "Binary Molecular"]

def _gen_binary_ionic(el1, el2, mIndex):
    """Return [name, equation, type] for a binary ionic compound."""
    if mIndex == 1:
        mElement, nElement = el1, el2
    else:
        mElement, nElement = el2, el1

    if mElement[4] == "tm":
        if mElement[2] in tmcharges:
            choices = tmcharges.get(mElement[2])
            index = random.randint(1, len(choices)-1) if len(choices) > 1 else 0
            mCharge = choices[index]
            mName = mElement[1] + " (" + str(mCharge) + ") / " + str(tmNames.get(mElement[2] + str(mCharge)))
        else:
            mCharge = random.randint(1,4)
            mName = mElement[1] + "(" + str(mCharge) + ")"
    else:
        mCharge = int(mElement[3][0])
        mName = mElement[1]

    nName = ionNames.get(nElement[2])
    nCharge = int(nElement[3][0])
    if nCharge > 4: nCharge = 8 - nCharge

    mNum = nCharge // math.gcd(nCharge, int(mCharge))
    nNum = int(mCharge) // math.gcd(nCharge, int(mCharge))

    if mNum == 1: mNum = ""
    if nNum == 1: nNum = ""

    name = str(mName) + " " + str(nName)
    equation = mElement[2] + str(mNum) + nElement[2] + str(nNum)
    return [name, equation, "Binary Ionic"]

def _pick_ternary_ions(compoundType):
    """Pick valid ions for a ternary ionic or acid compound.
    Returns (pIon, otherIon, pIndex) or retries until valid."""
    pIonList = list(polyatomicIons.items())

    while True:
        if compoundType == "p":  # ternary ionic
            pIon = list(pIonList[random.randint(0, len(pIonList) - 1)])
            if pIon[0] == "ammonium":
                if random.randint(0,5) == 1:
                    otherIon = list(pIonList[random.randint(0, len(pIonList) - 1)])
                    if otherIon[0] == "ammonium": continue
                    return pIon, otherIon, 1  # two polyatomics
                else:
                    otherIon = elements[random.randint(1,108)]
                    if (otherIon[4] in ("m", "tm")) or otherIon[6] in ("Noble Gas", "Actinide", "Lanthanide"):
                        continue
                    return pIon, otherIon, 0  # ammonium + nonmetal element
            else:
                otherIon = elements[random.randint(1,108)]
                if (otherIon[4] in ("s", "n")) or otherIon[6] in ("Noble Gas", "Actinide", "Lanthanide"):
                    continue
                return pIon, otherIon, 0  # polyatomic + metal element

        elif compoundType == "a":  # acid
            if random.randint(0,2) == 2:
                pIon = list(pIonList[random.randint(0, len(pIonList) - 1)])
                if pIon[0] in ("ammonium", "peroxide", "hydroxide"):
                    continue
                return pIon, None, 2  # polyatomic acid
            else:
                otherIon = elements[random.randint(1,108)]
                if (otherIon[4] in ("m", "tm")) or otherIon[6] in ("Noble Gas", "Actinide", "Lanthanide"):
                    continue
                if otherIon[2] in ("O", "H", "Po"):
                    continue
                return None, otherIon, 3  # binary acid

def _gen_ternary_ionic(pIon, otherIon, pIndex):
    """Return [name, equation, type] for a ternary ionic compound."""
    if pIndex == 0:
        # metal/nonmetal element + polyatomic ion
        mElement = otherIon
        if mElement[4] == "tm" or mElement[0] in (50, 83):
            if mElement[2] in tmcharges:
                choices = tmcharges.get(mElement[2])
                index = random.randint(1, len(choices)-1) if len(choices) > 1 else 0
                mCharge = int(choices[index])
                mName = mElement[1] + " (" + str(mCharge) + ") / " + str(tmNames.get(mElement[2] + str(mCharge)))
            else:
                mCharge = int(random.randint(1,4))
                mName = mElement[1] + "(" + str(mCharge) + ")"
        elif mElement[4] == "m":
            mCharge = int(mElement[3][0])
            if mCharge > 4 and mCharge != 8: mCharge = 8 - mCharge
            mName = mElement[1]
        else:
            mCharge = int(mElement[3][0])
            mName = (ionNames.get(mElement[2])).lower()
            if int(mCharge) > 4 and mCharge != 8:
                mCharge = 8 - mCharge

        pName = pIon[0]
        pCharge = int(pIon[1][-1])
        pSymbol = pIon[1].split(" ")[0]

        mNum = pCharge // math.gcd(pCharge, int(mCharge))
        pNum = int(mCharge) // math.gcd(pCharge, int(mCharge))

        if mNum == 1: mNum = ""
        if int(pNum) == 1: pNum = ""
        elif int(mCharge) != 1: pSymbol = "(" + pSymbol + ")"

        if mElement[4] in ("tm", "m"):
            name = mName + " " + pName
        else:
            name = pName + " " + mName

        if pSymbol in ["NH4", "(NH4)"]:
            equation = pSymbol + str(pNum) + otherIon[2]
        else:
            equation = otherIon[2] + str(mNum) + pSymbol + str(pNum)
        return [name, equation, "Ternary Ionic"]

    elif pIndex == 1:
        # two polyatomic ions (ammonium + other)
        pName = pIon[0]
        pCharge = int(pIon[1][-1])
        pSymbol = pIon[1].split(" ")[0]

        oName = otherIon[0]
        oCharge = int(otherIon[1][-1])
        oSymbol = otherIon[1].split(" ")[0]

        oNum = pCharge // math.gcd(pCharge, int(oCharge))
        pNum = int(oCharge) // math.gcd(pCharge, int(oCharge))

        if oNum == 1: oNum = ""
        if pNum == 1: pNum = ""
        else: pSymbol = "(" + pSymbol + ")"

        name = pName + " " + oName
        equation = pSymbol + str(pNum) + oSymbol + str(oNum)
        return [name, equation, "Ternary Ionic"]

def _gen_acid(pIon, otherIon, pIndex):
    """Return [name, equation, type] for an acid."""
    if pIndex == 2:
        # polyatomic acid
        pName = pIon[0]
        pCharge = int(pIon[1][-1])
        pSymbol = pIon[1].split(" ")[0]

        if "dihydrogen" in pName:
            pSymbol = pSymbol[2:]
            pName = pName.replace("dihydrogen", "")
            pCharge += 2
        elif "hydrogen" in pName:
            pSymbol = pSymbol[1:]
            pCharge += 1
            pName = pName.replace("hydrogen","")

        pName = pName.replace("ite", "ous")
        pName = pName.replace("ate","ic")
        pName = pName.replace("sulf", "sulfur")
        pName = pName.replace("sulfuride","sulfide")
        pName = pName.replace("phosph","phosphor")
        pName = pName.replace("cynanide","hydrocyanic")
        pName = pName.replace("azide", "hydroazoic")

        if pCharge == 1: pCharge = ""

        equation = "H" + str(pCharge) + pSymbol
        equation = equation.replace("HH2", "H3").replace("HH", "H2")
        name = pName + " acid"
        return [name, equation, "Acid"]

    elif pIndex == 3:
        # binary acid
        mElement = otherIon
        mCharge = int(mElement[3][0])
        if mCharge > 4: mCharge = 8 - mCharge
        if mCharge == 1: mCharge = ""

        name = "hydro" + acidNames.get(mElement[2]) + " acid"
        equation = "H" + str(mCharge) + mElement[2]
        return [name, equation, "Acid"]

def _gen_raw_compound(polyChance=chanceList[0], acidChance=chanceList[1], biChance=chanceList[2], diChance=chanceList[3], hChance=chanceList[4]):
    """Generate a random compound as [name, equation, type] (internal)."""
    compoundType = _pick_compound_type(polyChance, acidChance, biChance, diChance, hChance)

    if compoundType == "d":
        return _gen_diatomic()
    if compoundType == "h":
        return _gen_hydrocarbon()

    if compoundType in ("p", "a"):
        pIon, otherIon, pIndex = _pick_ternary_ions(compoundType)
        if pIndex in (0, 1):
            return _gen_ternary_ionic(pIon, otherIon, pIndex)
        else:
            return _gen_acid(pIon, otherIon, pIndex)

    # binary compound
    el1, el2, mIndex = _pick_binary_elements()
    if mIndex == 0:
        return _gen_binary_molecular(el1, el2)
    else:
        return _gen_binary_ionic(el1, el2, mIndex)

def randomCmpd(polyChance=chanceList[0], acidChance=chanceList[1], biChance=chanceList[2], diChance=chanceList[3], hChance=chanceList[4]):
    """Generate a random compound and return it as a compound object.

    This is the public API — absorbs the generation complexity so that
    compound.__init__ can stay simple (just takes a formula string).
    """
    raw = _gen_raw_compound(polyChance, acidChance, biChance, diChance, hChance)
    name, equation, cmpd_type = raw
    cmpd = make_compound(equation)
    # Override the auto-derived name with the generator's name, which
    # is more specific (e.g. includes Roman numerals for TM compounds).
    cmpd.name = name
    return cmpd

# backward-compatible alias (will be removed after all callers migrate)
getRandomCompound = _gen_raw_compound

# ── Random element helpers ──────────────────────────────────────────

typeList = []

def randElement(type = ""):
    if type not in ["b", "m", "tm", "s", "n", "", "ntm"]: raise Exception("enter a valid type. " + type)
    if type == "b":
        good = [6,7,8,9,17,35,53]
        return elements[random.choice(good)]
    if typeList == []:
        typeList.append(None)
        for i in elements:
            if i != "n/a":
                typeList.append(i[4])
    if type == "m":
        metals = [3, 4, 11, 12, 19, 20, 37, 38, 55, 56, 87, 88]
        el = elements[random.choice(metals)]
        return el
    if type == "ntm":
        type = ""
        while True:
            el = random.choice(elements)
            if el != "n/a" and int(el[0]) < 108 and (el[4] == type or type == "") and el[6] != "Noble Gas" and el[4] not in ["tm", "n/a"]:
                return el

    while True:
        el = random.choice(elements)
        if el != "n/a" and int(el[0]) < 108 and (el[4] == type or type == "") and el[6] != "Noble Gas":
            return el

def randPolyatomic():
    ion = random.choice(list(polyatomicIons.values()))
    return [ion[:ion.index(" ")], int(ion[-1])]

# ── Bond-related generators ────────────────────────────────────────

def randBMForBonds():
    while True:
        el1 = randElement("b")[2]
        while (el2 := randElement("b")[2]) == el1: pass

        c = random.randint(1,5)
        if c == 1: c = ""
        eq = f"{el1}{el2}{c}"
        try:
            make_compound(eq).bondEnergy()
        except: continue

        return eq

def randCmpdForBonds(dChance = 0, hChance = 0, aChance = 0, bmChance = 0):
    """Return a random compound object suitable for bond-related problems."""
    chances = [dChance, hChance, aChance, bmChance]
    if (all([not i for i in chances])): chances = [1,1,1,1]

    letters = ["d", "h", "a", "b"]
    choices = []
    for i, letter in zip(chances, letters):
        for _ in range(i): choices.append(letter)

    choice = random.choice(choices)

    if choice == "d": return randomCmpd(0,0,0,1,0)
    if choice == "h": return randomCmpd(0,0,0,0,1)
    if choice == "a":
        while True:
            cmpd = randomCmpd(0,1,0,0,0)
            eq = cmpd.equation
            bad = any(frag in eq for frag in ["NH4", "BO", "Cr", "OH", "Mn", "SiF6", "P", "As", "Si", "Br", "CN", "S2O3"])
            if bad: continue
            if len(cmpd.compound) == 2: continue
            if cmpd.isHydroCarbon(): continue
            return cmpd
    if choice == "b":
        eq = randBMForBonds()
        return make_compound(eq)

    raise Exception("Error determining compound")

# ── Random reaction generation ──────────────────────────────────────
# Each _gen_* function returns a dict with pre-computed skeleton:
#   {"skeleton": [[reactant_cmpds], [product_cmpds]],
#    "typeRx": str, "occurs": bool, "misc": optional}

_DIATOMIC = {"H", "N", "O", "F", "Cl", "Br", "I"}

def _metal_nonmetal_product(m_sym, m_charge, n_sym, n_charge):
    """Compute the product formula for metal + nonmetal synthesis/combustion."""
    g = math.gcd(n_charge, m_charge)
    mNum = n_charge // g
    nNum = m_charge // g
    # strip trailing "2" from diatomic nonmetals
    nonmetal = ""
    if n_sym[-1] == "2":
        for ch in n_sym:
            if not ch.isdigit(): nonmetal += ch
    else:
        nonmetal = n_sym
    mStr = "" if mNum == 1 else str(mNum)
    nStr = "" if nNum == 1 else str(nNum)
    return f"{m_sym}{mStr}{nonmetal}{nStr}"

_S2_PRODUCTS = {
    "SO2": "H2SO3", "SO3": "H2SO4", "CO2": "H2CO3",
    "N2O3": "HNO2", "N2O5": "HNO3", "P2O3": "H3PO3",
    "P2O5": "H3PO4", "As2O3": "H3AsO3", "As2O5": "H3AsO4",
    "NH3": "NH4OH",
}

def _gen_synthesis(bond):
    """Generate a synthesis reaction with pre-computed skeleton."""
    case = random.randint(1,5)
    if bond: case = 3

    if case in (1, 2):
        tmChoice = random.randint(0,1)
        if tmChoice == 0:
            mElement = randElement("m")
            m_sym, m_charge = mElement[2], int(mElement[3][0])
        else:
            mElement = randElement("tm")
            m_sym, m_charge = mElement[2], random.randint(1,4)
        nElement = randElement("n")
        ncharge = int(nElement[3][0])
        if ncharge > 4 and ncharge != 8: ncharge = 8 - ncharge
        n_sym = nElement[2] + "2" if nElement[2] in _DIATOMIC else nElement[2]
        product_eq = _metal_nonmetal_product(m_sym, m_charge, n_sym, ncharge)
        return {"skeleton": [[make_compound(m_sym), make_compound(n_sym)],
                             [make_compound(product_eq)]],
                "typeRx": "s1"}

    if case == 3:
        options = ["SO2", "SO3", "CO2", "N2O3", "N2O5", "P2O3", "P2O5", "As2O3", "As2O5", "NH3"]
        if bond: options = ["SO2", "SO3", "CO2", "NH3"]
        oxide = random.choice(options)
        product = _S2_PRODUCTS[oxide]
        return {"skeleton": [[make_compound(oxide), make_compound("H2O")],
                             [make_compound(product)]],
                "typeRx": "s2"}

    if case in (4, 5):
        tmChoice = random.randint(0,1)
        if tmChoice == 0:
            mElement = randElement("m")
            m = [mElement[2], int(mElement[3][0])]
        else:
            mElement = randElement("tm")
            if mElement[2] in tmNames:
                tmChoices = list(tmNames.keys())
                tmChoice = random.choice(tmChoices)
                while mElement[2] not in tmChoice:
                    tmChoice = random.choice(tmChoices)
                m = [tmChoice[:-1], int(tmChoice[-1])]
            else: m = [mElement[2], random.randint(1,4)]
        oCharge = int(m[1] / math.gcd(2, m[1]))
        mCharge = str(int(2 * oCharge / m[1]))
        if oCharge == 1: oCharge = ""
        if mCharge == "1": mCharge = ""
        mOxide = m[0] + mCharge + "O" + str(oCharge)
        # compute hydroxide product
        metal = mOxide[0:2] if mOxide[1].islower() else mOxide[0]
        lastDigit = mOxide[-1]
        if lastDigit == "O":
            ohCharge = 1 if "2" in mOxide else 2
        elif lastDigit == "3": ohCharge = 3
        else: ohCharge = 4
        product_eq = metal + ("OH" if ohCharge == 1 else f"(OH){ohCharge}")
        return {"skeleton": [[make_compound(mOxide), make_compound("H2O")],
                             [make_compound(product_eq)]],
                "typeRx": "s3"}

def _gen_decomposition(bond):
    """Generate a decomposition reaction with pre-computed skeleton."""
    case = random.randint(1,5)
    if bond: case = 3

    if case == 1:
        mElement = randElement("m")
        m_sym, m_charge = mElement[2], int(mElement[3][0])
        eq = m_sym + "ClO3" if m_charge == 1 else m_sym + "(ClO3)" + str(m_charge)
        # chlorate decomposition -> chloride + O2
        if "(ClO3)" in eq:
            idx = eq.index("(")
            ClO3Num = eq[-1]
        else:
            idx = eq.index("ClO3")
            ClO3Num = ""
        chloride_eq = eq[:idx] + "Cl" + ClO3Num
        return {"skeleton": [[make_compound(eq)],
                             [make_compound(chloride_eq), make_compound("O2")]],
                "typeRx": "d2"}

    elif case == 2:
        mElement = randElement("m")
        m_sym, m_charge = mElement[2], int(mElement[3][0])
        pCharge = m_charge / math.gcd(2, m_charge)
        mch = str(int(2 * pCharge / m_charge))
        if pCharge == 1: pCharge = ""
        if mch == "1": mch = ""
        eq = m_sym + mch + "CO3" if pCharge == "" else m_sym + mch + "(CO3)" + str(pCharge)
        # carbonate decomposition -> oxide + CO2
        if "(CO3)" in eq:
            idx = eq.index("(")
            CO3Num = eq[-1]
        else:
            idx = eq.index("CO3")
            CO3Num = ""
        oxide_eq = eq[:idx] + "O" + CO3Num
        return {"skeleton": [[make_compound(eq)],
                             [make_compound(oxide_eq), make_compound("CO2")]],
                "typeRx": "d3"}

    else:
        if bond:
            eq = randBMForBonds()
        else:
            eq = _gen_raw_compound(0,0,1,0,0)[1]
        cmpd = make_compound(eq)
        el1 = cmpd.compound[0][0]
        try: el2 = cmpd.compound[1][0]
        except IndexError: raise Exception("Invalid compound: " + str(cmpd))
        if el1 in _DIATOMIC: el1 += "2"
        if el2 in _DIATOMIC: el2 += "2"
        return {"skeleton": [[cmpd], [make_compound(el1), make_compound(el2)]],
                "typeRx": "d1"}

def _gen_combustion(bond):
    """Generate a combustion reaction with pre-computed skeleton."""
    case = random.randint(1,2)
    if bond: case = 2

    if case == 1:
        tmChoice = random.randint(0,1)
        if tmChoice == 0:
            mElement = randElement("m")
            m_sym, m_charge = mElement[2], int(mElement[3][0])
        else:
            mElement = randElement("tm")
            m_sym, m_charge = mElement[2], random.randint(1,4)
        product_eq = _metal_nonmetal_product(m_sym, m_charge, "O2", 2)
        return {"skeleton": [[make_compound(m_sym), make_compound("O2")],
                             [make_compound(product_eq)]],
                "typeRx": "c1"}

    elif case == 2:
        if bond:
            raw = _gen_raw_compound(0,0,0,0,1)
            cmpd_eq = raw[1]
        else:
            cNum = random.randint(1,10)
            hNum = random.randint(1,20)
            oNum = random.randint(0,5)
            if cNum == 1: cNum = ""
            if hNum == 1: hNum = ""
            if oNum == 1: oNum = ""
            cmpd_eq = f"C{cNum}H{hNum}"
            if oNum != 0: cmpd_eq += "O" + str(oNum)
        typeRx = random.choice(["complete combustion", "incomplete combustion"])
        co_product = "CO2" if typeRx == "complete combustion" else "CO"
        return {"skeleton": [[make_compound(cmpd_eq), make_compound("O2")],
                             [make_compound(co_product), make_compound("H2O")]],
                "typeRx": typeRx}

_M_ACTIVITY = ["Ag", "Hg", "Cu", "H", "Pb", "Fe", "Zn", "Al", "Mg", "Na", "Ca", "K", "Li"]
_NM_ACTIVITY = ["I", "Br", "Cl", "F"]

def _gen_single_replacement_sr1():
    """Generate a metal single replacement reaction (sr1) with pre-computed skeleton."""
    m1 = random.choice(_M_ACTIVITY)
    m2 = m1
    while m2 == m1:
        m2 = random.choice(_M_ACTIVITY)
    m1Charge = findCharge(m1)
    m2Charge = findCharge(m2)

    if m1 == "Hg" and m1Charge == 1:
        m1 = "Hg2"; m1Charge = 2
    if m2 == "Hg" and m2Charge == 1:
        m2 = "Hg2"; m2Charge = 2

    polyatomic = random.randint(0,1)
    if polyatomic == 1:
        n = randPolyatomic()
        nIons = n[1]
    else:
        nElement = randElement("n")
        n = [nElement[2], int(nElement[3][0])]
        nIons = n[1]
        if nIons > 4 and nIons != 8: nIons = 8 - nIons

    nCharge = int(m2Charge / math.gcd(nIons, m2Charge))
    m2Charge_num = int(nIons / math.gcd(nIons, m2Charge))
    if nCharge == 1:
        nCharge = ""; nName = n[0]
    elif polyatomic == 1:
        nName = f"({n[0]})"
    else: nName = n[0]
    m2ch = "" if m2Charge_num == 1 else m2Charge_num
    reactant_eq = f"{m2}{m2ch}{nName}{nCharge}"

    # compute product: m1 + nonmetal
    nm_clean = n[0].replace("(","").replace(")","")
    product_eq = ionicCompoundFromElements(m=[m1, m1Charge], n=[nm_clean, nIons])

    # activity series check
    m1Index = 1 if m1 == "Hg2" else _M_ACTIVITY.index(m1)
    m2Index = 1 if m2 == "Hg2" else _M_ACTIVITY.index(m2)
    occurs = m1Index >= m2Index

    # build element compounds for m1 and m2
    m1_el = m1
    if m1 in _DIATOMIC: m1_el += "2"
    elif m1 == "Hg2": m1_el = "Hg"
    m2_el = m2
    if m2 in _DIATOMIC: m2_el += "2"
    elif m2 == "Hg2": m2_el = "Hg"

    return {"skeleton": [[make_compound(reactant_eq), make_compound(m1_el)],
                         [make_compound(product_eq), make_compound(m2_el)]],
            "typeRx": "sr1", "occurs": occurs}

def _gen_single_replacement_sr2():
    """Generate a nonmetal single replacement reaction (sr2) with pre-computed skeleton."""
    nActivitySeries = ["I2", "Br2", "Cl2", "F2"]
    n1 = random.choice(nActivitySeries)
    n2 = n1
    while n1 == n2:
        n2 = random.choice(nActivitySeries)

    tmChoice = random.randint(0,1)
    if tmChoice == 0:
        mElement = randElement("m")
        m = [mElement[2], int(mElement[3][0])]
    else:
        mElement = randElement("tm")
        m = [mElement[2], random.randint(1,4)]

    mCharge = m[1]
    if mCharge == 1: mCharge = ""
    reactant_eq = f"{m[0]}{n2[:-1]}{mCharge}"

    # product: metal + n1
    product_eq = ionicCompoundFromElements(m=m, n=[n1[:-1], 1])

    # activity series check
    occurs = _NM_ACTIVITY.index(n2[:-1]) <= _NM_ACTIVITY.index(n1[:-1])

    return {"skeleton": [[make_compound(reactant_eq), make_compound(n1)],
                         [make_compound(product_eq), make_compound(n2)]],
            "typeRx": "sr2", "occurs": occurs}

def _gen_single_replacement():
    """Generate a single replacement reaction."""
    if random.randint(1,2) == 1:
        return _gen_single_replacement_sr1()
    else:
        return _gen_single_replacement_sr2()

def _gen_double_replacement():
    """Generate a double replacement reaction with pre-computed skeleton."""
    repeat = True
    while repeat or (product1.isSoluable() == "inconclusive") or (product2.isSoluable() == "inconclusive"):
        repeat = False
        cmpd1 = _gen_raw_compound()
        while cmpd1[2] != "Ternary Ionic":
            cmpd1 = _gen_raw_compound()
        cmpd2 = _gen_raw_compound()
        while cmpd2[2] != "Ternary Ionic":
            cmpd2 = _gen_raw_compound()
        eq1 = cmpd1[1]
        eq2 = cmpd2[1]
        ionized1 = ionizeTernaryIonic(eq1)
        ionized2 = ionizeTernaryIonic(eq2)
        if ionized1[0] == ionized2[0]: repeat = True
        if ionized2[1] == ionized1[1]: repeat = True
        product1 = make_compound(ionicCompoundFromElements(m=ionized1[0], n=ionized2[1]))
        product2 = make_compound(ionicCompoundFromElements(m=ionized2[0], n=ionized1[1]))

    reactants = [make_compound(eq1), make_compound(eq2)]
    products = [product1, product2]

    # decompose unstable products
    for i, prod in enumerate(products):
        if prod.equation == "NH4OH":
            products.pop(i)
            products.extend([make_compound("NH3"), make_compound("H2O")])
        elif prod.equation == "H2CO3":
            products.pop(i)
            products.extend([make_compound("H2O"), make_compound("CO2")])

    # check if reaction occurs (at least one insoluble product)
    occurs = False
    for prod in products:
        if not prod.isSoluable():
            occurs = True

    return {"skeleton": [reactants, products],
            "typeRx": "dr", "occurs": occurs}

def _gen_special(bond):
    """Generate a special reaction with pre-computed skeleton."""
    if bond:
        Cn = random.randint(1,6)
        Hn = 2 * Cn - 2 * random.randint(0,2) + 2
        if Cn == 1: Cn = ""; Hn = 4
        if Hn == 0: Hn = 2
        other = random.choice(["F2", "Cl2", "Br2", "I2"])
        hydrocarbon = make_compound(f"C{Cn if Cn != '' else ''}H{Hn}")
        halogen = make_compound(other)
        cmpd = hydrocarbon.compound
        if cmpd[0][1] * 2 + 2 == cmpd[1][1]:
            newCmpd = f"C{cmpd[0][1] if cmpd[0][1] != 1 else ''}H{cmpd[1][1]-2}{halogen.equation}"
            products = [make_compound(newCmpd), make_compound("H2")]
        else:
            products = [make_compound(hydrocarbon.equation + halogen.equation)]
        return {"skeleton": [[hydrocarbon, halogen], products],
                "typeRx": "special", "misc": {"label": "hydrocarbon replacement"}}

    dilute = random.choice([True, False])
    label = "dilute" if dilute else "concentrated"
    nox = "NO" if dilute else "NO2"
    return {"skeleton": [[make_compound("Cu"), make_compound("HNO3")],
                         [make_compound("Cu(NO3)2"), make_compound(nox), make_compound("H2O")]],
            "typeRx": "special", "misc": {"label": label}}

def _pick_rx_type(typeRx):
    """Pick a reaction type based on user constraint."""
    rxTypes = ["synthesis", "decomposition", "combustion", "single replacement", "double replacement", "special"]
    rxType = random.choice(rxTypes)
    bond = False
    if typeRx != "n/a" and typeRx in rxTypes or type(typeRx) == list:
        if type(typeRx) == list:
            i = 0
            while (rxType := random.choice(typeRx)) not in rxTypes:
                if (i := i + 1) == 10: raise Exception("bad rx type: " + str(typeRx))
        else: rxType = typeRx
    if typeRx == "bond":
        rxType = random.choice(["synthesis", "decomposition", "combustion", "special"])
        bond = True
    return rxType, bond

def randomRx(typeRx = "n/a"):
    """Generate a random reaction and return it as a reaction object."""
    rxType, bond = _pick_rx_type(typeRx)

    if rxType == "synthesis": data = _gen_synthesis(bond)
    elif rxType == "decomposition": data = _gen_decomposition(bond)
    elif rxType == "combustion": data = _gen_combustion(bond)
    elif rxType == "single replacement": data = _gen_single_replacement()
    elif rxType == "double replacement": data = _gen_double_replacement()
    elif rxType == "special": data = _gen_special(bond)

    return make_reaction(data)


# ── Manual reaction construction ───────────────────────────────────

def custom_reaction(reactants, products, typeRx="custom", label=None):
    """Create a reaction from explicit reactants and products.

    Args:
        reactants: list of formula strings or compound objects
        products:  list of formula strings or compound objects
        typeRx:    reaction type label (default "custom")
        label:     optional descriptor (e.g. "dilute", "concentrated")

    Returns a balanced reaction object, or raises ValueError if it
    cannot be balanced.

    Examples:
        custom_reaction(["H2", "O2"], ["H2O"])
        custom_reaction(["Fe", "O2"], ["Fe2O3"], typeRx="synthesis")
    """
    r_cmpds = [make_compound(r) if isinstance(r, str) else r for r in reactants]
    p_cmpds = [make_compound(p) if isinstance(p, str) else p for p in products]

    data = {"skeleton": [r_cmpds, p_cmpds], "typeRx": typeRx}
    if label:
        data["misc"] = {"label": label}

    rx = make_reaction(data)
    try:
        coeffs = rx.balanceEq()
        if not coeffs or all(c == 0 for c in coeffs):
            raise ValueError("all-zero coefficients")
        # Verify balance: for each element, reactant total must equal product total
        r_total = len(r_cmpds)
        for el_sym in {sym for cmpd in r_cmpds + p_cmpds for sym, _ in cmpd.compound}:
            r_sum = sum(coeffs[i] * c.compoundDict.get(el_sym, 0) for i, c in enumerate(r_cmpds))
            p_sum = sum(coeffs[r_total + i] * c.compoundDict.get(el_sym, 0) for i, c in enumerate(p_cmpds))
            if r_sum != p_sum:
                raise ValueError(f"element {el_sym} not conserved ({r_sum} vs {p_sum})")
    except ValueError:
        raise
    except Exception as e:
        r_str = " + ".join(c.equation for c in r_cmpds)
        p_str = " + ".join(c.equation for c in p_cmpds)
        raise ValueError(f"Cannot balance: {r_str} -> {p_str}") from e

    return rx


def dilute_hno3():
    """Cu + dilute HNO3 -> Cu(NO3)2 + NO + H2O"""
    return custom_reaction(["Cu", "HNO3"], ["Cu(NO3)2", "NO", "H2O"],
                           typeRx="special", label="dilute")


def concentrated_hno3():
    """Cu + concentrated HNO3 -> Cu(NO3)2 + NO2 + H2O"""
    return custom_reaction(["Cu", "HNO3"], ["Cu(NO3)2", "NO2", "H2O"],
                           typeRx="special", label="concentrated")
