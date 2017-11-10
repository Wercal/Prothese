"""Main file, used to start the application"""
from sensors import SensorDebug

class Main:
    """ main class """


    instance = SensorDebug()
    print(instance.getMovement())

    #print("Hello World!")
