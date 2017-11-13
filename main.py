"""Main file, used to start the application"""
import time
from sensors import SensorDebug

from arduino import Arduino



class Main:
    """ main class """


    instance = SensorDebug()
    #print(instance.getMovement())

    arduinoInstance = Arduino()

    t_end = time.time() + 5 # 5 seconds

    while time.time() < t_end:
        arduinoInstance.onboardled("H")

    #print("Hello World!")
