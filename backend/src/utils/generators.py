import random, math
from chemData import *
from src.utils.parsing import findCharge, ionizeTernaryIonic, ionicCompoundFromElements
from src.registry import make_compound

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

    temp = tempK

    unit = random.choice(temps)

    if unit == "K":
        return [temp, unit, temp]
    elif unit == "C":
        return [temp - 273, "degrees " + unit, temp]
    else:
        return [(temp-273) * 9 / 5 + 32, "degrees " + unit, temp]

def randPressureUnit(pressureAtm):
    pressures = ["atm", "kPa", "torr"]

    pressure = pressureAtm

    unit = random.choice(pressures)

    if unit == "atm":
        return [pressure, unit, pressure]
    
    if unit == "kPa":
        return [pressure * 101.3, unit, pressure]
    
    if unit == "torr":
        return [pressure * 760, unit, pressure]    

def randVolumeUnit(volumeL):
    volumes = ["L", "m^3", "mL"]

    volume = volumeL

    unit = random.choice(volumes)

    if unit == "L":
        return [volume, unit, volume]
    
    if unit == "m^3":
        return [volume / 1000, unit, volume]
    
    if unit == "mL":
        return [volume * 1000, unit, volume]    

def randTemp():
    return randTempUnit(random.randint(100,450))

def randPressure():
    return randPressureUnit(round(4 * random.random(), 3))

def randVolume():
    return randVolumeUnit(.5 * random.randint(1,200))

chanceList = [3,3,3,1,0]

