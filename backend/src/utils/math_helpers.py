from chemData import *
import random
import math 
from src.utils.generators import randElement

def getAnswer(answer):
    temp = input("Get answer? ")
    if temp == "break":
        return "break"
    else:
        print("\n" + str(answer) + "\n\n")

def getUnit(powerList = []):
    if powerList == []:
        for unit in units:
            p = random.randrange(-2,3)
            powerList.append((unit, p))

    for i, unit in enumerate(units):
        p = powerList[i][1]
        if p == 0: continue
        complexUnits = []
        factor = 0
        n  = random.randrange(1,15)
        prefix = prefixNumbers.get(n)
        complexUnit = prefix + unit + "^" + str(p)
        complexUnits.append(complexUnit)
        prefixFactor = prefixes.get(prefix)
        factor = factor + prefixFactor * p

    finalUnit = " * ".join(complexUnits)
    output = [finalUnit, factor]
    return output

def getPressure(pressureAtm, unit):
    if unit == "atm":
        return pressureAtm
    if unit == "kPa":
        return pressureAtm * 101.3
    if unit == "torr":
        return pressureAtm * 760
    
    raise Exception(f"Error: getPressure({pressureAtm}, {unit})")

def getVolume(volumeL, unit):
    if unit == "L":
        return volumeL
    if unit == "m^3":
        return volumeL / 1000
    if unit == "mL":
        return volumeL * 1000
    
    raise Exception(f"Error: getPressure({volumeL}, {unit})")

def getTemp(tempK, unit):
    if unit == "K":
        return tempK
    if unit == "degrees C":
        return tempK - 273
    if unit == "degrees F":
        return (tempK-273) * 9 / 5 + 32
    
    raise Exception(f"Error: getTemp({tempK}, {unit})")

def solveForVolume(pressure: float, moles: float, temp: int):
    volume = moles * Ratm * temp / pressure
    return volume

def findPeriod(el):
    if el <= 2: return 1
    if el <= 10: return 2
    if el <= 18: return 3
    if el <= 36: return 4
    if el <= 54: return 5
    if el <= 86: return 6
    return 7

def electronConfig(number = 0):
    if number == 0: el = randElement()
    else: el = elements[number]
    numElectrons = int(el[0])
    rList = [el[1]]
    match numElectrons:
        case 1: return ["H", "1s1","1s1"] # H
        case 2: return ["He", "1s2", "1s2"] # He
        case 24: return ["Cr", "[Ar] 4s1 3d5", "1s2 2s2 2p6 3s2 3p6 4s1 3d5"] # Cr
        case 29: return ["Cu", "[Ar] 4s1 3d9", "1s2 2s2 2p6 3s2 3p6 4s1 3d9"] # Cu
        case 57: return ["La", "[Xe] 6s2 5d1", "1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p6 5s2 4d10 5p6 6s2 5d1"] # La
        case 89: return ["Ac", "[Rn] 7s2 6d1", "1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p6 5s2 4d10 6s2 4f14 5d10 6p6 7s2 6d1"] # Ac

    ngConfigs = {"He" : "1s2",
                  "Ne" : "1s2 2s2 2p6",
                  "Ar" : "1s2 2s2 2p6 3s2 3p6",
                  "Kr" : "1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p6",
                  "Xe" : "1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p6 5s2 4d10",
                  "Rn" : "1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p6 5s2 4d10 6s2 4f14 5d10 6p6",
                  "Og" : "1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p6 5s2 4d10 6s2 4f14 5d10 6p6 7s2 5f14 6d10 7p6"}
    
    nobleGasses = [(-1,""), (2, "He"), (10, "Ne"), (18, "Ar"), (36, "Kr"), (54, "Xe"), (86, "Rn"), (118, "Og"), {999, ""}]

    period = findPeriod(numElectrons)

    string = f"[{nobleGasses[period-1][1]}] "
    numElectrons -= nobleGasses[period-1][0]

    level = period // 2 # 1 is <= Ar (sp), 2 is <= Xe (spd), 3 is <= Og (spdf)

    if numElectrons == 0:
        return ngConfigs.get(nobleGasses[period-2][1])

    if level == 1:
        if numElectrons <= 2:
            string += f" {period}s{numElectrons}"
        else:
            string += f" {period}s2 {period}p{numElectrons - 2}"
    if level == 2:
        if numElectrons <= 2:
            string += f" {period}s{numElectrons}"
        elif numElectrons <= 12:
            string += f" {period}s2 {period-1}d{numElectrons - 2}"
        else:
            string += f" {period}s2 {period -1}d10 {period}p{numElectrons - 12}"
    if level == 3:
        if numElectrons <= 2:
            string += f" {period}s{numElectrons}"
        elif numElectrons <= 16:
            string += f" {period}s2 {period - 2}f{numElectrons - 3} {period - 1}d1"
        elif numElectrons <= 26:
            string += f" {period}s2 {period - 2}f14 {period - 1}d{numElectrons - 16}"
        else:
            string += f" {period}s2 {period - 2}f14 {period - 1}d10 {period}p{numElectrons - 26}"

    rList.append(string)
    ng = string[1:3]
    rList.append(ngConfigs.get(ng) + string[4:])
    return rList

