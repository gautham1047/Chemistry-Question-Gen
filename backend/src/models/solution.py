from chemData import *
import random
from math import gcd, log10
from src.models.compound import compound
from src.models.reaction import reaction, ionize_ab
from src.utils.parsing import ionicCompoundFromElements, ionizeTernaryIonic
from src.utils.math_helpers import round_sig

class solution:
    def __init__(self, solute : compound, mass_solute : float = None, solute_density : float = 0, moles_solute : float = None, moles_solvent : float = None, total_volume : float = None, solvent : compound = compound("H2O")) -> None:
        # solute density in g/mL, mass solute in g, moles solute and moles solvent in mol, total volume in L
        # if solute density is 0, then we ignore the solute's mass for stuff
        # if solute density is None, then the code tries to find the density (if it can't, it randomly generates it in [.5,3.5])

        self.solute = solute
        self.solvent = solvent

        self.volume = None
        self.moles_solute = None
        self.moles_solvent = None

        if moles_solute and mass_solute: raise Exception("solute mass is overconstrained")
        if mass_solute: self.moles_solute = mass_solute / self.solute.getMass()
        if moles_solute: self.moles_solute = moles_solute
    
        if moles_solvent: self.moles_solvent = moles_solvent

        self.solvent_density = miscDensities.get(self.solvent.getEq())
        if not self.solvent_density: raise Exception(f"invalid solvent: {solvent.equation}")
        self.solute_density = solute_density  
        if self.solute_density == None: self.solute_density = miscDensities.get(self.solute.getEq())
        if self.solute_density == None: self.solute_density = round(random.random() * 3 + .5, 2)
        
        if total_volume:
            self.volume = total_volume
            if self.moles_solute and self.moles_solvent: raise Exception("volume is overconstrained")
            if not self.moles_solute: 
                if self.solvent_density != 0: total_volume -= self.solvent.getMass(self.moles_solvent) / (1000 * self.solvent_density)
                self.moles_solute = 1000 * total_volume * self.solute_density / self.solute.getMolarMass()
            if not self.moles_solvent:
                if self.solute_density != 0: total_volume -= self.solute.getMass(self.moles_solute) / (1000 * self.solute_density)
                self.moles_solvent = 1000 * total_volume * self.solvent_density / self.solvent.getMolarMass()
        
        if not self.moles_solute: self.moles_solute = 0
        if not self.moles_solvent: self.moles_solvent = 1
        if not self.volume: 
            if self.solute_density == 0: self.volume = self.solvent.getMass(self.moles_solvent) / (1000 * self.solvent_density)
            else:
                solute_volume = self.solute.getMass(self.moles_solute) / (1000 * self.solute_density)
                solvent_volume = self.solvent.getMass(self.moles_solvent) / (1000 * self.solvent_density)
                self.volume = solute_volume + solvent_volume

        if not self.moles_solute and self.solute_density == 0: self.moles_solute = 1

    def __str__(self):
        return f"{self.molarity()} M solution of {self.solute.equation} in {self.solvent.equation}"
    
    def moleFractions(self, solute = True):
        if solute: return self.moles_solute / (self.moles_solute + self.moles_solvent)
        else: return self.moles_solvent / (self.moles_solute + self.moles_solvent)
    
    def molality(self):
        return 1000 * self.moles_solute / self.solvent.getMass(self.moles_solvent)

    def molarity(self):
        return self.moles_solute / self.volume
    
    def pMV(self):
        # divide by 1000 (L --> mL) and multiply by a 100 (percent)
        return self.solute.getMass(self.moles_solute) / (10 * self.volume)
    
    def solute_volume(self):
        if self.solute_density == 0: return 0
        return self.solute.getMass(self.moles_solute) / (1000 * self.solute_density)
    
    def solvent_volume(self):
        return self.solvent.getMass(self.moles_solvent) / (1000 * self.solvent_density)

    # solute_density needs to be None or specified for this to work
    def pVV(self):
        return 100 * self.solute_volume() / self.solvent_volume()

    def setMolarity(self, newMolarity, addSolvent = False, addSolute = False):
        if addSolute and addSolvent: raise Exception("Only choose addSolute or addSolvent")
        if addSolute:
            M = self.molarity()
            self.moles_solute *= newMolarity / M
            self.volume *= M / newMolarity
        if addSolvent:
            M - self.molarity()
            self.moles_solvent *= M / newMolarity
            self.volume *= newMolarity / M

    def dissovles(self):
        return self.solute.isPolar() == self.solvent.isPolar()
    
    def aqueous(self):
        return self.solvent == compound("H2O")

    def describeSolute(self):
        if self.checkSolution != None: return self.checkSolution()

        if (self.solute.isSoluable() and self.solute.isIonic()) or self.solute.equation in ["HI", "HCl", "HBr"]: return "Strong Electrolyte"
        if not self.solute.isPolar(): return "Nonelectrolyte"
        return "Weak Electrolyte"

    def saturation(self):
        if self.checkSolution != None: return self.checkSolution()

        solubility = solubilities.get(self.solute.equation)
        if solubility == None: return "Unknown"

        gSolute = self.solute.getMass(self.moles_solute)
        gSolvent = self.solvent.getMass(self.moles_solvent)
        s = gSolute / (100 * gSolvent)

        if s > solubility: return "Oversaturated"
        if s == solubility: return "Saturated"
        return "Unsaturated"

    def checkSolution(self):
        if not self.dissovles(): return "You must have a solution that dissolves"
        if not self.aqueous(): return "You must have an aqueous solution"
        return None

    def boilingPoint(self):
        K = bpElevationConstants.get(self.solvent.getEq())
        if K == None: K = round(random.random() * 9 + 1, 2)

        try: return  miscBps.get(self.solvent.getEq()) + self.particlesPerSolute() * K * self.molality()
        except: return None
        
    def freezingPoint(self):
        K = fpDepressionConstants.get(self.solvent.getEq())
        if K == None: raise Exception(f"no constant found: {self.solute.equation()}")

        try: return miscFps.get(self.solvent.getEq()) - self.particlesPerSolute() * K * self.molality()
        except: return None

    def particlesPerSolute(self):
        if self.solute.isMolecular(): return 1
        if len(self.solute.uniqueEls()) == 2: return self.solute.totalAtoms()

        else:
            m, n = ionizeTernaryIonic(self.solute.equation)
            m = m[1]
            n = n[1]
            commonFactor = gcd(m,n)
            m /= commonFactor
            n /= commonFactor
            return int(m + n)

