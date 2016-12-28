# CRISTIAN ECHEVERRÍA RABÍ

__all__ = ['Conductor', 'ConductorMaker']

#-----------------------------------------------------------------------------------------

class ConductorMaker(object):
    """Mutable object to create inmutable Conductor objects
       Same arguments that Conductor
    """
    __slots__ = ('name', 'category', 'diameter', 'area', 'weight', 'strength', 'r25',
                 'hcap', 'idx')
    
    def __init__(self, name='', category=None, diameter=0.0, area=0.0, weight=0.0, strength=0.0,
                 r25=0.0, hcap=0.0, idx=None):
        self.name = name
        self.category = category
        self.diameter = diameter
        self.area = area
        self.weight = weight
        self.strength = strength
        self.r25 = r25
        self.hcap = hcap
        self.idx = idx

    def get(self):
        return Conductor(self.name, self.category, self.diameter, self.area, self.weight, 
                         self.strength, self.r25, self.hcap, self.idx)

    def __str__(self):
        return "ConductorMaker: %s" % self.name

#-----------------------------------------------------------------------------------------

class Conductor(object):
    """Container for conductor characteristics"""
    
    __slots__ = ('_name', '_category', '_diameter', '_area', '_weight', '_strength', '_r25',
                 '_hcap', '_idx')
    
    def __init__(self, name='', category=None, diameter=0.0, area=0.0, weight=0.0,
                 strength=0.0, r25=0.0, hcap=0.0, idx=None):
        """
        name     : Name of conductor
        category : Category instance
        diameter : Diameter [mm]
        area     : Cross section area [mm2]
        weight   : Weight per unit [kg/m]
        strength : Rated strength [kg]
        r25      : Resistance at 25°C [Ohm/km]
        hcap     : Heat capacity [kcal/(ft*°C)]
        idx      : Database key
        """
        self._name = name
        self._category = category
        self._diameter = diameter
        self._area = area
        self._weight = weight
        self._strength = strength
        self._r25 = r25
        self._hcap = hcap
        self._idx = idx

    @property
    def name(self):
        return self._name
    
    @property
    def category(self):
        return self._category
    
    @property
    def diameter(self):
        return self._diameter
    
    @property
    def area(self):
        return self._area
    
    @property
    def weight(self):
        return self._weight
    
    @property
    def strength(self):
        return self._strength
    
    @property
    def r25(self):
        return self._r25
    
    @property
    def hcap(self):
        return self._hcap
    
    @property
    def idx(self):
        return self._idx
    
    def __str__(self):
        return "Conductor: %s" % self.name