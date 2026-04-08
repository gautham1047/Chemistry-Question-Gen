from chemData import *
from math import gcd
import random

def atomsInCompound(formula: str):
    def parse(i):
        atoms = {}

        while i < len(formula):
            if formula[i] == '(':
                inner_atoms, i = parse(i + 1)

                num = 0
                while i < len(formula) and formula[i].isdigit():
                    num = num * 10 + int(formula[i])
                    i += 1
                num = num or 1

                for k, v in inner_atoms.items():
                    atoms[k] = atoms.get(k, 0) + v * num

            elif formula[i] == ')':
                return atoms, i + 1

            else:
                elem = formula[i]
                i += 1
                while i < len(formula) and formula[i].islower():
                    elem += formula[i]
                    i += 1

                num = 0
                while i < len(formula) and formula[i].isdigit():
                    num = num * 10 + int(formula[i])
                    i += 1
                num = num or 1

                atoms[elem] = atoms.get(elem, 0) + num

        return atoms, i

    result_dict, _ = parse(0)

    return [[atom, count] for atom, count in result_dict.items()]

def getAtomMass(symbol):
    for i in elements:
        if symbol == i[2]:
            if i[2] == "Cl":
                return 35.5
            else:
                return round(float(i[8]))

def findElement(el = "Input an element!"):
    if el == "HNH": raise Exception("Error: HNH")
    for i in elements:
        if i[2] == el:
            return i
    raise Exception("Error: Element not found: " + el)

def findCharge(el):
    el = findElement(el)
    if el[4] in ["n", "s", "m"]:
        group = el[3]
        charge = int(group[0])
        if charge > 4 and charge != 8:
            charge = 8 - charge
    else:
        tmChoices = []
        for i in tmNames:
            if el[2] in i:
                tmChoices.append(int(i[-1]))
        if tmChoices != []:
            charge = random.choice(tmChoices)
        else: charge = random.randint(1,4)

    return charge

def findPolyatomicIon(ion, charge) -> str:
    if ion == "MnO4":
        if charge == 1:  return "permanganate"
        else: return "manganate"
    ion += " " + str(charge)
    name = [k for k, v in polyatomicIons.items() if v == ion]
    try: name = name[0]
    except IndexError: raise Exception(f"enter a valid ion: {ion}")
    return str(name)

def polyatomicCharge(polyatomicIon = "Enter a polyatomic ion!"):
    for i in list(polyatomicCharges.keys()):
        if polyatomicIon == i:
            return int(polyatomicCharges.get(i))
    raise Exception(f"Enter a valid polyatomic ion: {polyatomicIon}")

def compoundToString(compound):
    returnString = ""
    for i in compound:
        num = str(i[1])
        if num == "1": num = ""
        returnString += i[0] + num
    return returnString

def ionizeTernaryIonic(el):
    if el[1].isupper(): index = 1
    elif el[2].isupper(): index = 2
    else: index = 3
    if "NH4" in el:
        if "(NH4)" in el:
            index = el.index(")")
            metal = ["NH4", 1]
            pCharge = int(el[index+1])
            polyatomicIon = el[index+2:]
            return [metal, [polyatomicIon, pCharge]]
        else:
            index = el.index("4")
            metal = ["NH4",1]
            polyatomicIon = [el[index+1:], 1]
            return [metal, polyatomicIon]
    elif "(" in el:
        index = el.index("(")
        # ) will have the index -2
        polyatomicIon = el[index+1:-2]
        try: mNum = int(el[index-1])
        except ValueError: mNum = 1
        pNum = int(el[-1])
        if el[index-1].isdigit():
            metal = el[:index-1]
        else: metal = el[:index]
    else:
        polyatomicIon = el[index:]
        pNum = 1
        try: mNum = int(el[index-1])
        except ValueError: mNum = 1
        if el[index-1].isdigit():
            metal = el[:index-1]
        else: metal = el[:index]
    pCharge = polyatomicCharge(polyatomicIon)
    mCharge = int(pCharge / mNum) * pNum
    return [[metal, mCharge], [polyatomicIon, pCharge]]

def ionicCompoundFromElements(**inputElements):
    for key, value in inputElements.items():
        if key == "m":
            m = value
        else:
            n = value
        
    mCharge = int(m[1])
    nCharge = int(n[1])

    mNum = int(nCharge / gcd(mCharge, nCharge))
    nNum = int(mCharge / gcd(nCharge, mCharge))

    polyatomic = False
    caps = False
    for i in n[0]:
        tempCaps = False
        if i.isdigit():
            polyatomic = True
        if i.isupper():
            tempCaps = True
        if caps and tempCaps:
            polyatomic = True
        elif tempCaps:
            caps = True

    if mNum == 1: mNum = ""
    if nNum == 1: nNum = ""
    elif polyatomic:
        n[0] = f"({n[0]})"

    return f"{m[0]}{mNum}{n[0]}{nNum}"

def findHeatOfFormation(cmpd) -> list:
    small = False
    if cmpd == "Br2":
        cmpd = random.choice(["Br2 (g)", "Br2 (l)"])
        small = True
    elif cmpd == "C":
        cmpd = random.choice(["C (s, diamond)" , "C (s, graphite)"])
        small = True
    elif cmpd == "H2O":
        cmpd = random.choice(["H2O (g)", "H2O (l)"])
        small = True
    elif cmpd == "I2":
        cmpd = random.choice(["I2 (g)", "I2 (s)"])
        small = True
    elif cmpd == "P":
        cmpd = random.choice(["P (s, white)", "P (s, red)"])
        small = True
    elif cmpd == "S":
        cmpd = random.choice([ "S (s, rhombic)", "S (s, monoclinic)"])
        small = True

    if cmpd in heatOfFormationsSmall:
        typeCmpd = "small"
        if small: typeCmpd = "special"
        return [cmpd, heatOfFormationsSmall.get(cmpd), typeCmpd]
    

    if cmpd in heatOfFormationsLarge:
        return [cmpd, heatOfFormationsLarge.get(cmpd), "large"]
    else: 
        value = 0
        while value == 0:
            value = random.choice(list(heatOfFormationsLarge.values()))
        return [cmpd, value, "random"]