class AB_blueprint:
    def __init__(self, moles = None, volume = 1, molarity = 1):
        self.acid = compound("H2O")
        self.base = compound("H2O")
        self.c_acid = compound("H3O", 1)
        self.c_base = compound("OH", -1)

        if moles: self.molarity = moles / volume
        else: self.molarity = molarity

        self.volume = volume
        self.K_eq = "LARGE"

        self.bl_rx : reaction = None

        self.eq = "H2O"

    def HConc(self):
        # Handle strong acids/bases (K_eq = 9e200) as special case
        # Strong acids/bases undergo complete dissociation
        if self.K_eq >= 1e100:
            # Check if this is an acid or base by examining the class type
            if isinstance(self, acid):
                # Strong acid: [H+] = molarity (complete dissociation)
                return self.molarity
            elif isinstance(self, base):
                # Strong base: [OH-] = molarity × (number of OH groups)
                # Then [H+] = Kw / [OH-] where Kw = 1e-14

                # Determine number of OH groups from the base equation
                oh_groups = 1
                if "(OH)2" in self.base.equation:
                    oh_groups = 2

                oh_conc = self.molarity * oh_groups
                return 1e-14 / oh_conc

        # Weak acids/bases: use equilibrium calculation.
        # Floor to a tiny positive value: after a common-ion shift H+ can be
        # driven arbitrarily close to 0 (log10 would crash on 0/negative).
        return max(self.bl_rx.prodEqConcs[0], 1e-20)
    
    def pH(self):
        return -1 * log10(self.HConc())

    def pOH(self):
        return 14 - self.pH()
    
    def OHConc(self):
        # Handle strong bases as special case
        if self.K_eq >= 1e100 and isinstance(self, base):
            # Strong base: [OH-] = molarity × (number of OH groups)
            oh_groups = 1
            if "(OH)2" in self.base.equation:
                oh_groups = 2
            return self.molarity * oh_groups

        # For acids and weak bases: use Kw relationship
        return (10 ** -14) / (self.HConc())

    def addCommonIon(self, added_molarity):
        prod_eq, _ = self.bl_rx.eqExpression()
        common_ion_index = 0
        if prod_eq[0][0].equation in ["OH", "H3O", "H"]: common_ion_index = 1

        newProdConcs = self.bl_rx.prodEqConcs
        newProdConcs[common_ion_index] += added_molarity

        self.bl_rx.eqConcsFromIntial(newProdConcs, [self.molarity])

    def moles(self):
        return self.molarity * self.volume
    
    def __str__(self) -> str:
        return f"{round_sig(self.volume)} L of {round_sig(self.molarity)} M {self.eq}"

    def __repr__(self) -> str:
        return self.__str__()

