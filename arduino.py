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
        ser.port = 'COM9'
        ser.open()
        if status == "1":
            ser.write(b'a')
        if status == "2":
            ser.write(b'b')
        ser.close()
        