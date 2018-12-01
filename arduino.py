import serial
import time
ser = serial.Serial('/dev/ttyACM0')
ser.baudrate = 9600
# ser = serial.Serial('COM3', 9600)
time.sleep(2)
ser.write(str.encode("Unknown#"))

