import random, math, sympy as sp, numpy as np
from chemData import *
from src.models.compound import compound
from src.utils.parsing import ionicCompoundFromElements
from src.models.element import element
from src.utils.math_helpers import round_sig
from src.registry import set_reaction_factory

class reaction:
    def __init__(self, inputList, eqChoice = "NONE", waterAsGas = False):
        self.phases = None
        self.K_eq = None
        self.reactantList = None
        self.typeRx = None
        self.misc = None
        self.occurs = True
        # Lazy-computed and memoized by _computeSkeleton / balanceEq.
        self._skele_cache = None
        self._coeffs_cache = None

        if inputList == "eq":
            solid_index = []
            n = random.randint(2,5)
            options = [
                [["NOCl"], ["NO", "Cl2"]],
                [["H2", "CO2"], ["H2O", "CO"]],
                [["N2", "O2"], ["NO"]],
                [["N2", "O2"], ["NO2"]],
                [["C", "O2"], ["CO"]],
                [["C", "O2"], ["CO2"]],
                [["H2", f"C{n}H{2*n-2}"], [f"C{n}H{2*n}"]],
                [["H2", f"C{n}H{2*n-2}"], [f"C{n}H{2*n+2}"]],
                [["H2", f"C{n}H{2*n}"], [f"C{n}H{2*n+2}"]]
            ]
            i = eqChoice if eqChoice != "NONE" and eqChoice in range(0,12) else random.randint(0,11)
            if i < 9: 
                rx = options[i]
                if rx[0][0] == "C": solid_index = [0]
            elif i == 9:
                hOne, hTwo = random.sample(["H", "Cl", "Br", "I", "F"], 2)
                rx = [[hOne + "2", hTwo + "2"], [hOne + hTwo]]
            else:
                ones = [3,11,19,37,55]
                one = bool(random.getrandbits(1))
                if one: 
                    m = elements[random.choice(ones)][2]
                    rx = [[f"{m}2O", "H2"], [m, "H2O"]]
                else: 
                    m = elements[random.choice([i + 1 for i in ones])][2]
                    rx = [[f"{m}O", "H2"], [m, "H2O"]]

                solid_index = [0,2]

            # switch the order half the time
            switchOrder = random.getrandbits(1)
            if switchOrder: 
                rx[0], rx[1] = rx[1], rx[0]
                if solid_index == [0]: solid_index = [1]

            self.reactantList, self.misc = [[compound(i) for i in react] for react in rx]
            if waterAsGas: self.phases = ["g" for _ in rx[0] + rx[1]]
            else: self.phases = ["g" if not i == "H2O" else random.choice(["l", "g"]) for i in rx[0] + rx[1]]
            for s in solid_index:
                self.phases[s] = "s"
            self.typeRx = "eq"
            power_of_K = random.randint(5,12) * (-1) ** random.randint(0,1)
            K_eq = random.random() * 10 ** power_of_K
            self.generateEqConcs(K_eq)

            self.typeRx = "eq"
        elif inputList[0] in ["a", "b", "ab"]:
            self.typeRx = inputList[0]
            self.reactantList = inputList[1]
            self.misc = inputList[2]

            self.phases = ["l" if i.equation == "H2O" else "aq" for i in self.reactantList + self.misc]

            self.K_eq = inputList[3][1]
            self.reactEqConcs = [inputList[3][0]]
            self.prodEqConcs = [0,0]
            self.eqConcsFromIntial([0, 0], [inputList[3][0]])
        elif inputList[0] == "n":
            self.typeRx = inputList[0]
            self.reactantList = inputList[1]
            self.misc = inputList[2]
        elif inputList[0] == "s":
            self.typeRx = inputList[0]
            self.reactantList = inputList[1]
            self.misc = inputList[2]
            self.phases = ["s", "aq", "aq"]
            self.K_eq = inputList[3][0]
            self.reactEqConcs = []
            self.prodEqConcs = [inputList[3][1], inputList[3][2]]
            self.eqConcsFromIntial()
        else:       
            self.reactantList = inputList[0]
            # never change the order of reactantList
            self.typeRx = inputList[1]
            self.misc = inputList

    def __str__(self):
        coefficients = self.balanceEq()
        skeleton = self.SkeletonEquation()
        rxStr = ""
        for i, cmpd in enumerate(skeleton[0]):
            if coefficients[i] == 1: coefficient = ""
            else: coefficient = coefficients[i]
            rxStr += str(coefficient) + str(cmpd) + " + "
        rxStr = rxStr[:-3]
        if self.typeRx == "d": rxStr += "--Δ-->"
        else: rxStr += " -----> "
        if self.occurs or self.typeRx == "dr":
            for i, cmpd in enumerate(skeleton[1]):
                try:
                    if coefficients[i+len(skeleton[0])] == 1: coefficient = ""
                    else: 
                        coefficient = coefficients[i + len(skeleton[0])]
                except IndexError: pass 
                rxStr += str(coefficient) + str(cmpd) + " + "
            rxStr = rxStr[0:-3]
            if self.typeRx == "dr" and not self.occurs: rxStr += "\nDR/NR"
        else: rxStr += "SR/NR"
        
        return rxStr

    def phaseStr(self):
        if self.phases == None: return str(self)
        reactants, products = self.formatRxList()
        index = -1 # := increments on the first iteration
        rx_str = ""
        
        for reactant in reactants: rx_str += f"{reactant[1] if reactant[1] != 1 else ''}{reactant[0].__repr__()}({self.phases[(index := index + 1)]}) + "
        rx_str = rx_str[:-3] + "-->"
        for product in products: rx_str += f"{product[1] if product[1] != 1 else ''}{product[0].__repr__()}({self.phases[(index := index + 1)]}) + "
        return rx_str[:-3]

    def SkeletonEquation(self) -> list[list[compound]]:
        # Returns [[reactant compounds], [product compounds]]. Memoized.
        # Problem files should prefer reactants() / products() which return
        # [[cmpd, coeff], ...] pairs. SkeletonEquation is kept for internal use.
        if self._skele_cache is not None:
            return self._skele_cache
        self._skele_cache = self._computeSkeleton()
        return self._skele_cache

    def _computeSkeleton(self) -> list[list[compound]]:
        match self.typeRx:
            case "s1":
                m = self.reactantList[0]
                n = self.reactantList[1]
                mNum = n[1]
                nNum = m[1]
                gcd = math.gcd(mNum, nNum)
                mNum = int(mNum/gcd)
                nNum = int(nNum/gcd)
                if mNum == 1: mNum = ""
                if nNum == 1: nNum = ""
                nonmetal = ""
                if n[0][-1] == "2":
                    for i in n[0]:
                        if not i.isdigit():
                            nonmetal += i
                else: nonmetal = n[0]
                return [[compound(m[0]), compound(n[0])],[compound(f"{m[0]}{mNum}{nonmetal}{nNum}")]]
            case "s2":
                answerDict = {
                    "SO2" : "H2SO3",
                    "SO3" : "H2SO4",
                    "CO2" : "H2CO3",
                    "N2O3" : "HNO2",
                    "N2O5" : "HNO3",
                    "P2O3" : "H3PO3",
                    "P2O5" : "H3PO4",
                    "As2O3" : "H3AsO3",
                    "As2O5" : "H3AsO4",
                    "NH3" : "NH4OH"
                }
                cmpd = self.reactantList[0][0]
                product = answerDict.get(cmpd)
                return [[compound(cmpd), compound("H2O")],[compound(product)]]
            case "s3":
                mOxide = self.reactantList[0][0]
                lastDigit = mOxide[-1]
                if lastDigit == "O":
                    if "2" in mOxide:
                        mCharge = 1
                    else: mCharge = 2
                else: 
                    if lastDigit == "3":
                        mCharge = 3
                    else: mCharge = 4
                if mOxide[1].islower():
                    metal = mOxide[0:2]
                else: metal = mOxide[0]
                product = f"{metal}"
                if mCharge == 1:
                    product += "OH"
                else: product += "(OH)" + str(mCharge)
                mOxide = compound(mOxide)
                product= compound(product)
                return [[mOxide, compound("H2O")], [product]]
            case "d1":
                cmpd = compound(self.reactantList[0])
                el1 = cmpd.compound[0][0]
                try: el2 = cmpd.compound[1][0]
                except IndexError: raise Exception("Invalid compound: " + cmpd)
                diatomicAtoms = ["H", "N", "O", "F", "Cl", "Br", "I"]
                if el1 in diatomicAtoms: el1 += "2"
                if el2 in diatomicAtoms: el2 += "2"
                return [[cmpd], [compound(el1), compound(el2)]]
            case "d2":
                cmpd = self.reactantList[0]
                if "(ClO3)" in cmpd:
                    index = cmpd.index("(")
                    ClO3Num = cmpd[-1]
                else: 
                    index = cmpd.index("ClO3")
                    ClO3Num = ""
                el1 = compound(cmpd[:index] + "Cl" + ClO3Num)
                el2 = compound("O2")
                return [[compound(cmpd)], [el1, el2]]
            case "d3":
                cmpd = self.reactantList[0]
                if "(CO3)" in cmpd:
                    index = cmpd.index("(")
                    CO3Num = cmpd[-1]
                else: 
                    index = cmpd.index("CO3")
                    CO3Num = ""
                el1 = compound(cmpd[:index] + "O" + CO3Num)
                el2 = compound("CO2")
                return [[compound(cmpd)], [el1, el2]]
            case "c1":
                m = self.reactantList[0]
                n = self.reactantList[1]
                mNum = n[1]
                nNum = m[1]
                gcd = math.gcd(mNum, nNum)
                mNum = int(mNum/gcd)
                nNum = int(nNum/gcd)
                if mNum == 1: mNum = ""
                if nNum == 1: nNum = ""
                nonmetal = ""
                if n[0][-1] == "2":
                    for i in n[0]:
                        if not i.isdigit():
                            nonmetal += i
                else: nonmetal = n[0]
                return [[compound(m[0]), compound(n[0])],[compound(f"{m[0]}{mNum}{nonmetal}{nNum}")]]
            case "complete combustion":
                reactant = compound(self.reactantList[0])
                return [[reactant, compound("O2")], [compound("CO2"), compound("H2O")]]
            case "incomplete combustion":
                reactant = compound(self.reactantList[0])
                return [[reactant, compound("O2")], [compound("CO"), compound("H2O")]]
            case "sr1":
                mActivitySeries = ["Ag", "Hg", "Cu", "H", "Pb", "Fe", "Zn", "Al", "Mg", "Na", "Ca", "K", "Li"]
                metal1= self.reactantList[1]
                m1 = metal1[0]
                nonmetal = self.misc[3]
                nonmetal[0] = nonmetal[0].replace("(","")
                nonmetal[0] = nonmetal[0].replace(")", "")
                metal2 = self.misc[2]
                m2 = metal2[0]
                product = ionicCompoundFromElements(m = metal1, n = nonmetal)
                metal1.append("element")
                metal2.append("element")
                cmpd = self.reactantList[0][0]
                if m1 == "Hg2": m1Index = 1
                else: m1Index = mActivitySeries.index(m1)
                if m2 == "Hg2": m2Index = 1
                else: m2Index = mActivitySeries.index(m2)
                if m1Index < m2Index:
                    self.occurs = False
                return [[compound(cmpd), compound(metal1)],[compound(product), compound(metal2)]]
            case "sr2":
                nActivitySeries = ["I", "Br", "Cl", "F"]
                nmetal1 = self.reactantList[1]
                metal = self.misc[2]
                nmetal2 = self.misc[3]
                nmetal2.append("element")
                nmetal1[1] = 1
                nmetal2[1] = 2
                product = ionicCompoundFromElements(m = metal, n = nmetal1)
                nmetal1.append("element")
                cmpd = self.reactantList[0][0]
                nmetal1[1] = str(nmetal1[1])
                nmetal2[1] = str(nmetal2[1])
                nmetal1[1] += "2"
                nmetal2[1] += "2"
                if nActivitySeries.index(nmetal2[0]) > nActivitySeries.index(nmetal1[0]):
                    self.occurs = False
                return [[compound(cmpd), compound(nmetal1[0] + '2')], [compound(product), compound(nmetal2[0] + "2")]]
            case "dr": # this has a ton of errors apparently
                returnList = self.misc[2]
                for index, product in enumerate(returnList[1]):
                    if product.equation == "NH4OH":
                        returnList[1].pop(index)
                        returnList[1].append(compound("NH3"))
                        returnList[1].append(compound("H2O"))
                    elif product.equation == "H2CO3":
                        returnList[1].pop(index)
                        returnList[1].append(compound("H2O"))
                        returnList[1].append(compound("CO2"))
                self.occurs = False
                try:
                    for product in returnList[1]:
                        if not product.isSoluable():
                            self.occurs = True
                except:
                    print(returnList)
                    print(self.reactantList)
                    raise Exception("error generating skeleton equation")

                return returnList
            case "special":
                if self.misc[2] in ["dilute", "concentrated"]:
                    reactants = [i[0] for i in self.reactantList]
                    products = [i[0] for i in self.misc[3]]
                if self.misc[2] == "hydrocarbon replacement":
                    reactants = [i[0] for i in self.reactantList]
                    cmpd = reactants[0].compound
                
                    if cmpd[0][1] * 2 + 2== cmpd[1][1]:
                        newCmpd = f"C{cmpd[0][1] if cmpd[0][1] != 1 else ''}H{cmpd[1][1]-2}{reactants[1].equation}"
                        products = [compound(newCmpd), compound("H2")]
                    else: products = [compound(reactants[0].equation + reactants[1].equation)]
                
                return [reactants, products]
            case "eq" | "ab" | "a" | "b" | "n" | "s":
                return [self.reactantList, self.misc]
            case _: print(self.typeRx)

    def balanceEq(self):
        if self._coeffs_cache is not None:
            return self._coeffs_cache
        self._coeffs_cache = self._computeBalance()
        return self._coeffs_cache

    def _computeBalance(self):
        rpList = self.SkeletonEquation()
        try: rList = rpList[0]
        except:
            print([str(i) for i in self.misc])
            raise Exception("bad skeleton equation: " + str(rpList))
        pList = rpList[1]
        relList = []
        # for single elements, the format is [El, 1]
        for reactant in rList:
            for i in reactant.compound:
                if type(i) == str:
                    if i not in relList: relList.append(i)
                else:
                    try:
                        if i[0] not in relList:
                            relList.append(i[0])
                    except TypeError: pass
        inputMatrix = [] # [[el1 in react1, el1 in react2..., -el1 in product1, -el1 in product2, 0], [el2 in react1, el2 in react2..., -el1 in product1, -el1 in product2, 0],...]
        for el in relList:
            toAppend = []
            for reactant in rList:
                elcount = 0
                for i in reactant.compound:
                    if type(i) == str:
                        if i == el:
                            elcount += reactant.compound[1]
                        break
                    elif i[0] == el:
                            elcount += i[1]
                toAppend.append(elcount)
            for product in pList:
                elcount = 0
                for i in product.compound:
                    if type(i) == str:
                        if i == el:
                            elcount += product.compound[1]
                        break
                    elif i[0] == el:
                            elcount += i[1]
                toAppend.append(elcount)
            toAppend.append(0)
            inputMatrix.append(toAppend)
        
        inputArray = sp.Matrix(inputMatrix)
        rrefMatrix = list(inputArray.rref()[0])
        rrefList = []
        numcmpd = len(rList) + len(pList)
        i = numcmpd - 1
        while i in range(1,len(rrefMatrix)-1):
            rrefList.append(abs(float(rrefMatrix[i])))
            i += numcmpd + 1
        if rrefList[-1] == 0:
            rrefList = rrefList[0:-1]
        
        # print(f"rrefList: {rrefList}")
        for i, num in enumerate(rrefList):
            if num == 0: rrefList.pop(i)

        rrefList.extend([1.0])
        good = True

        for i in rrefList:
            if type(i) != int and not i.is_integer():
                good = False
        factor = 1
        if good: numList = rrefList
        while not good:
            numList = []
            for i in rrefList:
                i *= factor
                numList.append(i)
            factor += 1
            good = True
            for i in numList:
                if not i.is_integer():
                    good = False  

        numList = [int(i) for i in numList if int(i) != 0]

        l = len([i for sublist in rpList for i in sublist])
        while len(numList) < l:
            numList.append(1)

        return numList
    
    def reactants(self) -> list[list]:
        """Return reactants as [[compound, coefficient], ...]. Canonical public API."""
        r_cmpds, _ = self.SkeletonEquation()
        coeffs = self.balanceEq()
        return [[cmpd, coeffs[i]] for i, cmpd in enumerate(r_cmpds)]

    def products(self) -> list[list]:
        """Return products as [[compound, coefficient], ...]. Canonical public API."""
        r_cmpds, p_cmpds = self.SkeletonEquation()
        coeffs = self.balanceEq()
        offset = len(r_cmpds)
        return [[cmpd, coeffs[offset + i]] for i, cmpd in enumerate(p_cmpds) if offset + i < len(coeffs)]

    def allCompounds(self) -> list[compound]:
        reactants, products = self.SkeletonEquation()
        return reactants + products

    def formatRxList(self) -> list:
        # Legacy shim. New code should use reactants() / products() directly.
        # For "special" type, tacks on self.misc[2] as a third element (dilute/concentrated/etc).
        result = [self.reactants(), self.products()]
        if self.typeRx == "special":
            result.append(self.misc[2])
        return result

    def enthalpyFromBonds(self):
        try:
            react = sum(coeff * cmpd.bondEnergy() for cmpd, coeff in self.reactants())
            prod = sum(coeff * cmpd.bondEnergy() for cmpd, coeff in self.products())
        except Exception:
            return f"error finding the enthalpy of {self}"
        return react - prod

    def generatePhases(self):
        reactants, products = self.SkeletonEquation()
        if len(reactants) > 2 and reactants[0].isHydroCarbon() and reactants[1].equation == "O2":
            phases = ["g", "g"]
            for cmpd in products:
                if cmpd.isWater(): phases.append(random.choice(["g", "l", "l"]))
                else: phases.append("g")
            self.phases = phases
            return phases
        
        phases = []
        if self.typeRx == "dr":
            for cmpd in reactants + products:
                if cmpd.isSoluable(): phases.append("aq")
                elif cmpd.isWater(): phases.append("l")
                elif cmpd.isMolecular(): phases.append("g")
                else: phases.append("s")
            self.phases = phases
            return phases

        if self.typeRx == "sr":
            for cmpd in reactants + products:
                if cmpd.isElement(): phases.append(element(cmpd.equation).getPhase())
                elif cmpd.isSoluable(): phases.append("aq")
                else: phases.append("s")
            self.phases = phases
            return phases
        
        phase_of_other = random.choice(["s", "aq"])
        for cmpd in reactants + products:
            if cmpd.isDiatomic(): phases.append("g")
            elif cmpd.isElement(): phases.append(element(cmpd.equation).getPhase())
            elif cmpd.isMolecular(): phases.append(random.choice(["l", "g"]))
            elif cmpd.equation == "Cu(NO3)2": phases.append("aq")
            else: phases.append(phase_of_other)
        self.phases = phases
        return phases

    def molecularity(self):
        return len(self.SkeletonEquation()[0])

    def checkRxForThermo(self):
        if not self.occurs: return False
        if self.phases == None: self.generatePhases()
        for phase, cmpd in zip(self.phases, self.allCompounds()):
            if thermoData.get(thermCompound(cmpd.equation + "(" + phase + ")")) == None: return False
        return True
    
    def thermoProfile(self, choice):
        # choice: 0 = enthalpy, 1 = gibbs, 2 = entropy
        if not self.checkRxForThermo(): return None
        i = 0
        n = len(self.reactants())
        curr = 0
        coeffs = self.balanceEq()
        for phase, cmpd in zip(self.phases, self.allCompounds()):
            amount = thermoData.get(thermCompound(cmpd.equation + "(" + phase + ")"))[choice]
            if i < n: curr -= coeffs[i] * amount
            else: curr += coeffs[i] * amount
            i += 1
        return curr

    def generateEqConcs(self, K_eq = None):
        prod_eq, react_eq = self.eqExpression()
        if K_eq == None:
            self.prodEqConcs = [random.randint(1,50000) / 10000 for _ in prod_eq]
            self.reactEqConcs = [random.randint(1,50000) / 10000 for _ in react_eq]
            self.K_eq = 1
            for expression, conc in zip(prod_eq, self.prodEqConcs): self.K_eq *= conc ** expression[1]
            for expression, conc in zip(react_eq, self.reactEqConcs): self.K_eq /= conc ** expression[1]
            self.K_eq = round_sig(self.K_eq, 6)
        else:
            self.K_eq = K_eq
            n = len(prod_eq)
            self.prodEqConcs = [K_eq ** (1/n) for _ in prod_eq]
            self.reactEqConcs = [1 for _ in react_eq]
            if any([i > 100 for i in self.prodEqConcs + self.reactEqConcs]):
                n = len(react_eq)
                self.reactEqConcs = [K_eq ** (-1/n) for _ in react_eq]
                self.prodEqConcs = [1 for _ in prod_eq]

    def eqExpressionStr(self):
        if self.phases == None: raise Exception("Must define phases!")
        reactants, products = self.formatRxList()
        index = -1
        reacts = [f"[{cmpd.equation}]" + (f"^{coeff}" if coeff != 1 else "") for cmpd, coeff in reactants if self.phases[index := index + 1] in ["g","aq"]]
        prods = [f"[{cmpd.equation}]" + (f"^{coeff}" if coeff != 1 else "") for cmpd, coeff in products if self.phases[index := index + 1] in ["g","aq"]]
        if prods == []: prods = ["1"]
        if reacts == []: return "".join(prods)
        return "".join(prods) + "/" + "".join(reacts)
    
    def eqExpression(self):
        if self.phases == None: raise Exception("Must define phases!")
        reactants, products = self.formatRxList()
        index = -1
        reacts = [[cmpd, coeff] for cmpd, coeff in reactants if self.phases[index := index + 1] in ["g","aq"]]
        prods = [[cmpd, coeff] for cmpd, coeff in products if self.phases[index := index + 1] in ["g","aq"]]
        return [prods, reacts]

    def reactionQuotient(self, prodConc = None, reactConc = None):
        if prodConc == None: prodConc = self.prodEqConcs
        if reactConc == None: reactConc = self.reactEqConcs

        prodEq, reactEq = self.eqExpression()

        prodConc = [i + 1e-200 for i in prodConc]
        reactConc = [i + 1e-200 for i in reactConc]

        Q = 1
        for conc, coeff in zip(prodConc, prodEq): Q *= conc ** coeff[1]
        try:
            for conc, coeff in zip(reactConc, reactEq): Q /= conc ** coeff[1]
        except:

            return float('inf')

        return Q

    def eqConcsFromIntial(self, newProd : list[int] = None, newReact : list[int] = None):
        if  not newProd: 
            newProd = self.prodEqConcs
        if not newReact: 
            newReact = self.reactEqConcs
        if len(newProd) != len(self.prodEqConcs) or len(newReact) != len(self.reactEqConcs): raise Exception("Invalid equilbrium inputs")
        prodEq, reactEq = self.eqExpression()
                
        rQuotient = self.reactionQuotient(newProd, newReact)
        pError = abs((rQuotient - self.K_eq) / self.K_eq)

        if pError < .05:
            self.prodEqConcs = newProd
            self.reactEqConcs = newReact

            return None

        towardsProducts = 2 * int(self.K_eq > rQuotient) - 1
        # 1 if it is towards the products, -1 if it is towards the reactants

        prodRoots = [[-1 * towardsProducts * initConc / stoicRatio[1]] * stoicRatio[1] for initConc, stoicRatio in zip(newProd, prodEq)]
        reactRoots = [[towardsProducts * initConc / stoicRatio[1]] * stoicRatio[1] for initConc, stoicRatio in zip(newReact, reactEq)]
        prodRoots = sum(prodRoots, []) # flattens list
        reactRoots = sum(reactRoots, []) # flattens list

        if prodRoots == []: prodPoly = np.polynomial.Polynomial([1])
        else: prodPoly = np.polynomial.polynomial.Polynomial.fromroots(prodRoots)
        if reactRoots == []: reactPoly = np.polynomial.Polynomial([1])
        else: reactPoly = np.polynomial.polynomial.Polynomial.fromroots(reactRoots)

        for stoicRatio in prodEq: prodPoly *= (towardsProducts * stoicRatio[1]) ** stoicRatio[1]
        for stoicRatio in reactEq: reactPoly *= (-towardsProducts * stoicRatio[1]) ** stoicRatio[1]

        eqPoly = prodPoly - reactPoly * self.K_eq

        roots = list(filter(lambda x : np.imag(x) < 1e-3 and x >= 0, eqPoly.roots()))

        d = min(np.real(roots))
        self.prodEqConcs = [initConc + towardsProducts * stoicRatio[1] * d for initConc, stoicRatio in zip(newProd, prodEq)]
        self.reactEqConcs = [initConc - towardsProducts * stoicRatio[1] * d for initConc, stoicRatio in zip(newReact, reactEq)]

