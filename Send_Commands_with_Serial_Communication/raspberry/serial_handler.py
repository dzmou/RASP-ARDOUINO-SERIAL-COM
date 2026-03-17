"""
Handles the serial communication between the Raspberry Pi and the Arduino.
"""
import serial
import time
from config import SERIAL_PORT, BAUD_RATE, TIMEOUT

# Global serial instance
ser = None

def connect():
    """
    Establish a serial connection with the Arduino using the parameters defined in config.
    Returns:
        bool: True if connection is successful, False otherwise.
    """
    global ser
    
    # Return early if we are already connected
    if is_connected():
        return True
        
    try:
        # Initialize the serial connection
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
        time.sleep(2)  # Wait for Arduino to reset after connection
        return is_connected()
    except serial.SerialException as e:
        print(f"Error connecting to Arduino on {SERIAL_PORT}: {e}")
        ser = None
        return False

def send_command(cmd):
    """
    Send a command string to the Arduino and read the response.
    
    Args:
        cmd (str): The command to send.
        
    Returns:
        str: The response from the Arduino, or an empty string if no response.
    """
    # Append newline, encode to bytes, and write to the serial port
    ser.write((cmd + '\n').encode('utf-8'))
    
    # Wait briefly for the Arduino to process the command and reply
    time.sleep(0.1)
    
    response = ""
    # Check if there is data waiting to be read from the serial buffer
    if ser.in_waiting:
        # Read the line, decode it to string, and remove whitespace/newlines
        response = ser.readline().decode('utf-8').strip() # strip() removes whitespace/newlines
    return response

def is_connected():
    """
    Check if the serial connection to the Arduino is currently open.
    
    Returns:
        bool: True if connected and open, False otherwise.
    """
    return ser is not None and ser.is_open

def disconnect():
    """
    Close the serial connection to the Arduino if it is currently open.
    """
    global ser
    if is_connected():
        try:
            ser.close()
            print("Serial connection closed.")
        except Exception as e:
            print(f"Error closing serial connection: {e}")