def getRandomCompound(polyChance=chanceList[0], acidChance=chanceList[1], biChance=chanceList[2], diChance = chanceList[3], hChance = chanceList[4]):
    chanceList = []
    p = 0
    a = 0
    b = 0
    d = 0
    h =0
    while p < int(polyChance):
        chanceList.append("p")
        p +=1
    while a < int(acidChance):
        chanceList.append("a")
        a +=1
    while b < int(biChance):
        chanceList.append("b")
        b +=1
    while d < int(diChance):
        chanceList.append("d")
        d += 1
    while h < int(hChance):
        chanceList.append("h")
        h += 1

    if chanceList == []:
        chanceList = ["p","a","b", "d", "h"]
    compoundType = random.choice(chanceList)

    bad = True
    while bad:
        if compoundType == "p": #ternary ionic
            pIonList = list(polyatomicIons.items())
            pIon = list(pIonList[random.randint(0, len(pIonList) -1)])
            if pIon[0] == "ammonium":
                if random.randint(0,5) == 1:
                    otherIon = list(pIonList[random.randint(0, len(pIonList) -1)])
                    if otherIon == "ammonium":
                        bad = True
                    else:
                        bad = False
                        mIndex = 99
                        pIndex = 1
                else:
                    otherIon = elements[random.randint(1,108)]
                    if (otherIon[4] == "m" or otherIon[4] == "tm") or otherIon[6] == "Noble Gas":
                        bad = True
                    elif otherIon[6] == "Actinide" or otherIon[6] == "Lanthanide" :
                        bad = True
                    else:
                        bad = False
                        mIndex = 99
                        pIndex = 0
            else:
                otherIon = elements[random.randint(1,108)]
                if (otherIon[4] == "s" or otherIon[4] == "n") or otherIon[6] == "Noble Gas":
                    bad = True
                elif otherIon[6] == "Actinide" or otherIon[6] == "Lanthanide" :
                    bad = True
                else:
                    bad = False
                    mIndex = 99
                    pIndex = 0
        elif compoundType == "a": #acids
            if random.randint(0,2) == 2:
                pIonList = list(polyatomicIons.items())
                pIon = list(pIonList[random.randint(0, len(pIonList) -1)])
                if pIon[0] == "ammonium" or pIon[0] == "peroxide" or pIon[0] == "hydroxide":
                    bad = True
                else:
                    bad = False
                    mIndex = 99
                    pIndex = 2
            else:
                otherIon = elements[random.randint(1,108)]
                if (otherIon[4] == "m" or otherIon[4] == "tm") or otherIon[6] == "Noble Gas" or (otherIon[2] == "O" or otherIon[2] == "H" or otherIon[2] == "Po"):
                    bad = True
                elif otherIon[6] == "Actinide" or otherIon[6] == "Lanthanide" :
                    bad = True
                else:
                    bad = False
                    mIndex = 99
                    pIndex = 3
        elif compoundType == "d": #diatomic
            pIndex = 99
            mIndex = 99
            diatomicAtoms = ["H", "N", "O", "F", "Cl", "Br", "I"]
            atom = random.choice(diatomicAtoms)
            diatomicNames = ["Hydrogen", "Nitrogen", "Oxygen", "Flourine", "Chlorine", "Bromine", "Iodine"]
            index = diatomicAtoms.index(atom)
            return [diatomicNames[index] + " Gas", atom + "2", "diatomic"]
        elif compoundType == "h": # hydrocarbons
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
        else: # binary
            num1 = random.randint(1,108)
            el1 = elements[num1]
            num2 = random.randint(1,108)
            el2 = elements[num2]
            if (el1[4] == "m" or el1[4] == "tm") and (el2[4] == "m" or el2[4] == "tm") or el1[6] == "Noble Gas" or el2[6] == "Noble Gas" or el1 == el2:
                bad = True
            elif el1[6] == "Actinide" or el1[6] == "Lanthanide" or el2[6] == "Actinide" or el2[6] == "Lanthanide":
                bad = True
            else:
                bad = False
            if el1[4] == "s" and el2[4] == "s":
                mIndex = 0
            elif el1[4] == "m" or el1[4] == "tm":
                mIndex = 1
            elif el2[4] == "m" or el2[4] == "tm":
                mIndex = 2
            else: mIndex = 0
            # I am assuming that the combination of a nonmetal and semimetal is always molecular (cause idk what determines it)
            pIndex = 99
        
    if mIndex == 0:
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
        name = name.replace("ao", "o")
        name = name.replace("oo", "o")
        name = name.replace("aa","a")

        if int(amount1) == 1:
            amount1 = ""
        if int(amount2) == 1:
            amount2 = ""

        equation = el1[2] + str(amount1) + el2[2] + str(amount2)

        return [name, equation, "Binary Molecular"]
    elif mIndex == 1 or mIndex == 2:
        if mIndex == 1:
            mElement = el1
            nElement = el2
        elif mIndex == 2:
            mElement = el2
            nElement = el1
        else: print("mIndexing error")
        if mElement[4] == "tm":
            if mElement[2] in tmcharges:
                if len(tmcharges.get(mElement[2]))-1 != 0:
                    index = random.randint(1,len(tmcharges.get(mElement[2]))-1)
                else: index = 0
                mCharge = tmcharges.get(mElement[2])[index]
                mName = mElement[1] + " (" + str(mCharge) + ") / " + str(tmNames.get(mElement[2] + str(mCharge)))
            else:
                mCharge = random.randint(1,4)
                mName = mElement[1] + "(" + str(mCharge) + ")"
        else:
            mCharge = int(mElement[3][0])
            mName = mElement[1]

        nName = ionNames.get(nElement[2])
        if int(nElement[3][0]) < 4:
            nCharge = int(nElement[3][0])
        else: nCharge = 8-int(nElement[3][0])

        mNum = nCharge // math.gcd(nCharge, int(mCharge))
        nNum = int(mCharge) // math.gcd(nCharge, int(mCharge))

        if mNum == 1:
            mNum = ""
        if nNum == 1:
            nNum = ""

        name = str(mName) + " " + str(nName)
        equation = mElement[2] + str(mNum) + nElement[2] + str(nNum)
        return [name, equation, "Binary Ionic"]
    elif pIndex == 0:
        mElement = otherIon

        if mElement[4] == "tm" or mElement[0] == 50 or mElement[0] == 83:
            if mElement[2] in tmcharges:
                if len(tmcharges.get(mElement[2]))-1 != 0:
                    index = random.randint(1,len(tmcharges.get(mElement[2]))-1)
                else: index = 0
                mCharge = int(tmcharges.get(mElement[2])[index])
                mName = mElement[1] + " (" + str(mCharge) + ") / " + str(tmNames.get(mElement[2] + str(mCharge)))
            else:
                mCharge = int(random.randint(1,4))
                mName = mElement[1] + "(" + str(mCharge) + ")"
        elif mElement[4] == "m":
            mCharge = int(mElement[3][0])
            if mCharge > 4 and mCharge != 8: mCharge = 8- mCharge
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

        if mNum == 1:
            mNum = ""
        if int(pNum) == 1:
            pNum = ""
        elif int(mCharge) != 1:
            pSymbol = "(" + pSymbol + ")"

        if mElement[4] == "tm" or mElement[4] == "m":
            name = mName + " " + pName
        else:
            name = pName + " " + mName

        if pSymbol in ["NH4", "(NH4)"]:
            equation = pSymbol + str(pNum) + otherIon[2]
        else:
            equation = otherIon[2] + str(mNum) + pSymbol + str(pNum)
        return [name, equation, "Ternary Ionic"]
    elif pIndex == 1:
        pName = pIon[0]
        pCharge = int(pIon[1][-1])
        pSymbol = pIon[1].split(" ")[0]

        oName = otherIon[0]
        oCharge = int(otherIon[1][-1])
        oSymbol = otherIon[1].split(" ")[0]

        oNum = pCharge // math.gcd(pCharge, int(oCharge))
        pNum = int(oCharge) // math.gcd(pCharge, int(oCharge))

        if oNum == 1:
            oNum = ""
        if pNum == 1:
            pNum = ""
        else:
            pSymbol = "(" + pSymbol + ")"

        name = pName + " " + oName
        equation = pSymbol + str(pNum) + oSymbol + str(oNum)
        return [name, equation, "Ternary Ionic"]
    elif pIndex == 2:
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

        if pCharge == 1:
            pCharge = ""

        equation = "H" + str(pCharge) + pSymbol
        equation = equation.replace("HH2", "H3")
        equation = equation.replace("HH", "H2")
        name = pName + " acid"
        return [name, equation, "Acid"]
    elif pIndex == 3:
        mElement = otherIon
        if int(otherIon[3][0]) < 4:
            mCharge = int(otherIon[3][0])
        else: mCharge = 8-int(otherIon[3][0])
        mName = otherIon[1]

        if mCharge == 1:
            mCharge = ""

        name = "hydro" + acidNames.get(otherIon[2]) + " acid"
        equation = "H" + str(mCharge) + otherIon[2]

        return [name, equation, "Acid"]

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
    # WIP !!
    chances = [dChance, hChance, aChance, bmChance]
    if (all([not i for i in chances])): chances = [1,1,1,1]

    letters = ["d", "h", "a", "b"]
    choices = []
    for i, letter in zip(chances, letters):
        for _ in range(i): choices.append(letter)

    choice = random.choice(choices)

    if choice == "d": return getRandomCompound(0,0,0,1,0)
    if choice == "h": return getRandomCompound(0,0,0,0,1)
    if choice == "a": 
        while True:
            c = getRandomCompound(0,1,0,0,0)
            cmpd = make_compound(c)
            eq = cmpd.equation
            cont = False
            for i in ["NH4", "BO", "Cr", "OH", "Mn", "SiF6", "P", "As", "Si", "Br", "CN", "S2O3"]:
                if i in eq: 
                    cont = True
                    break
            if cont: continue 

            if len(cmpd.compound) == 2: continue

            if cmpd.isHydroCarbon(): continue

            return c
    if choice == "b": 
        eq = randBMForBonds()
        cmpd = make_compound(eq)
        cmpd.refresh()
        return [cmpd.name, cmpd.equation, "binary molecular"]

    raise Exception("Error determining compound")

