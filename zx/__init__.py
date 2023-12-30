# CRISTIAN ECHEVERRÍA RABÍ

from . import zx
from .zx import *

#-----------------------------------------------------------------------------------------

version = "0.9.0"
__version__ = version

#-----------------------------------------------------------------------------------------
# Category instances to use as constants

CC_CU     = zx.Category(12000.0, 0.0000169,  0.0, 0.00374)      # COPPER
CC_AAAC   = zx.Category( 6450.0, 0.0000230, 20.0, 0.00340)      # AAAC (AASC)
CC_ACAR   = zx.Category( 6450.0, 0.0000250, 20.0, 0.00385)      # ACAR
CC_ACSR   = zx.Category( 8000.0, 0.0000191, 20.0, 0.00395)      # ACSR
CC_AAC    = zx.Category( 5600.0, 0.0000230, 20.0, 0.00395)      # ALUMINUM
CC_CUWELD = zx.Category(16200.0, 0.0000130,  0.0, 0.00380)      # COPPERWELD
CC_AASC   = CC_AAAC
CC_ALL    = CC_AAC

#-----------------------------------------------------------------------------------------

class CategoryMaker(object):
    """ Mutable object to create inmutable Category objects
        Same arguments that Category
    """
    __slots__ = ('modelas', 'coefexp', 'creep', 'alpha')
    
    def __init__(self, modelas=0.0, coefexp=0.0, creep=0.0, alpha=0.0):
        self.modelas = modelas
        self.coefexp = coefexp
        self.creep = creep
        self.alpha = alpha
    
    @staticmethod
    def fromCategory(c):
        """ staticmethod: Returns CategoryMaker object from Category object
            c : Category object
        """
        return CategoryMaker(c.modelas, c.coefexp, c.creep, c.alpha)

    def get(self):
        return zx.Category(self.modelas, self.coefexp, self.creep, self.alpha)

#-----------------------------------------------------------------------------------------

class ConductorMaker(object):
    """ Mutable object to create inmutable Conductor objects
        Same arguments that Conductor except category is replaced for catmk
        catmk : CategoryMaker object
    """
    __slots__ = ('catmk', 'diameter', 'area', 'weight', 'strength', 'r25', 'hcap')
    
    def __init__(self, catmk, diameter=0.0, area=0.0, weight=0.0, strength=0.0, r25=0.0,
                 hcap=0.0):
        self.catmk = catmk
        self.diameter = diameter
        self.area = area
        self.weight = weight
        self.strength = strength
        self.r25 = r25
        self.hcap = hcap

    def get(self):
        return zx.Conductor(self.catmk.get(), self.diameter, self.area, self.weight, 
                            self.strength, self.r25, self.hcap)
