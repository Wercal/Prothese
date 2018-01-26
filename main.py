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

    derniere_commmande=-1
    
    while True:
        #arduinoInstance.onboardled(myoinstance.maVariable)
        myo_command = myoinstance.myoCommand("tata")

        toto =123

        
        print(myoinstance.returnValue)
        print(myoinstance.maVariable)

        if (derniere_commmande!=myo_command):
            print ("Commande envoye au arduino")
            print (myo_command)
            derniere_commmande=myo_command
            arduinoInstance.onboardled(myo_command)
            time.sleep(13)
