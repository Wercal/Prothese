from myo import init, Hub, Feed

from sensors import SensorDebug

init('bin')
feed = Feed()
hub = Hub()
hub.run(1000, feed)

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
    #print(quat.getMovement())

    #print('Orientation:', myo.orientation)
    #print(instance.getMovement())
    print (myos[0], myos[0].pose)
    
    #print (myo.pose) // This code crash the IDE for unknow reason
    
  

finally:
  hub.shutdown()  # !! crucial