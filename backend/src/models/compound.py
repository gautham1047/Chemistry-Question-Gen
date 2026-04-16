from src.utils.parsing import *
from src.utils.bonding import *
from src.utils.naming import name_from_atoms
from src.registry import set_compound_factory, make_compound, make_reaction
from math import gcd

class compound:
    def __init__(self, compoundList=None, charge=0):
        self.K_sp = None
        self.temp = 0

        if isinstance(compoundList, compound):
            self.name = compoundList.name
            self.equation = compoundList.equation
            self.charge = compoundList.charge
            self.compound = [list(a) for a in compoundList.compound]
            self._rebuild_dict()
            return

        if compoundList == "e-":
            self.name = "electron"
            self.equation = "e-"
            self.charge = -1
            self.compound = []
            self.compoundDict = {}
            return

        if isinstance(compoundList, str):
            _, parsed_charge = parse_formula(compoundList)
            # strip any charge suffix from the equation without touching the body
            eq = compoundList
            if "^" in eq:
                eq = eq.split("^", 1)[0]
            elif eq and eq != "e-" and eq[-1] in "+-":
                eq = eq[:-1]
            self.equation = eq
            self.name = None  # filled below after self.compound is populated
        else:
            raise TypeError(f"compound() got unexpected input: {type(compoundList).__name__}")

        self.charge = charge if charge else parsed_charge

        self.compound = atomsInCompound(self.equation)
        self._rebuild_dict()
        if self.name is None:
            self.name = name_from_atoms(self.compound, self.equation)

    def _rebuild_dict(self):
        self.compoundDict = {}
        for sym, count in self.compound:
            self.compoundDict[sym] = self.compoundDict.get(sym, 0) + count

    def __eq__(self, other):
        if not isinstance(other, compound):
            return NotImplemented
        return self.equation == other.equation and self.charge == other.charge

    def __hash__(self):
        return hash((self.equation, self.charge))

    def __repr__(self):
        if self.equation == "e-": return "e-"
        return self.equation + ("_" + str(self.charge)) * (self.charge != 0)

    def getEq(self):
        return compoundToString(self.compound)

    def getMolarMass(self):
        return sum(getAtomMass(sym) * count for sym, count in self.compound)
    
    def getMass(self, moles = 1):
        return moles * self.getMolarMass()

    def getAtoms(self, moles = 1):
        return moles * 6.02e+23 * self.totalAtoms()
    
    def percentComposition(self):
        MM = self.getMolarMass()
        return [[sym, getAtomMass(sym) * count * 100 / MM]
                for sym, count in self.compoundDict.items()]

    def getName(self):
        return self.name

    def multCompound(self, factor):
        self.compound = [[sym, count * factor] for sym, count in self.compound]
        self._rebuild_dict()
        self.equation = compoundToString(self.compound)
        self.name = name_from_atoms(self.compound, self.equation)

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
    
    def raiseTemp(self, finalTemp, moles, fp, bp, hF, hV, sSH, lSH, gSH):
        # Returns heat (kJ) required to bring the sample from self.temp to finalTemp.
        # Negative = released. Water example: (T, moles, 0, 100, 6.01, 40.7, 1.7, 4.18, 2.1)
        if finalTemp == self.temp:
            if finalTemp == fp: return hF * moles
            if finalTemp == bp: return hV * moles
            return 0

        mass = self.getMass(moles)

        def enthalpy(T):
            # Cumulative enthalpy (kJ) with fusion/vap steps baked in at fp/bp.
            if T < fp:
                return sSH * mass * T / 1000
            h = sSH * mass * fp / 1000 + hF * moles
            if T < bp:
                return h + lSH * mass * (T - fp) / 1000
            return h + lSH * mass * (bp - fp) / 1000 + hV * moles + gSH * mass * (T - bp) / 1000

        heat = enthalpy(finalTemp) - enthalpy(self.temp)
        self.temp = finalTemp
        return heat

    def heat(self, heatSupplied, moles, fp, bp, hF, hV, sSH, lSH, gSH):
        # Returns new temperature after absorbing heatSupplied joules.
        # Walks phase segments until budget exhausted.
        mass = self.getMass(moles)
        sh = {"s": sSH, "l": lSH, "g": gSH}

        if self.temp < fp: phase = "s"
        elif self.temp < bp: phase = "l"
        else: phase = "g"
        # legacy: promote past phases with zero specific heat (no data for that state)
        if phase == "s" and sSH == 0: phase = "l"
        if phase == "l" and lSH == 0: phase = "g"

        if heatSupplied >= 0:
            # heating: s →(hF@fp)→ l →(hV@bp)→ g
            transitions = [("s", fp, hF * moles * 1000, "l"),
                           ("l", bp, hV * moles * 1000, "g")]
            for cur, boundary, pc, nxt in transitions:
                if phase != cur: continue
                c = mass * sh[phase]
                span = c * (boundary - self.temp)
                if heatSupplied < span:
                    self.temp += heatSupplied / c
                    return self.temp
                heatSupplied -= span
                self.temp = boundary
                if heatSupplied <= pc:
                    return boundary
                heatSupplied -= pc
                phase = nxt
            self.temp += heatSupplied / (mass * sh[phase])
            return self.temp

        # cooling: g →(hV@bp)→ l →(hF@fp)→ s; track positive "to remove" budget
        remaining = -heatSupplied
        transitions = [("g", bp, hV * moles * 1000, "l"),
                       ("l", fp, hF * moles * 1000, "s")]
        for cur, boundary, pc, nxt in transitions:
            if phase != cur: continue
            c = mass * sh[phase]
            span = c * (self.temp - boundary)
            if remaining < span:
                self.temp -= remaining / c
                return self.temp
            remaining -= span
            self.temp = boundary
            if remaining < pc:
                return boundary
            remaining -= pc
            phase = nxt
        # solid tail — guard against missing solid SH data
        if sh[phase] == 0:
            self.temp = fp
            return fp
        self.temp -= remaining / (mass * sh[phase])
        return self.temp
    
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
        # polyatomic acid: leading H(n), remainder is a polyatomic ion
        if self.compoundDict.get("H", 0) == 0:
            return False
        body = compoundToString([[s, c] for s, c in self.compound if s != "H"])
        return body in polyatomicCharges

    def isBinaryMolecular(self):
        return len(self.uniqueEls()) == 2 and self.isMolecular()

    def isElement(self):
        return all([i.islower() and not i.isdigit() for i in self.equation[1:]])

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
        except Exception: raise Exception("No lewis dot structure found")

    def getCovalentBonds(self):
        try:
            matrix = self.covalentBonds()
        except Exception:
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
                except (NameError, UnboundLocalError): pass
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
        if len(self.compound) == 1 and self.totalAtoms() == 1: return 0
        
        energy = 0
        bonds = self.getCovalentBonds()
        for i in bonds:
            try:
                try:
                    bond = i[0][0] + str(i[1]) + i[2][0]
                    energy += bondEnergies.get(bond)
                except TypeError:
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
        except KeyError:
            raise Exception(f"bond type not found: effective pairs: {effectivePairs}, lone pairs: {lonePairs}")

    def totalAtoms(self):
        """Total atom count across all elements (H2O -> 3). Not to be confused
        with `len(self.compoundDict)` which gives the number of *distinct*
        elements."""
        return sum(count for _, count in self.compound)

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
        except Exception: return False

    def getNumEl(self, el):
        for i in self.compound:
            if i[0] == el: return i[1]

        return 0

    def isIonic(self):
        # ionic = contains at least one metal or transition metal, OR an NH4+ cation
        if "NH4" in self.equation:
            return True
        for sym in self.compoundDict:
            try:
                el = findElement(sym)
            except Exception:
                continue
            if el[4] in ("m", "tm"):
                return True
        return False

    def isWater(self):
        return self.equation == "H2O"

    def solubility_rx(self, mConc=0, nConc=0):
        if self.K_sp is None:
            self.K_sp = KspDict.get(self.equation) or random.choice(list(KspDict.values()))

        cation, anion = self._dissociate()
        return make_reaction(["s", [self],
                              [make_compound(*cation), make_compound(*anion)],
                              [self.K_sp, mConc, nConc]])

    def _dissociate(self):
        """Return ((cation_formula, cation_charge), (anion_formula, anion_charge))."""
        try:
            m, nm = ionizeTernaryIonic(self.equation)
            return (m[0], m[1]), (nm[0], -nm[1])
        except Exception:
            pass

        if "(NH4)" in self.equation:
            return ("NH4", 1), (self.equation[6:], -int(self.equation[5]))
        if "NH4" in self.equation:
            return ("NH4", 1), (self.equation[3:], -1)
        if len(self.compoundDict) == 2:
            m_sym, m_count = self.compound[0]
            n_sym, n_count = self.compound[1]
            nm_charge = int(findElement(n_sym)[3][0])
            if nm_charge > 4:
                nm_charge = 8 - nm_charge
            m_charge = int(nm_charge * n_count / m_count)
            return (m_sym, m_charge), (n_sym, -nm_charge)

        raise ValueError(f"cannot dissociate {self.equation}")

    # cant handle peroxides
    def oxidation_numbers(self) -> dict[str, int]:
        if len(self.compound) == 1: return {self.compound[0][0] : self.charge}
        oxiList = dict.fromkeys(self.compoundDict.keys(), 0)

        try:
            metal, polyatomicIon = ionizeTernaryIonic(self.equation)
            oxiList[metal[0]] = metal[1]
            oxiPoly = compound(polyatomicIon[0], charge=-polyatomicIon[1]).oxidation_numbers()
            return oxiList | oxiPoly
        except Exception:
            pass

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
        except ValueError: zero_index = 0

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
        self.name = self.name + " " + prefixes.get(numWater) + "hydrate"
        self.equation += f" 🞄 {numWater}H2O"
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
        self._rebuild_dict()

    def isPolar(self): return True

    def percentWater(self):
        return self.numWater * 18 / self.getMolarMass()

set_compound_factory(lambda eq, charge=0: compound(eq, charge))
