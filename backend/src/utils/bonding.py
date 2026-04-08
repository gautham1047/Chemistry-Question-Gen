from chemData import *
from src.utils.parsing import findElement, polyatomicCharge
from src.registry import make_compound
import random
boxSize = 9

def covalentBondsD(cmpd):
    el = cmpd.equation[0:-1]
    if el == "N": 
        b = 3
        bond = "≡" * boxSize
    elif el == "O": 
        bond = "=" * boxSize
        b = 2
    else: 
        bond = "―" * boxSize
        b = 1
    
    return [[[el, 8 - 2 * b], bond, [el, 8 - 2 * b]]]

def covalentBondsBM(cmpd, charge = 0):
    cmpdList = cmpd.compound
    ones = []
    for i in cmpdList:
        if i[1] == 1: ones.append(i)

    center = min(ones, key = lambda i : ENDict.get(i[0]))

    els = []

    for i in cmpdList:
        for _ in range(i[1]):
            els.append(i[0])

    matrix = [[None for _ in range(0,5)] for _ in range(0,5)]
    if center[0] != "H": matrix[2][2] = [center[0], 8 - 2 * len(els) + 2]
    else: matrix[2][2] = ['H', 0]

    curr = 0
    pattern = [(0,2), (4,2), (2,0), (2,4), (4,0), (0,4), (0,0), (4,4)]
    lines = ["―" * boxSize, "|", "⟍", "⟋"]
    bonds = []
    for i in els:
        if i == center[0]: continue
        x, y = pattern[curr]
        if i == "H": matrix[y][x] = ['H', 0]
        else: matrix[y][x] = [i, 6]

        x = (x+2)//2
        y = (y+2)//2
        index = int(curr > 1)
        if curr > 3: index = 2 + int(curr <= 5)
        matrix[y][x] = f"{lines[index % 4]}"
        bonds.append((x,y))
        curr += 1

    totalValance = -charge
    for el in cmpdList:
        totalValance += int(findElement(el[0])[3][0]) * el[1]

    if totalValance % 2 == 1: raise Exception("The total valence must be even!")

    eLeft = totalValance - 2 * (len(els) -1)

    eUsed = 0
    for line in matrix:
        for i in line:
            if type(i) == list: eUsed += i[1]

    eExcess = eUsed - eLeft
    if cmpd.equation[0] == "B" and cmpd.equation[0:2] != "Br" and cmpdList[0][1] == 1:
        otherEls = cmpdList[1:]
        total = 0
        c = False
        for i in otherEls:
            total += i[1]
            if i[0] not in ["F", "Cl", "Br", "I"]: c = True
        
        if not c and total == 3:
            matrix[2][2][1] = 0
            return matrix
    
    if eExcess > 0:
        bondsNeeded = eExcess // 2
        doubleBonds = []
        needTriple = False
        i = 0
        while bondsNeeded > 0:
            if i < 2:
                try:
                    currBond = bonds[0]
                    i += 1
                except:
                    needTriple = True
                    break
            else: 
                currBond = random.choice(bonds)
            doubleBonds.append(currBond)
            bonds.remove(currBond)
            x, y = currBond
            matrix[y][x] = make_double_bond(matrix[y][x])

            bondsNeeded -= 1
            if bonds == []: 
                needTriple = True
                break

        if needTriple:
            while bondsNeeded > 0:
                currBond = random.choice(doubleBonds)
                doubleBonds.remove(currBond)
                x, y = currBond
                matrix[y][x] = make_triple_bond(matrix[y][x])
                bondsNeeded -= 1
    
    if eExcess < 0:
        matrix[2][2][1] -= eExcess

    #if charge != 0: matrix[0].append(-charge)
    matrix[2][2][1] = abs(matrix[2][2][1])
    return matrix    

