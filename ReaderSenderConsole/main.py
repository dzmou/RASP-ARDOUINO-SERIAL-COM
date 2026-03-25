import serial
import threading
import time

# Function for the reading thread
def read_from_port(ser):
    while True:
        if ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8').rstrip()
                print(f"\n[RECEIVE]: {line}")
            except Exception as e:
                print(f"Read error: {e}")
                break

# Function for the sending thread
def send_to_port(ser):
    while True:
        msg = input("[SEND]: ")
        if msg:
            ser.write(('\n==============================='+msg + '\n').encode('utf-8'))

if __name__ == '__main__':
    # Adjust port and baudrate as needed
    serial_port = '/dev/ttyACM0'
    baud_rate = 9600
    
    try:
        ser = serial.Serial(serial_port, baud_rate, timeout=1)
        ser.flush()
        print(f"Connected to {serial_port}")

        # Create threads
        reader = threading.Thread(target=read_from_port, args=(ser,), daemon=True)
        writer = threading.Thread(target=send_to_port, args=(ser,), daemon=True)

        # Start threads
        reader.start()
        writer.start()

        # Keep the main thread alive
        while True:
            time.sleep(1)

    except serial.SerialException as e:
        print(f"Error: Could not open serial port: {e}")
    except KeyboardInterrupt:
        print("\nClosing program...")