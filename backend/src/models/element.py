from src.utils.parsing import findElement
from src.utils.generators import randElement
from src.utils.math_helpers import findPeriod
from chemData import *

class element:
    def __init__(self, eq = None, elData = None, charge = 0) -> None:
        if elData == None:
            if eq == None: eq = randElement()[2]
            self.eq = eq
            try:
                self.elData = findElement(self.eq)
            except: raise Exception("Invalid elemnt: " + self.eq)
        else:
            self.elData = elData
            self.eq = elData[2]

        # should only be the magnitude of the charge, the sign will be decided later
        self.charge = charge

    def getCharge(self):
        if self.isMetal(): return self.charge

        return -self.charge

    def isMetal(self):
        number = self.getAtomicNumber()
        return number in [3, 4, 11, 12, 19, 20, 37, 38, 55, 56, 87, 88]
    
    def isSemimetal(self):
        number = self.getAtomicNumber()
        return number in [5, 14, 32, 33, 51, 52, 84, 85]

    def getGroup(self):
        group = self.elData[3]
        if group in ["1a", "2a"]: return float(group[0])
        if "b" in group: return float(group[0]) + 2
        if "n" in group:
            num = self.getAtomicNumber()

            if num in [58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]:
                return 3 + (num - 57) / 15
            if num in [90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103]:
                return 3 + (num - 89) / 15
            
            raise Exception("bad tm, num: " + str(num))
        return float(group[0]) + 10
    
    def getAtomicNumber(self):
        return int(self.elData[0])

    def getPeriod(self):
        return int(findPeriod(self.getAtomicNumber()))

    def getEN(self):
        return electronegativities.get(self.eq)

    def compareSize(self, other): # return self's size - other's size (+ if self is bigger, 0 if its the same, - if self is smaller)
        if other.getCharge() > self.getCharge(): return 1
        if other.getCharge() < self.getCharge(): return -1

        return -self.compareIE(other)

    def compareEN(self, other): # + if self is more electronegative, 0 if its the same, - if self is less electronegative
        myEN = self.getEN()
        otherEN = self.getEN()

        if myEN == None or otherEN == None:
            return self.compareIE(other)
        else:
            diff = myEN - otherEN
            if diff == 0: return 0
            return diff // abs(diff)

    def compareIE(self, other): # + if self has more IE, 0 if its the same, - if self has less IE
        if self.eq == "He" and other.eq == "He": return 0
        if self.eq == "He": return 1
        if other.eq == "He": return -1

        if self.eq == "H" and other.eq == "H": return 0
        if self.eq == "H": return 1
        if other.eq == "He": return -1

        if self.isMetal() and not other.isMetal(): return -1
        if other.isMetal() and not self.isMetal(): return 1

        if self.isSemimetal() and not other.isSemimetal(): return -1
        if other.isSemimetal() and not self.isSemimetal(): return 1

        if self.getGroup() > other.getGroup(): return 1
        if self.getGroup() < other.getGroup(): return -1

        if self.getPeriod() > other.getPeriod(): return -1
        if self.getPeriod() < other.getPeriod(): return 1

        return 0
    
    def compareEA(self, other): # + if self's EA is more exothermic (more negative), 0 if its the same, - if self's EA is less exothermic (less negative)
        return self.compareIE(other)
    
    def __str__(self) -> str:
        return f"{self.eq} {self.getCharge()}"
    
    def getPhase(self):
        n = self.getAtomicNumber()
        if n in [35, 80]: return "l"
        if n in [1, 2, 7, 8, 9, 10, 17, 18, 36, 5, 86]: return "g"
        return "s"
