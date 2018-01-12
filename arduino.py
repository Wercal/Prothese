"""class to use the arduino"""
import serial

class Arduino:
    """base class for the engine"""


    def __init__(self):
        self.attribut = 'engine default value'

    @classmethod
    def onboardled(cls, status):
        """ blink led """
        ser = serial.Serial()
        ser.baudrate = 9600
        ser.port = 'COM8'
        ser.open()
        if status == "H":
            ser.write(b'H')
        else:
            ser.write(b'L')
        ser.close()
        