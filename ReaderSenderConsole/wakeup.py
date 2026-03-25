import serial
import time

# Configuration based on device specs
SERIAL_PORT = '/dev/ttyACM0'  # Adjust for your specific Raspberry Pi port
BAUD_RATE = 9600
WAKEUP_CHAR = b'1'  # Any numeric key (0-9) works
ESC_CHAR = b'\x1b'  # ESC character to return to sleep/log mode

def wakeup_datahog():
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print("Initiating wake-up sequence (duration: 12 seconds)...")
            
            start_time = time.time()
            # Send numeric key repeatedly for slightly over the 10s wake-up period
            while time.time() - start_time < 12:
                ser.write(WAKEUP_CHAR)
                time.sleep(1)  # Interval between attempts
                
                # Check if device responded with the Main Menu
                if ser.in_waiting > 0:
                    response = ser.read(ser.in_waiting).decode('ascii', errors='ignore')
                    if "Main Menu" in response or response.strip():
                        print("Device Awakened: Main Menu accessed.")
                        return True
            
            print("Wake-up attempt complete.")
    except Exception as e:
        print(f"Connection Error: {e}")
    return False

def sleep_datahog():
    # Sending ESC returns the device to sleep/log mode
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            ser.write(ESC_CHAR)
            print("ESC sent: Device returning to sleep/logging mode.")
    except Exception as e:
        print(f"Error sending sleep command: {e}")

if __name__ == "__main__":
    if wakeup_datahog():
        # Perform your data ingestion or configuration here
        # display wakeup success message
        print("\n\n\nWakeup success\n\n\n")
        # keep read serial to display the menu 
        while True:
            if ser.in_waiting > 0:
                response = ser.read(ser.in_waiting).decode('ascii', errors='ignore')
                print(response)