def covalentBondsHC(cmpd):
    # these two compounds break the code, so I have to deal with them separately
    if cmpd.equation == "C2H2": return [[None for i in range(0,7)],[None for i in range(0,7)],[["H", 0], "―" * boxSize, ["C", 0], "≡" * boxSize, ["C",0], "―" * boxSize, ["H",0]],[None for i in range(0,7)],[None for i in range(0,7)]]
    if cmpd.equation == "C2H4": return [[None, None, ["H",0], None, ["H", 0], None, None],[None, None, "|", None, "|", None, None],[["H", 0], "―" * boxSize, ["C", 0], "=" * boxSize, ["C",0], "―" * boxSize, ["H",0]],[None for i in range(0,7)],[None for i in range(0,7)]]

    cmpdList = cmpd.compound
    if cmpd.uniqueEls() == set(["H", "C"]): # not hydrocarbon derivative
        Cn = cmpdList[0][1]
        Hn = cmpdList[1][1]
        if Cn * 2 + 2 == Hn:
            t = "alkane"
        elif Cn * 2 == Hn:
            t = "alkene"
        elif Cn * 2 - 2 == Hn:
            t = "alkyne"
        else:
            raise Exception("You must input a valid hydrocarbon (alkane, alkene, alkyne)!")
        
        matrix = [[None for i in range(0, Hn + 1)] for j in range(0,5)]
        matrix[0] = [None if i % 2 == 1 or i == 0 or i == Hn else ["H", 0] for i in range(0,Hn + 1)]
        matrix[1] = [None if i % 2 == 1 or i == 0 or i == Hn else "|" for i in range(0,Hn + 1)]
        matrix[2] = ["―" * boxSize if i % 2 == 1  else ["C", 0] for i in range(0,Hn + 1)]
        matrix[3] = matrix[1].copy()
        matrix[4] = matrix[0].copy()
        matrix[2][0] = ["H", 0]
        matrix[2][Hn] = ["H", 0]
        if t == "alkane": return matrix

        for i in range(5):
            matrix[i].append(matrix[i][Hn-1])
            matrix[i].append(matrix[i][Hn])
            matrix[i][Hn] = matrix[i][Hn-2]

        horizontal_bonds = [2*i+3 for i in range(Cn-2)]
        bond = random.choice(horizontal_bonds)
        x, y = bond, 2
        matrix[y][x] = make_double_bond(matrix[y][x])
        matrix[1][x-1] = None
        matrix[1][x+1] = None
        matrix[0][x-1] = None
        matrix[0][x+1] = None

        if t == "alkene": return matrix
        for i in range(5):
            matrix[i].append(matrix[i][Hn+1])
            matrix[i].append(matrix[i][Hn+2])
            if type(matrix[i][Hn]) in [list]: matrix[i][Hn+2] = matrix[i][Hn].copy()
            else: matrix[i][Hn+2] = matrix[i][Hn]

        matrix[0][Hn+2] = ["H",0]
        matrix[1][Hn+2] = "|"

        matrix[y][x] = make_triple_bond(matrix[y][x])
        matrix[3][x-1] = None
        matrix[3][x+1] = None
        matrix[4][x-1] = None
        matrix[4][x+1] = None

        return matrix
    elif cmpd.uniqueEls() == set(["H", "C", "O"]):
        parts = -1
        for i in ["COO", "CO"]:
            if i in cmpd.equation:
                parts = cmpd.equation.split(i)
                parts.insert(1, create_parts(i))
                break
        if parts == -1: raise Exception(f"Enter a valid hydrocarbon derivative. cmpd: {cmpd.equation}")

        for i in [0,2]:
            try: Cn = int(parts[i][1])
            except: Cn = 1
            parts[i] = create_parts(Cn, i // 2)

        return combine_bond_matricies(parts[0], parts[1], parts[2])
    else:
        uniqueEls = cmpd.uniqueEls()
        if "C" in uniqueEls and "H" in uniqueEls:
            otherCmpds = [i for i in cmpdList if i[0] not in ["C", "H"]]
            for i in otherCmpds:
                if i[0] not in ["F", "Cl", "Br", "I"]: raise Exception(f"Enter a valid hydrocarbon derivative. cmpd: {cmpd.equation}")
        else: raise Exception(f"Enter a valid hydrocarbon derivative. cmpd: {cmpd.equation}")

        otherTotal = 0
        for i in otherCmpds:
            otherTotal += i[1]

        for i in cmpdList:
            if i[0] == "C": c = i[1]
            if i[0] == "H": h = i[1] + otherTotal
        
        matrix = covalentBondsHC(make_compound(f"C{c}H{h}"))
        for i in range(len(matrix)):
            line = matrix[i]
            for j in range(len(line)):
                curr = line[j]
                if curr == None or type(curr) == str: continue
                matrix[i][j] = matrix[i][j].copy()
        hPos = []
        for y in range(len(matrix)):
            row = matrix[y]
            for x in range(len(row)):
                curr = row[x]
                if curr == ["H", 0]: hPos.append((x, y))

        replacementsNeeded = 0
        replacements = []
        for i in otherCmpds:
            for _ in range(i[1]):
                replacements.append(i[0])
            replacementsNeeded += i[1]

        while replacementsNeeded:
            h = random.choice(hPos)
            hPos.remove(h)
            x, y = h
            matrix[y][x][0] = replacements[0]
            replacements.pop(0)
            replacementsNeeded -= 1

        return matrix

def covalentBondsA(cmpd):
    eq = cmpd.equation
    if eq == "HC2H3O2": return ["acetate", "temp"]
    if eq == "HC7H5O2": return ["benzoate","temp"]
    if eq == "HN3": return ["azide", "temp"]
    if eq == "H2C4H4O6": return ["tartrate", "temp"]
    if eq == "H2C2O4": return ["oxalate","temp"]
    if eq == "HCN": return ["cyanate", "temp"]
    if eq == "H2O2": return ["peroxide", "temp"]
    if eq == "H2S2O3": return ["thiocynanate", "temp"]

    for i in ["NH4", "BO", "Cr", "OH", "Mn", "SiF6", "P", "As", "Si"]:
        if i in eq: return ["bad acid"] 

    if len(cmpd.compound) == 2: return ["bad acid"]

    ion = eq[int(eq[1].isdigit()) + 1:]
    charge = polyatomicCharge(ion)

    right = [[None, None], [None, None], [["H", 0], "―" * boxSize], [None, None], [None, None]]
    left = [[None, None], [None, None], [None, None], [None, None], [None, None]]
    if charge > 1: 
        left = [[None, None], [None, None], ["―" * boxSize, ["H", 0]], [None, None], [None, None]]        

    middle = covalentBondsBM(make_compound(ion), -charge)

    if middle[2][0] == None:
        middle = [[l[2], l[3], l[4]] for l in middle]
    if middle[2][2] == None:
        middle = [[l[0]] for l in middle]

    return combine_bond_matricies(right, middle, left)

def make_double_bond(string):
    if "|" in string: return f"{'||': ^9}"
    if "―" in string: return "=" * boxSize
    if "⟋" in string: return f"{'⟋⟋': ^9}"
    if "⟍" in string: return f"{'⟍⟍': ^9}"

def make_triple_bond(string):
    if "|" in string: return f"{'|||': ^9}"
    if "=" in string: return "≡" * boxSize
    if "⟋⟋" in string: return f"{'⟋⟋⟋': ^9}"
    if "⟍⟍" in string: return f"{'⟍⟍⟍': ^9}"

def print_matrix(l : list):
    s = ""
    for line in l: s += "".join([" " * boxSize if i == None else f"{str(i): ^9}" for i in line]) + "\n"
    return s

def create_parts(Cn, d = 0):
    if Cn == "CO": return [ [None, ["O", 4], None], [None,  "||", None], ["―" * boxSize, ["C", 0], "―" * boxSize], [None,  None, None], [None, None, None] ]
    if Cn == "COO": return [ [None, ["O", 4], None, None, None], [None,  "||", None, None, None], ["―" * boxSize, ["C", 0], "―" * boxSize, ["O", 4], "―" * boxSize], [None, None, None, None, None], [None, None, None, None, None] ]
    try: Cn = int(Cn)
    except: raise Exception("enter an int! (or 'COO' or 'CO')")

    # d = 0 means H is on the left, d = 1 means H is on the right
    if d not in [0,1]: raise Exception("Enter a valid direction!")
    Hn = 2 * Cn + 1
    matrix = [[None for i in range(Hn)] for j in range(5)]
    matrix[0] = [["H", 0] if i % 2 == 0 and i != (Hn -1) * d else None for i in range(Hn)]
    matrix[1] = ["|" if i % 2 == 0 and i != (Hn -1) * d else None for i in range(Hn)]
    matrix[2] = [["C", 0] if i % 2 == 0 and i != (Hn -1) * d else "―" * boxSize for i in range(Hn)]
    matrix[2][(Hn-d) % Hn] = ["H", 0]
    matrix[3] = matrix[1].copy()
    matrix[4] = matrix[0].copy()
    return matrix

def combine_bond_matricies(m1, m2, m3):
    matrix = [None for i in range(5)]
    for i in range(5):
        m = m1[i].copy()
        m.extend(m2[i])
        m.extend(m3[i])
        matrix[i] = m

    return matrix