def randomRx(typeRx = "n/a"):
    # chooose the type of the reaction
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
    if rxType == "synthesis":
        case = random.randint(1,5)
        if bond: case = 3
        if case == 1 or case == 2:
            tmChoice = random.randint(0,1)
            if tmChoice == 0:
                mElement = randElement("m")
                m = [mElement[2], int(mElement[3][0])]
            else:
                mElement = randElement("tm")
                m = [mElement[2], random.randint(1,4)]
            nElement = randElement("n")
            ncharge = int(nElement[3][0])
            if ncharge > 4 and ncharge != 8:
                ncharge = 8-ncharge
            diatomicAtoms = ["H", "N", "O", "F", "Cl", "Br", "I"]
            if nElement[2] in diatomicAtoms:
                n = [nElement[2] + "2", ncharge]
            else:
                n = [nElement[2], ncharge]
            return [[m,n], "s1"]
        if case == 3:
            options = ["SO2", "SO3", "CO2", "N2O3", "N2O5", "P2O3", "P2O5", "As2O3", "As2O5", "NH3"]
            if bond: options = ["SO2", "SO3", "CO2", "NH3"]
            return [[[random.choice(options), 0], ["H2O",0]],"s2"]
        if case == 4 or case == 5:
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
            if oCharge == 1:
                oCharge = ""
            if mCharge == "1":
                mCharge = ""
            mOxide = m[0] + mCharge + "O" + str(oCharge)
            return [[[mOxide,0], ["H2O",0]], "s3"]
    elif rxType == "decomposition":
        case = random.randint(1,5)
        if bond: case = 3
        if case == 1:
            mElement = randElement("m")
            m = [mElement[2], int(mElement[3][0])]
            if m[1] == 1:
                eq = m[0] + "ClO3"
            else:
                eq = m[0] + "(ClO3)" + str(m[1])
            return [[eq,0], "d2"]
        elif case == 2:
            mElement = randElement("m")
            m = [mElement[2], int(mElement[3][0])]
            pCharge = m[1] / math.gcd(2, m[1])
            mCharge = str(int(2 * pCharge / m[1]))
            if pCharge == 1:
                pCharge = ""
            if mCharge == "1":
                mCharge = ""
            if pCharge == "":
                eq = m[0] + mCharge + "CO3"
            else:
                eq = m[0] + mCharge + "(CO3)" + str(pCharge)
            return [[eq,0], "d3"]
        else: #maybe add smth about decomposing hydroxides
            if bond: 
                return [[randBMForBonds(), 0], "d1"]

            cmpd = getRandomCompound(0,0,1,0,0)
            return [[cmpd[1],0], "d1"]
    elif rxType == "combustion":
        case = random.randint(1,2)
        if bond: case = 2
        if case == 1:
            tmChoice = random.randint(0,1)
            if tmChoice == 0:
                mElement = randElement("m")
                m = [mElement[2], int(mElement[3][0])]
            else:
                mElement = randElement("tm")
                m = [mElement[2], random.randint(1,4)]
            return [[m, ["O2",2]], "c1"]
        elif case == 2:
            if bond:
                cmpd = getRandomCompound(0,0,0,0,1)
                return [[cmpd[0], 0], random.choice(["complete combustion", "incomplete combustion"]) ]
            cNum = random.randint(1,10)
            hNum = random.randint(1,20)
            oNum = random.randint(0,5)
            if cNum == 1:
                cNum = ""
            if hNum == 1:
                hNum = ""
            if oNum == 1:
                oNum = ""
            cmpd = f"C{cNum}H{hNum}"
            if oNum != 0:
                cmpd += "O" + str(oNum)
            return [[cmpd,0], random.choice(["complete combustion", "incomplete combustion"])]
    elif rxType == "single replacement":
            case = random.randint(1,2)
            if case == 1:
                mActivitySeries = ["Ag", "Hg", "Cu", "H", "Pb", "Fe", "Zn", "Al", "Mg", "Na", "Ca", "K", "Li"]
                m1 = random.choice(mActivitySeries)
                m2 = m1
                while m2 == m1:
                    m2 = random.choice(mActivitySeries)
                m1Charge = findCharge(m1)
                m2Charge = findCharge(m2)

                if m1 == "Hg" and m1Charge == 1:
                    m1 = "Hg2"
                    m1Charge = 2
                if m2 == "Hg" and m2Charge == 1:
                    m2 = "Hg2"
                    m2Charge = 2

                polyatomic = random.randint(0,1)
                if polyatomic == 1:
                    n = randPolyatomic()
                    nIons = n[1]
                else:
                    nElement = randElement("n")
                    n = [nElement[2], int(nElement[3][0])]
                    nIons = n[1]
                    if nIons > 4 and nIons != 8:
                        nIons = 8 - nIons
                nCharge = int(m2Charge / math.gcd(nIons, m2Charge))
                m2Charge = int(nIons / math.gcd(nIons, m2Charge))
                if nCharge == 1: 
                    nCharge = ""
                    nName = n[0]
                elif polyatomic == 1:
                    nName = f"({n[0]})"
                else: nName = n[0]
                if m2Charge == 1: m2ch = ""
                else: m2ch = m2Charge
                return [[[f"{m2}{m2ch}{nName}{nCharge}",0], [m1, m1Charge]], "sr1", [m2, findCharge(m2[0:2])], [n[0], nIons]]
            elif case == 2:
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

                return [[[f"{m[0]}{n2[:-1]}{mCharge}",0], [n1[:-1], 1]], "sr2", m, [n2[:-1],1]]
    elif rxType == "double replacement":
        repeat = True
        while repeat or (product1.isSoluable() == "inconclusive") or (product2.isSoluable() == "inconclusive"):
            repeat = False
            cmpd1 = getRandomCompound()
            while cmpd1[2] != "Ternary Ionic":
                cmpd1 = getRandomCompound()
            cmpd2 = getRandomCompound()
            while cmpd2[2] != "Ternary Ionic":
                cmpd2 = getRandomCompound()
            cmpd1 = cmpd1[1]
            cmpd2 = cmpd2[1]
            ionized1 = ionizeTernaryIonic(cmpd1)
            ionized2 = ionizeTernaryIonic(cmpd2)
            if ionized1[0] == ionized2[0]:
                repeat = True
            if ionized2[1] == ionized1[1]:
                repeat = True
            product1 = make_compound(ionicCompoundFromElements(m = ionized1[0], n = ionized2[1]))
            product2 = make_compound(ionicCompoundFromElements(m = ionized2[0], n = ionized1[1]))
        return [[[cmpd1[1],0], [cmpd2[1], 0]], "dr", [[make_compound(cmpd1), make_compound(cmpd2)], [product1, product2]]]
    elif rxType == "special":
        if bond:
            Cn = random.randint(1,6)
            Hn = 2 * Cn - 2 * random.randint(0,2) + 2
            if Cn == 1:
                Cn = ""
                Hn = 4
            if Hn == 0: Hn = 2
            other = random.choice(["F2", "Cl2", "Br2", "I2"])
            return [[[make_compound(f"C{Cn if Cn != 1 else ''}H{Hn}"), 0], [make_compound(other)]], "special", "hydrocarbon replacement"]
        specialList = [[[[make_compound("Cu"),0], [make_compound("HNO3"),0]], "special", "dilute", [[make_compound("Cu(NO3)2"),0], [make_compound("NO"), 0], [make_compound("H2O"),0]]],
                       [[[make_compound("Cu"),0], [make_compound("HNO3"),0]], "special", "concentrated", [[make_compound("Cu(NO3)2"),0], [make_compound("NO2"), 0], [make_compound("H2O"),0]]]]
        return random.choice(specialList)


    # this should include: synthesis, decomposition, combustion (hydrocarbon stuff), single replacement, double replacement, 
    # based on that, get the elements
    # return [reactionList, type]