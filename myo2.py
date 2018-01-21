from myo import init, Hub, Feed

from sensors import SensorDebug

import time



class MyoC:

    maVariable = "3"

    def __init__(self):
        self.attribut = 'default value'
        global maVariable
        maVariable = "1"
        init('bin')
        

    def setValue(cls,val):
        global maVariable
        maVariable = val
    
    def returnValue():
        return maVariable

    @classmethod
    def myoCommand(cls, status):

        
        feed = Feed()
        hub = Hub()
        hub.run(1000, feed)

        global maVariable
        
        try:
            myo = feed.wait_for_single_device(timeout=2.0)
            if not myo:
                print("No Myo connected after 2 seconds")
                quit()
            print("Hello, Myo!")
            instance = SensorDebug()

            myos = feed.get_connected_devices()
                
            while hub.running and myo.connected:
                quat = myo.orientation
                #print('Orientation:', quat.x, quat.y, quat.z, quat.w)
                print (myos[0], myos[0].pose)
                
                #print (myos[0].pose)
                #print (myo.pose) #// This code crash the IDE for unknow reason



                if myo.pose == "wave_in":
                  print("pose wave_in")
                  maVariable="1"
                  break
                
                elif myo.pose == "wave_out":
                  print("pose wave_out") 
                  maVariable="2"
                  break
                else:
                  print("pas de position")
                  maVariable="3"
                
                time.sleep(0.01)


                
        finally:
            hub.shutdown()  # !! crucial

            return maVariable
