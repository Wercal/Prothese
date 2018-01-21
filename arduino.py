"""class to use the arduino"""
import serial
import time
class Arduino:
    """base class for the engine"""


    def __init__(self):
        self.attribut = 'engine default value'

    @classmethod
    def onboardled(cls, status):
        """ blink led """
        ser = serial.Serial()
        time.sleep(2)
        ser.baudrate = 9600
        ser.port = 'COM9'
        ser.open()

        if status == "1":
            for x in range(10):
                ser.write(b'a')
                time.sleep(0.2)
                ser.write(b'c')
                time.sleep(0.2)
        if status == "2":
             for x in range(10):
                ser.write(b'b')
                time.sleep(0.2)
                ser.write(b'c')
                time.sleep(0.2)

        time.sleep(0.2)
        ser.close()
        