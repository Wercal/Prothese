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
        time.sleep(0.5)
        ser.baudrate = 9600
        ser.port = 'COM8'

        try:
            ser.open()
            
            for x in range(0, 200):
                time.sleep(0.01)

                arduino_status="null"
                    
                try:
                    arduino_status = ser.readline().decode()
                except UnicodeDecodeError:
                    print(ser.readline())
                    
                if ("free" in arduino_status):
                    
                    if status == "1":
                        ser.write(b'a')
                    if status == "2":
                        ser.write(b'b')
                    break

            time.sleep(0.5)
        finally:
            ser.close()
        