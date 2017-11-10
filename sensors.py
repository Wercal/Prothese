"""class to use the sensors"""
from random import choice


class Sensor:
    """base class for the sensors"""

    def __init__(self):
        self.attribut = 'value'


    def a_method(self):
        """ print a value"""
        print(self.attribut)


class SensorDebug:
    """class that return random data, use for debug only"""

    def __init__(self):
        self.attribut = 'this is a debug attribut'


    def a_method(self):
        """this is a method that print a value"""
        print(self.attribut)

    def getMovement(self):
        """get random movement"""
        states = "open closed right left".split()
        return choice(states)
