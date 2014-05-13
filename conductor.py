# CRISTIAN ECHEVERRÍA RABÍ

__all__ = ['Conductor']

#-----------------------------------------------------------------------------------------

class Conductor(object):
    """Container for conductor characteristics"""
    
    __slots__ = ('name', 'category', 'diameter', 'area', 'weight', 'strength', 'r25',
                 'hcap', 'idx')
    
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
        self.name = name
        self.category = category
        self.diameter = diameter
        self.area = area
        self.weight = weight
        self.strength = strength
        self.r25 = r25
        self.hcap = hcap
        self.idx = idx

    def __str__(self):
        return self.name