def isParamagnetic(el = 0):
    if el == 0: el = random.randint(1,118)
    if el == 1: return True
    if el == 2: return False
    try:
        eConfig = electronConfig(el)[1]
    except: pass
    eConfig = eConfig.split("]")[1]
    nums = []
    for i in range(len(eConfig)):
        if eConfig[i-1].isalpha():
            if i == len(eConfig) - 1 or not eConfig[i+1].isdigit(): nums.append(eConfig[i-1:i+1])
            else: nums.append(eConfig[i-1:i+2])
    
    letterToNum = {"s" : 2, "p" : 6, "d" : 10, "f" : 10}
    for i in nums: 
        n = letterToNum.get(i[0])
        if int(i[1:]) != n:
            return True
    return False

def round_sig(x, sig=4):
   return round(x, sig-int(math.floor(math.log10(abs(x))))-1)

def quantumNumbers(num):
    # assume that the first electron in each orbital has positive spin
    eConfig = electronConfig(num)[1]
    last = eConfig.split(" ")[-1]
    n = int(last[0])
    l = {"s" : 0, "p" : 1, "d" : 2, "f" : 3}.get(last[1])
    electronsInLast = int(last[2])
    ml = -l
    ms = 1/2
    while electronsInLast > 1:
        electronsInLast -= 1
        ml += 1
        if ml == l+1: 
            ms *= -1
            ml = -l
    
    return [n, l, ml, ms]

def getIMF(cmpd1, cmpd2):
    polarity1 = cmpd1.isPolar()
    polarity2 = cmpd2.isPolar()

    if not polarity1 or not polarity2: 
        return ["LD"]

    r = ["LD", "Dipole Dipole"]

    hydrogenBondEls = ["N", "O", "F"]
    if "H" in cmpd1.equation:
        for el in hydrogenBondEls:
            if cmpd2.hasEl(el): r = ["LD", "Hydrogen Bonds"]
    
    if "H" in cmpd2.equation:
        for el in hydrogenBondEls:
            if cmpd1.hasEl(el): r = ["LD", "Hydrogen Bonds"]

    if r == ["LD", "Hydrogen Bonds"] and cmpd1.isHydroCarbon() and cmpd2.isHydroCarbon() and int(cmpd1.getNumEl("C")) >= 8 and int(cmpd2.getNumEl("C")) >= 8:
        return ["Hydrogen Bonds", "LD"]

    return r

# ALL COUNTERPART STUFF IS WIP
def getCounterpartLoop(eq : str):
    i3 = False
    if "I3" in eq: 
        i3 = True
        eq = "I3"
    # list is in form [num of el1 * 10 + valence of el1,...]
    sToL = {"CO2" : [14, 22], "SO2" : [32], "H2O" : [21, 12], "I3" : [31], "SO3" : [42], "NH3" : [13, 31], "ClF3" : [41],
            "CCl4" : [14, 41], "SF4" : [12, 41], "XeF4" : [10, 41], "PCl5" : [13,51], "ClF5" : [61], "SF6" : [12, 61]}
    
    numDicts = {1 : ["H", "F", "Cl", "Br", "I"], 2 : ["O", "S", "Se"], 3 : ["N", "P"], 4 : ["C"], 0 : ["Ar", "Kr", "Xe", "Rn"]}
    l = sToL.get(eq)
    if not eq: raise Exception("only input compounds from the vsepr table!")
    newCmpdList = {}
    for i in l:
        els = numDicts.get(i % 10)
        for _ in range(i // 10):
            if len(set(newCmpdList) & set(els)) == 0 or not bool(random.randint(0,2)): curr = random.choice(els)
            else: curr = random.choice(list(set(newCmpdList) & set(els)))
            if curr in newCmpdList: newCmpdList[curr] += 1
            else: newCmpdList[curr] = 1
    
    newCmpdStr = ""
    for el in list(newCmpdList): newCmpdStr += el + str(newCmpdList.get(el)) * int(newCmpdList.get(el) != 1)

    if i3: newCmpdStr += "-"
    return [newCmpdStr, newCmpdList]

def getCounterpart(eq : str):
    while True:
        counterpart = getCounterpartLoop(eq)
        ones = [counterpart[1][i] == 1 for i in list(counterpart[1])]
        if len(counterpart[1]) != 1 and ones.count(True) == 1: break
    return counterpart[0]

counterpart_starters = ["CO2", "SO2", "H2O", "I3", "SO3", "NH3", "ClF3", "CCl4", "SF4", "XeF4", "PCl5", "ClF5", "SF6"]
