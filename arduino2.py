import serial
import time 

ser = serial.Serial()
time.sleep(2)
ser.baudrate = 9600
ser.port = 'COM9'
ser.open()


while True:
    ser.write(b'a')
    time.sleep(0.2)
    ser.write(b'b')  

ser.write(b'c')
time.sleep(0.5)

ser.close()