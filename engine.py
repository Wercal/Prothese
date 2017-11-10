"""class to use the engine"""
from random import choice


class Engine:
    """base class for the engine"""

    def __init__(self):
        self.attribut = 'engine default value'

    def method(self):
        """ print a value"""
        print(self.attribut)


class EngineDebug:
    """class that return random data, use for debug only"""

    def __init__(self):
        self.attribut = 'this is a debug attribut'

    def a_method(self):
        """this is a method that print a value"""
        print(self.attribut)

    def setMovement(self):
        """return random finger movement value"""
        states = "Pollex SecundusManus MediusManus Annularis QuintusManus".split()
        return choice(states)
