from src.utils.parsing import *
from src.utils.generators import getRandomCompound
from src.utils.bonding import *
from src.registry import set_compound_factory, make_compound, make_reaction
from math import gcd

class compound:
    def __init__(self, compoundList = "RANDOM", charge = 0):
        if compoundList == "e-":
            self.charge = -1
            self.K_sp = None
            self.name = "electron"
            self.equation = "e-"
            self.type = "electron"
            self.compound = []
            self.temp = 0
            return None

        self.charge = charge
        self.K_sp = None
        if compoundList == "RANDOM": compoundList = getRandomCompound()
        if type(compoundList) == list:
            self.name = compoundList[0]
            self.equation = compoundList[1]
            try: self.type = compoundList[2]
            except IndexError: self.type = "n/a"
        elif type(compoundList) == str:
            if "_" in compoundList:
                compoundList, self.charge = compoundList.split("_")
                self.charge = int(self.charge)
            if compoundList[-1] == "-": 
                self.charge = -1
                compoundList = compoundList[:-1]
            self.name = "Unknown"
            self.equation = compoundList
            self.type = "Unknown"
        
        if self.type == "element": # if the input is a string this is never run?
            self.equation = self.name
            self.compound = [self.equation,1]
            if self.equation in ["H", "N", "O", "F", "I", "C", "Br", "Cl"]:
                self.compound[1] = 2
                self.equation += "2"
            elif self.equation in ["H2", "N2", "O2", "F2", "I2", "C2", "Br2", "Cl2"]:
                self.compound = [self.compound[0:-1], 2]
            elif self.equation == "Hg2":
                self.equation = "Hg"
                self.compound = [["Hg",1]]
        else: self.compound = atomsInCompound(self.equation)

        if type(self.compound[0]) == str:
            self.compound = [self.compound]

        self.compoundDict = {}
        for i in self.compound: 
            if i[0] in self.compoundDict: self.compoundDict[i[0]] += i[1]
            else: self.compoundDict[i[0]] = i[1]

        self.temp = 0

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if self.equation == "e-": return "e-"
        return self.equation + ("_" + str(self.charge)) * (self.charge != 0)

    def getEq(self): # why did i even make this method?!
        eq = ""
        for i in self.compoundDict:
            num = self.compoundDict[i]
            if num == 1:
                num = ""
            eq += i[0] + str(num)
        return eq
            
    def getMolarMass(self):
        mass = 0
        for i in self.compound:
            if type(i) == list:
                mass += getAtomMass(i[0]) * i[1]
            else: mass += getAtomMass(self.compound[0]) * self.compound[1]
        return mass
    
    def getParticles(self, moles = 1):
        return moles * 6.02e+23
    
    def getMass(self, moles = 1):
        return moles * self.getMolarMass()
    
    def getAtoms(self, moles = 1):
        atomsPerMolecule = 0
        try:
            for i in self.compound:
                atomsPerMolecule += i[1]
        except IndexError: return 6.02e23 * self.compound[1]
        except TypeError: return 6.02e23 * self.compound[1]
        return self.getParticles(moles) * atomsPerMolecule
    
    def percentComposition(self):
        MM = self.getMolarMass()
        returnList = []
        for i in self.compoundDict:
            nameI = i[0]
            percentI = getAtomMass(i) * self.compoundDict[i] * 100 / MM
            returnList.append([nameI, percentI])
        return returnList

    def getName(self):
        name = self.name
        if "\ " in name:
            name = name.split("\ ")[1]
        return name
    
    def getNameFromEq(self, eqOveride = None, cmpdOverride = None):
        if eqOveride == None or cmpdOverride == None: 
            eq = self.equation
            cmpd = self.compound
        else: 
            eq = eqOveride
            cmpd = cmpdOverride
        SpecialCmpds = {"NH3": "ammonia", "H2O": "water", "C2H6O" : "ethanol", 
                        "CH3CH2OH" : "ethanol", "C2H5OH" : "ethanol", "CHCl3" : "Chloroform",
                        "CH3COCH3" : "acetone", "C6H6" : "benzene", "CH4" : "methane",
                        "CH3OH" : "methanol", "C6H12O6" : "glucose", "C12H22O11" : "sucrose",
                        "C6H6O" : "phenol", "C6H5OH" : "phenol", "C6H5NO2" : "nitrobenzene",
                        "C10H16O" : "camphor"}

        uniqueEls = []
        for i in cmpd:
            if type(i) != int and i[0] not in uniqueEls: uniqueEls.append(i[0])
        if eq in SpecialCmpds.keys(): return SpecialCmpds.get(eq)
        if len(cmpd) == 1 or type(cmpd[1]) == int: 
            diatomics = {"H2": "hydrogen", "N2": "nitrogen", "O2": "oxygen", "F2": "flourine", "Cl2": "chlorine", "Br2": "bromine", "I2": "iodine"}
            if eq in diatomics.keys(): return diatomics.get(eq) + " gas"
            
            el = findElement(eq)
            return el[1]
        if "C" in uniqueEls and "H" in uniqueEls: return eq
        elif len(cmpd) == 2 and "(" not in eq:
            if eq[0] == "H" and not eq[1].islower():
                return "hydro" + acidNames.get("".join([i for i in eq if i != "H" and not i.isdigit()])) + " acid"
            ionic = False
            nonmetals = []
            for i in uniqueEls:
                el = findElement(i)
                if el[4] in ["m", "tm"]:
                    ionic = True
                    metal = i
                else: nonmetals.append(i)
            if ionic: 
                metal = findElement(metal)
                metalName = metal[1]
                nonmetalName = ionNames.get(nonmetals[0])
                if metal[4] == "tm":
                    try: mCharge = ionizeTernaryIonic(eq)[0][1] # takes care of peroxide and azide
                    except:
                        nonmetal = findElement(nonmetals[0])
                        nmCharge = int(nonmetal[3][0])
                        if nmCharge > 4: nmCharge = 8 - nmCharge
                        mCharge = int(nmCharge * cmpd[1][1] / cmpd[0][1])
                    tmFix = f" ({mCharge}) "
                else: tmFix = " "
                return metalName + tmFix + nonmetalName
            el1 = eq[0]
            el2 = ""
            foundDigitOrUpper = False
            coeffecients = []
            for i in eq[1:]:
                if i.isdigit() or i.isupper():
                    foundDigitOrUpper = True
                elif not foundDigitOrUpper: el1 += i
                if foundDigitOrUpper and not i.isdigit(): 
                    el2 += i
                if i.isdigit(): coeffecients.append(int(i))
            idealCoefficients = [findCharge(el1), findCharge(el2)]
            if set(idealCoefficients) == set(coeffecients):
                el1 = findElement(el1)
                el2 = findElement(el2)
                if el1[7] > el2[7]: 
                    firstEl = el2
                    lastEl = el1
                else: 
                    firstEl = el1
                    lastEl = el2
                lastEl = ionNames.get(lastEl[2])
                return firstEl[1] + " " + lastEl
        else:
            # check for acids
            if eq[0] == "H" and not eq[1].islower():
                ion = ""
                if eq[1].isdigit(): index = 2
                else: index = 1
                ion = eq[index:]
                if eq[1].isdigit(): charge = int(eq[1])
                else: charge = 1
                name = findPolyatomicIon(ion,charge)
                name = name.replace("ite", "ous")
                name = name.replace("ate","ic")
                name = name.replace("sulf", "sulfur")
                name = name.replace("sulfuride","sulfide")
                name = name.replace("phosph","phosphor")
                name = name.replace("cynanide","hydrocyanic")
                name = name.replace("azide", "hydroazoic")
                return name + " acid"
            try:
                ionized = ionizeTernaryIonic(eq)
                ion = findPolyatomicIon(ionized[1][0], ionized[1][1])
                metal = ionized[0][0]
                if metal == "NH4": return "ammonium " + ion
                metal = findElement(metal)
                if metal[4] == "tm": 
                    tmFix = f" ({ionized[0][1]}) "
                else: tmFix = " "
                return metal[1] + tmFix + ion
            except: pass
        return eq

    def refresh(self):
        self.name = self.getNameFromEq()
        self.compound = atomsInCompound(self.equation)
        if len(self.compound) == 1: self.type = "element"

    def multCompound(self, factor):
        toMake = []
        for i in self.compound:
            newNum = i[1] * factor
            toMake.append([i[0], newNum])
        for i in self.compoundDict:
            self.compoundDict[i] *= factor
        self.compound = toMake

    def isSoluable(self):
        if self.equation in ["O2", "CO2", "NH3", "N2", "F2", "Cl2", "I2", "He", "Ne", "Ar", "Kr", "Xe", "Rn", "H2O"]:
            return False
        if ("Li" in self.equation) or ("Na" in self.equation) or ("K" in self.equation and "Kr" not in self.equation) or ("Rb" in self.equation) or ("Cs" in self.equation) or ("Fr" in self.equation): return True
        elif ("NH4" in self.equation): return True
        elif "NO4" in self.equation or "NO3" in self.equation or "C2H3O2" in self.equation or "ClO3" in self.equation or "ClO4" in self.equation: return True
        elif "SO4" in self.equation and "HSO4" not in self.equation:
            if ("Ca" in self.equation) or ("Ba" in self.equation) or ("Sr" in self.equation) or ("Ag" in self.equation) or ("Plumbous" in self.name) or ("Mercurous" in self.name): return False
            else: return True
        elif "OH" in self.equation: return False
        elif ("CO3" in self.equation and "HCO3" not in self.equation) or "CrO4" in self.equation or "C2O4" in self.equation or ("PO4" in self.equation and "HPO4" not in self.equation and "H2PO4" not in self.equation): return False
        elif len(self.compound) == 2:
            if "Cl" in self.equation or "Br" in self.equation or ("I" in self.equation and "Ir" not in self.equation and "In" not in self.equation):
                if ("Ag" in self.equation) or ("Plumbous" in self.name) or ("Mercurous" in self.name): return False
                else: return True
            elif "F" in self.equation and "Fe" not in self.equation and "Fr" not in self.equation and "Fm" not in self.equation and "Fl" not in self.equation: return False
            elif "S" in self.equation:
                if ("Ca" in self.equation) or ("Ba" in self.equation) or ("Sr" in self.equation) or ("Mg" in self.equation) or ("Be" in self.equation) or ("Ra" in self.equation): return True
                else: return False
            else: return "inconclusive"
        else: return "inconclusive"

    def setTemp(self, temp):
        self.temp = temp
    
    def raiseTemp(self, finalTemp, moles, fp, bp, heatOfFusion, heatOfVaporization, sSpecificHeat, lSpecificHeat, gSpecificHeat): # for example, water would be (finalTemp, moles, 0, 100, 6.01, 40.7, 1.7, 4.18, 2.1)
        if self.temp < fp: startState = "solid"
        elif self.temp < bp: startState = "liquid"
        else: startState = "gas"

        if finalTemp < fp: finalState = "solid"
        elif finalTemp < bp: finalState = "liquid"
        else: finalState = "gas"

        if finalTemp == self.temp:
            if finalTemp == fp: return heatOfFusion * moles
            if finalTemp == bp: return heatOfVaporization * moles
            return 0

        heat = 0
        
        mass = self.getMass(moles)

        #print(f"startState: {startState}, finalState: {finalState}")

        if startState == finalState: 
            if startState == "solid": return sSpecificHeat * mass * (finalTemp - self.temp) / 1000
            if startState == "liquid": return lSpecificHeat * mass * (finalTemp - self.temp) / 1000
            if startState == "gas": return gSpecificHeat * mass * (finalTemp - self.temp) / 1000

        if startState == "solid": heat += heatOfFusion * moles + sSpecificHeat * mass * (fp - self.temp) / 1000 
        if finalState == "gas": heat += heatOfVaporization * moles + gSpecificHeat * mass * (finalTemp - bp) / 1000 
        if startState == "gas": heat -= heatOfVaporization * moles + gSpecificHeat * mass * (self.temp - bp) / 1000 
        if finalState == "solid": heat -= heatOfFusion * moles + sSpecificHeat * mass * (fp - finalTemp) / 1000 
        if startState == "solid" and finalState == "liquid": heat += lSpecificHeat * mass * (finalTemp - fp) / 1000 
        if startState == "gas" and finalState == "liquid": heat -= lSpecificHeat * mass * (bp - finalTemp) / 1000 
        if startState == "liquid" and finalState == "solid": heat -= lSpecificHeat * mass * (self.temp - fp) / 1000 
        if startState == "liquid" and finalState == "gas": heat -= lSpecificHeat * mass * (bp - self.temp) / 1000 # this is being added, since finalTemp - bp is negative 

        self.temp = finalTemp
        return heat # heat is the amount of heat being used (if its negative, its how much heat is being released) in kJ
    
    def heat(self, heatSupplied, moles, fp, bp, heatOfFusion, heatOfVaporization, sSpecificHeat, lSpecificHeat, gSpecificHeat): # for example, water would be (heatSupplied, moles, 0, 100, 6.01, 40.7, 1.7, 4.18, 2.1)
        if self.temp < fp: startState = "solid"
        elif self.temp < bp: startState = "liquid"
        else: startState = "gas"

        if startState == "solid" and sSpecificHeat == 0: startState = "liquid"
        if startState == "liquid" and lSpecificHeat == 0: startState = "gas"

        mass = self.getMass(moles)
        # print(startState)
        if heatSupplied > 0: # for heating
            if startState == "solid":
                # print("s")
                finalTemp = heatSupplied / (mass * sSpecificHeat) + self.temp
                # print(f"finalTemp: {finalTemp}")
                if finalTemp < fp:
                    self.temp = finalTemp
                    return finalTemp
                heatSupplied -= mass * sSpecificHeat * (fp - self.temp)
                startState = "liquid"
                self.temp = fp
                    
                heatSupplied -= heatOfFusion * moles * 1000
                if heatSupplied <= 0: 
                    return fp
            # print(f"heatSupplied: {heatSupplied}")
            
            if startState == "liquid":
                # print("l")
                finalTemp = heatSupplied / (mass * lSpecificHeat) + self.temp
                # print(f"finalTemp: {finalTemp}")
                if finalTemp < bp:
                    self.temp = finalTemp
                    return finalTemp
                heatSupplied -= mass * lSpecificHeat * (bp - self.temp)
                startState = "gas"
                self.temp = bp

                heatSupplied -= heatOfVaporization * moles * 1000
                # print(f"heatSupplied: {heatSupplied}")
                if heatSupplied <= 0:
                    return bp
            
            # print("g")
            finalTemp = heatSupplied / (mass * gSpecificHeat) + self.temp
            self.temp = finalTemp
            return finalTemp
        else: # for cooling
            if startState == "gas":
                # print("g")
                finalTemp = heatSupplied / (mass * gSpecificHeat) + self.temp
                if finalTemp > bp:
                    self.temp = finalTemp 
                    return finalTemp
                heatSupplied += mass * gSpecificHeat * (self.temp - bp)
                startState = "liquid"
                self.temp = bp
            
                heatSupplied += heatOfVaporization * moles * 1000
                if heatSupplied > 0:
                    self.temp = bp
                    return bp
            
            if startState == "liquid":
                # print("l")
                finalTemp = heatSupplied / (mass * lSpecificHeat) + self.temp
                if finalTemp > fp:
                    self.temp = finalTemp
                    return finalTemp
                heatSupplied += mass * lSpecificHeat * (self.temp - fp)
                startState = "solid"
                self.temp = fp
            
                heatSupplied += heatOfFusion * moles * 1000
                if heatSupplied > 0:
                    self.temp = fp
                    return fp

            # print("s")
            # Guard against division by zero when sSpecificHeat is 0
            if sSpecificHeat == 0:
                # If no solid specific heat data, substance stays at freezing point
                self.temp = fp
                return fp
            finalTemp = heatSupplied / (mass * sSpecificHeat) + self.temp
            self.temp = finalTemp
            return finalTemp
    
    def isMolecular(self):
        for el in self.compound:
            el = findElement(el[0])
            if el[4] != "n": return False

        return "NH4" not in self.equation
    
    def isDiatomic(self):
        return self.equation in ["H2", "N2", "O2", "F2", "Cl2", "Br2", "I2"]
    
    def isHydroCarbon(self):
        return self.equation != "CO" and self.uniqueEls() == set(["H", "C"]) or self.uniqueEls() in [set(["H", "C", el]) for el in ["O", "F", "Cl", "Br", "I"]]
    
    def isAcid(self):
        return self.equation[0] == "H" and self.equation[int(self.equation[1].isdigit()) + 1:] in polyatomicCharges

    def isBinaryMolecular(self):
        return len(self.uniqueEls()) == 2 and self.isMolecular()

    def isTernaryIonic(self):
        if "(" in self.equation: return True
        if self.equation[-2:] == "O2": return True
        pass

    # incomplete
    def hasPeroxide(self):
        if "O2" not in self.equation or not self.isIonic(): return False
        if "(O2)" in self.equation: return True
        if len(self.uniqueEls()) != 2: return False
        metal = findElement(self.compound[0][0])

        charge = metal[3]
        if charge[-1] == "b": return False # i dont even want to deal with this
        else: charge = int(charge[0])

        nmCharge = charge

    def isElement(self):
        return all([i.islower() and not i.isdigit() for i in self.equation[1:]])

    def setEq(self, eq):
        self.equation = eq

    def uniqueEls(self):
        unique = set([])
        for i in self.compound:
            if i[0] not in unique: unique.add(i[0])

        return unique

    def covalentBonds(self):
        if self.isElement():
            return [self.equation]

        if self.isDiatomic():
            return covalentBondsD(self)
        
        if self.isAcid():
            return covalentBondsA(self)
        
        if self.isHydroCarbon():
            return covalentBondsHC(self)

        try: return covalentBondsBM(self, self.charge)
        except: raise Exception("No lewis dot structure found")

    def getCovalentBonds(self):
        try:
            matrix = self.covalentBonds()
        except:
            raise Exception(f"{self.equation} is not a covalent compound")
        
        bonds = []
        for i, line in enumerate(matrix):
            for j, entry in enumerate(line):
                if entry == None: continue
                if "|" in entry:
                    num = entry.count("|")
                    top = matrix[i-1][j]
                    bottom = matrix[i+1][j]

                if "―" in entry or "=" in entry or '≡' in entry:
                    num = {"―" : 1, "=" : 2, "≡" : 3}.get(entry[0])
                    top = matrix[i][j+1]
                    bottom = matrix[i][j-1]

                try: bonds.append([top, num, bottom])
                except: pass
        bonds = [bond if i % 2 == 0 else None for i, bond in enumerate(sorted(bonds))]
        for i in bonds:
            if i == None: bonds.remove(i)
        return sorted(bonds)

    def bondOrder(self):
        bonds = self.getCovalentBonds()
        total = 0
        for i in bonds: total += i[1]
        num = len(bonds)
        return total / num

    def sigmaBonds(self):
        return len(self.getCovalentBonds())
    
    def piBonds(self):
        bonds = self.getCovalentBonds()
        total = 0
        for i in bonds: total += i[1] - 1
        return total

    def bondEnergy(self):
        if self.equation == "CO2": return 1157
        if len(self.compound) == 1 and self.numElements() == 1: return 0
        
        energy = 0
        bonds = self.getCovalentBonds()
        for i in bonds:
            try:
                try:
                    bond = i[0][0] + str(i[1]) + i[2][0]
                    energy += bondEnergies.get(bond)
                except:
                    bond = i[2][0] + str(i[1]) + i[0][0]
                    energy += bondEnergies.get(bond)
            except TypeError: raise Exception("bond not found: " + str(i))

        return energy

    def VESPR(self): # make sure that the compound for this is generated by randBMForBonds()
        if not self.isBinaryMolecular():
            raise Exception("Bad Cmpd")
        
        matrix = self.covalentBonds()
        center = matrix[2][2]

        lonePairs = center[1] // 2

        bonds = 0
        for i in range(1,4):
            for j in range(1,4):
                if matrix[i][j] not in [None, center]: bonds += 1

        if bonds == 1:
            if center == matrix[2][0]: return ["linear", "linear", "180", "np", f"sp{lonePairs if lonePairs != 0 else ''}"]
            else: return ["linear", "linear", 180, "p", f"sp{lonePairs if lonePairs != 0 else ''}"]


        effectivePairs = bonds + lonePairs

        try: 
            return bondTypeDict[effectivePairs * 10 + lonePairs]
        except: 
            raise Exception(f"bond type not found: effective pairs: {effectivePairs}, lone pairs: {lonePairs}")

    def numElements(self):
        s = 0
        for i in self.compound: s += i[1]
        return s

    def hasEl(self, el): 
        for i in self.compound:
            if i[0] == el: return True
        
        return False

    def isPolar(self):        
        if self.isHydroCarbon():
            return "O" in self.equation

        if self.isDiatomic():
            return False
        
        try: return self.VESPR()[3] == "polar"
        except: return False

    def getNumEl(self, el):
        for i in self.compound:
            if i[0] == el: return i[1]

        return 0

    def isIonic(self):
        metal = self.compound[0][0]
        return int(findElement(metal)[0]) in metalsDict

    def isWater(self):
        return self.equation == "H2O"

    def isAqOrGas(self): 
        return self.isMolecular() or self.isIonic() or self.isElement()

    def gen_K_sp(self):
        Ksp = KspDict.get(self.equation)
        if Ksp == None: return random.choice(list(KspDict.values()))

        return Ksp
    
    def solubility_rx(self, mConc = 0, nConc = 0):
        if self.K_sp == None: self.K_sp = self.gen_K_sp()
        try:
            m, nm = ionizeTernaryIonic(self.equation)
            m = m[0] + "_" + str(m[1])
            nm = nm[0] + "_-" + str(nm[1])
        except:
            if "(NH4)" in self.equation:
                m = ["NH4", 1]
                nm = [self.equation[6:], int(self.equation[5])]
            elif "NH4" in self.equation:
                m = ["NH4", 1]
                nm = [self.equation[3:], 1]
            elif len(self.compoundDict) == 2:
                nm = list(self.compoundDict.keys())[1]
                nmCharge = int(findElement(nm)[3][0])
                nmCharge = min(4, nmCharge) + int(nmCharge > 4) * (4 - nmCharge)
                nm += "_-" + str(nmCharge)

                mCharge = nmCharge * self.compound[1][1] / self.compound[0][1]
                m = self.compound[0][0] + "_" + str(int(mCharge))
            # raise Exception(f"only input ternary ionic compounds, {self} is not valid")
        
        return make_reaction(["s", [self], [make_compound(m), make_compound(nm)], [self.K_sp, mConc, nConc]])

    # cant handle peroxides
    def oxidation_numbers(self) -> dict[str, int]:
        if len(self.compound) == 1: return {self.compound[0][0] : self.charge}
        oxiList = dict.fromkeys(self.compoundDict.keys(), 0)

        try:
            metal, polyatomicIon = ionizeTernaryIonic(self.equation)
            oxiList[metal[0]] = metal[1]
            polyatomicIon[1] = str(-polyatomicIon[1])
            oxiPoly = compound("_".join(polyatomicIon)).oxidation_numbers()
            return oxiList | oxiPoly
        except: pass

        if oxiList.get("F") != None: 
            oxiList["F"] = -1 * self.compoundDict["F"]

            if oxiList.get("O") != None: oxiList["O"] = 2 * self.compoundDict["O"]
        elif oxiList.get("O") != None: oxiList["O"] = -2 * self.compoundDict["O"]

        elementsInCmpd = list(oxiList.keys())

        metal = findElement(elementsInCmpd[0])

        if metal[3] in ["1a", "2a"]: oxiList[metal[2]] = int(metal[3][0]) * self.compoundDict[metal[2]]

        if elementsInCmpd[0] == "H": oxiList["H"] = self.compoundDict["H"]
        elif oxiList.get("H") != None: oxiList["H"] = -self.compoundDict["H"]

        oxiSum = sum(list(oxiList.values()))
        try: zero_index = list(oxiList.values()).index(0)
        except: zero_index = 0

        oxiList[elementsInCmpd[zero_index]] += self.charge - oxiSum

        for el in oxiList: oxiList[el] = int(oxiList[el] / self.compoundDict[el])

        # deals with when oxiList is (0,0) (binary compounds) (might cause errors?)
        if len(oxiList) == 2 and list(oxiList.values()) == [0,0]:
            if self.isIonic():
                nmCharge = findCharge(self.compound[1][0])
                mCharge = self.compound[1][1] * (self.compound[0][1] / nmCharge)
                oxiList[self.compound[0][0]] = mCharge
                oxiList[self.compound[1][0]] = nmCharge
            else:
                c1 = findCharge(self.compound[0][0])
                c2 = findCharge(self.compound[1][0])
                c = gcd(c1, c2)
                oxiList[self.compound[0][0]] = c2 / c
                oxiList[self.compound[1][0]] = -c1 / c

        return oxiList

class hydrate(compound):
    def __init__(self, equation : str, numWater : int):
        super().__init__(equation)

        self.anhydrous = self.equation
        self.anhydrousCmpd = self.compound

        self.equation += f" 🞄 {numWater}H2O"
        self.type = "hydrate"
        self.numWater = numWater
        hGood, oGood = False, False
        for i in self.compound:
            if i[0] == "H":
                i[1] += 2 * numWater
                hGood = True
            if i[0] == "O": 
                i[1] += numWater
                oGood = True

        if not hGood: self.compound.append(["H", 2 * numWater])
        if not oGood: self.compound.append(["O", numWater])

    def getNameFromEq(self):
        return super().getNameFromEq(eqOveride=self.anhydrous,cmpdOverride=self.anhydrousCmpd) + " " + prefixes.get(self.numWater) + "hydrate"

    def isPolar(self): return True

    def percentWater(self):
        return self.numWater * 18 / self.getMolarMass()

set_compound_factory(lambda eq, charge=0: compound(eq, charge))
