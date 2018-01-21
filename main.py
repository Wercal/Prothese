"""Main file, used to start the application"""
import time
from sensors import SensorDebug

from arduino import Arduino

from myo2 import MyoC

class Main:
    """ main class """

    

    instance = SensorDebug()
    #print(instance.getMovement())

    arduinoInstance = Arduino()

    t_end = time.time() + 5 # 5 seconds

    #while time.time() < t_end:


   # arduinoInstance.onboardled("1")

    
    print ("starting")
    myoinstance = MyoC()
    #myoinstance.setValue(0)
    #myoinstance.myoCommand("tata")
    
    while True:
        #arduinoInstance.onboardled(myoinstance.maVariable)
        zzz = myoinstance.myoCommand("tata")

        toto =123

        print(zzz)
        print(myoinstance.returnValue)
        print(myoinstance.maVariable)


        arduinoInstance.onboardled(zzz)
        time.sleep(0.5)
