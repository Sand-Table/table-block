import serial
import time

# Open grbl serial port ==> CHANGE THIS BELOW TO MATCH YOUR USB LOCATION
s = serial.Serial('/dev/cu.usbserial-10', 115200)  # GRBL operates at 115200 baud. Leave that part alone.
s.write(b"\r\n\r\n")


def write_design():

    # Open g-code file
    f = open('grbl.gcode', 'r')

    # Wake up grbl
    #time.sleep(5)  # Wait for grbl to initialize
    s.flushInput()  # Flush startup text in serial input
    #s.write(str.encode('$H' + '\n'))

    # Stream g-code to grbl
    for line in f:
        l = line.strip()  # Strip all EOL characters for consistency
        print('Sending: ' + l)
        s.write(str.encode(l + '\n'))  # Send g-code block to grbl
        grbl_out = s.readline()  # Wait for grbl response with carriage return
        print(' : ' + grbl_out.strip().decode())

    # Wait here until grbl is finished to close serial port and file.
    print("  Press <Enter> to exit and disable grbl.")

    # Close file and serial port
    f.close()

def close_serial():
    s.close()