class acid(AB_blueprint):
    def __init__(self, acid_eq =None, moles=None, volume=1, molarity=1):
        super().__init__(moles, volume, molarity)

        if "_" in acid_eq: eq, charge = acid_eq.split("_")
        else: eq, charge = acid_eq, 0
        
        self.acid = compound(eq, charge)
        self.base = compound("H2O")
        self.c_acid = compound("H3O", 1)
        
        c_base = list(self.acid.equation)
        if c_base[1].isnumeric():
            c_base[1] = str(int(c_base[1]) - 1)
            if c_base[1] == "1": c_base[1] = ""
        else: c_base = c_base[1:]

        self.c_base = compound("".join(c_base), int(self.acid.charge) - 1)

        self.K_eq = KaDict[eq+("_"+str(charge)) * (charge != 0)]
        if self.K_eq == "LARGE": self.K_eq = 9e200

        self.bl_rx = reaction(["a", [self.acid, self.base], [self.c_acid, self.c_base], [self.molarity, self.K_eq]])
        self.eq = self.acid.__repr__()

class base(AB_blueprint):
    def __init__(self, base_eq = None, moles=None, volume=1, molarity=1):
        super().__init__(moles, volume, molarity)

        self.base = compound(base_eq)
        self.acid = compound("H", 1)
        self.c_base = compound("OH", -1)
        
        if "(OH)2" in base_eq:
            c_acid_eq, c_acid_charge = base_eq[:2], 2
        elif "OH" in base_eq:
            c_acid_eq, c_acid_charge = base_eq[:-2], 1
        else:
            if base_eq[-1] == "H":
                c_acid_eq, c_acid_charge = base_eq + "2", 1
            if base_eq[-2] == "H":
                c_acid_eq, c_acid_charge = base_eq[:-1] + str(int(base_eq[-1]) + 1), 1
            else:
                c_acid_eq, c_acid_charge = base_eq + "H", 1

        self.c_acid = compound(c_acid_eq, c_acid_charge)

        self.K_eq = KbDict[base_eq]
        if self.K_eq == "LARGE": self.K_eq = 9e200

        self.bl_rx = reaction(["b", [self.base], [self.c_base, self.c_acid], [self.molarity, self.K_eq]])
        self.eq = self.base.__repr__()

# this has an error with computing the leftover moles and salt moles
class neutralization(reaction):
    def __init__(self, acidInput, baseInput):
        self.acid = acidInput
        self.base = baseInput
        self.totVol = self.acid.volume + self.base.volume
        acidIon = ionize_ab(self.acid.acid)
        baseIon = ionize_ab(self.base.base)
        self.salt = compound(ionicCompoundFromElements(m = baseIon, n = acidIon))
        super().__init__(["n", [self.acid.acid, self.base.base], [self.salt, compound("H2O")]])
        # acid + base -> salt + H2O
        # this part only works for strong acids and bases
        reacts, prods = self.formatRxList()
        leftover_moles = self.acid.moles() / reacts[0][1] - self.base.moles() / reacts[1][1]

        if leftover_moles >= 0: # base is limiting or stoiciometric mixture
            self.leftover_ab = acid(self.acid.acid.equation, moles = leftover_moles, volume = self.totVol)
            self.salt_moles = prods[0][1] * self.base.moles() / reacts[1][1]
        else: # acid is limiting
            self.leftover_ab = base(self.base.base.equation, moles = -leftover_moles, volume = self.totVol)
            self.salt_moles = prods[0][1] * self.acid.moles() / reacts[0][1]