def ionize_ab(cmpd : compound):
    # returns non H+ or OH- ion in a compound, given that it is an acid or base
    eq = cmpd.equation

    if eq[0] == "H":
        charge = eq[1]
        if eq[1].isdigit(): charge = int(charge)
        else: charge = 1

        return [eq[1 + eq[1].isdigit():], charge]
    
    if eq[-2:] == "OH": return [eq[:-2], 1]
    if eq[-5:-1] == "(OH)": return [eq[:-5], int(eq[-1])]

    raise Exception(f"invalid acid or base: {cmpd}")

class half_reaction(reaction):
    def __init__(self, init_cmpd : compound, final_cmpd : compound):
        rList = [init_cmpd]
        pList = [final_cmpd]

        rElements = [el for el in init_cmpd.compound if el[0] not in ["O", "H"]]
        pElements = [el for el in final_cmpd.compound if el[0] not in ["O", "H"]]
        if rElements != None and pElements != None:
            el1, num1 = rElements[0]
            num2 = final_cmpd.getNumEl(el1)
            rElements = [[el, num * num2] for el, num in rElements]
            pElements = [[el, num * num1] for el, num in pElements]

        if rElements != pElements:
            print(rElements)
            print(pElements)
            raise Exception("invalid half reaction")

        rCoeffs = [num2]
        pCoeffs = [num1]

        r_counts = {"O" : num2 * init_cmpd.getNumEl("O"), "H" : num2 * init_cmpd.getNumEl("H"), "e-": num2 * init_cmpd.charge}
        p_counts = {"O" : num1 * final_cmpd.getNumEl("O"), "H" : num1 * final_cmpd.getNumEl("H"), "e-": num1 * final_cmpd.charge}

        added = [] # will be # H2O, # H+, # e- (- means reactants, + means products)

        oDelta = r_counts["O"] - p_counts["O"]
        if oDelta < 0: 
            oDelta = -oDelta
            rList.append(compound("H2O"))
            rCoeffs.append(oDelta)
            r_counts["O"] += oDelta
            r_counts["H"] += 2 * oDelta
        elif oDelta > 0:
            pList.append(compound("H2O"))
            pCoeffs.append(oDelta)
            p_counts["O"] += oDelta
            p_counts["H"] += 2 * oDelta

        hDelta = r_counts["H"] - p_counts["H"]
        added.append(hDelta)
        if hDelta < 0:
            hDelta = -hDelta 
            rList.append(compound("H", 1))
            rCoeffs.append(hDelta)
            r_counts["H"] += hDelta
            r_counts["e-"] += hDelta
        elif hDelta > 0:
            pList.append(compound("H", 1))
            pCoeffs.append(hDelta)
            p_counts["H"] += hDelta
            p_counts["e-"] += hDelta

        eDelta = p_counts["e-"] - r_counts['e-']
        added.append(eDelta)
        if eDelta > 0:
            pList.append(compound("e-"))
            pCoeffs.append(eDelta)
            p_counts["e-"] -= eDelta
        elif eDelta < 0:
            eDelta = -eDelta
            rList.append(compound("e-"))
            rCoeffs.append(eDelta)
            r_counts["e-"] -= eDelta

        self.skele_eq = [rList, pList]
        self.coeffs = rCoeffs + pCoeffs

        self.phases = None
        self.K_eq = None
        self.reactantList = None
        self.typeRx = "redox"
        self.misc = None
        self.occurs = True
        # electrons on the right means oxidized, electrons on the left mean reduced
    
    # just have to redo balance_eq and skeleton str
    def balanceEq(self):
        return self.coeffs
    
    def SkeletonEquation(self) -> list[list[compound]]:
        return self.skele_eq

# finish this code
class redox_reaction(reaction):
    def __init__(self, red : half_reaction, ox : half_reaction):
        pass

set_reaction_factory(lambda *args, **kwargs: reaction(*args, **kwargs))

