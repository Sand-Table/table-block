import serial
from time import sleep
dev = serial.Serial("/dev/ttyUSB0", baudrate=115200)

dev.write(b'G0 G54 G17 G21 G90 G94 M5 M9 T0 F0 S0')
dev.write(b'G91 X1 Y0 F1')
print("done")