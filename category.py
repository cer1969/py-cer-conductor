# CRISTIAN ECHEVERRÍA RABÍ

__all__ = ['Category', 'CC_CU', 'CC_AAAC', 'CC_ACAR', 'CC_ACSR', 'CC_AAC', 'CC_CUWELD',
           'CC_AASC', 'CC_ALL',]

#-----------------------------------------------------------------------------------------

class Category(object):
    """Represents a category of conductors with similar characteristics"""
    
    __slots__ = ('name', 'modelas', 'coefexp', 'creep', 'alpha', 'idx')
    
    def __init__(self, name='', modelas=0.0, coefexp=0.0, creep=0.0, alpha=0.0, idx=None):
        """
        name    : Name of conductor category
        modelas : Modulus of elasticity [kg/mm2]
        coefexp : Coefficient of Thermal Expansion [1/°C]
        creep   : Creep [°C]
        alpha   : Temperature coefficient of resistance [1/°C]
        idx     : Database key
        """
        self.name = name
        self.modelas = modelas
        self.coefexp = coefexp
        self.creep = creep
        self.alpha = alpha
        self.idx = idx

    def __str__(self):
        return self.name

#-----------------------------------------------------------------------------------------
# Category instances to use as constants

CC_CU     = Category('COPPER',      12000.0, 0.0000169,  0.0, 0.00374, 'CU')
CC_AAAC   = Category('AAAC (AASC)',  6450.0, 0.0000230, 20.0, 0.00340, 'AAAC')
CC_ACAR   = Category('ACAR',         6450.0, 0.0000250, 20.0, 0.00385, 'ACAR')
CC_ACSR   = Category('ACSR',         8000.0, 0.0000191, 20.0, 0.00395, 'ACSR')
CC_AAC    = Category('ALUMINUM',     5600.0, 0.0000230, 20.0, 0.00395, 'AAC')
CC_CUWELD = Category('COPPERWELD',  16200.0, 0.0000130,  0.0, 0.00380, 'CUWELD')
CC_AASC   = CC_AAAC
CC_ALL    = CC_AAC
