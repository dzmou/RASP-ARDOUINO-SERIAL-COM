"""
Configuration settings for the Raspberry Pi to Arduino serial communication.
"""

PORT        = 5000 # endpoint port
DEBUG       = True # debug mode

# serial port, for connected Ardouino 
SERIAL_PORT = '/dev/ttyACM0' # or '/dev/ttyUSB0'

# Ardouino code values, they should be simalar to Ardouino code
BAUD_RATE   = 9600 
TIMEOUT     = 2
HOST        = '0.0.0.0'

VALID_COMMANDS = ["green", "blue", "red", "all", "off","test"]
