import serial
import serial.tools.list_ports
import threading
import time

class SerialBackend:
    """Handles serial communication logic independently of the GUI."""
    def __init__(self, callback):
        self.ser = None
        self.callback = callback
        self.running = False
        self.thread = None
        self.port = None
        self.baud = 9600

    def list_ports(self):
        """Returns a list of available serial port names."""
        return [p.device for p in serial.tools.list_ports.comports()]

    def connect(self, port, baud=9600):
        """Attempts to open a serial connection and starts the read thread."""
        self.disconnect()
        try:
            self.ser = serial.Serial(port, baud, timeout=0.1)
            self.port = port
            self.baud = baud
            self.running = True
            self.thread = threading.Thread(target=self._listen, daemon=True)
            self.thread.start()
            return True, "Connected"
        except Exception as e:
            return False, str(e)

    def disconnect(self):
        """Stops the read thread and closes the serial port."""
        self.running = False
        if self.ser and self.ser.is_open:
            try:
                self.ser.close()
            except:
                pass
        if self.thread and self.thread.is_alive():
            # Listen loop usually ends quickly due to 'running' flag
            self.thread.join(timeout=0.2)
        self.ser = None

    def write(self, msg):
        """Sends a message to the serial port."""
        if self.ser and self.ser.is_open:
            try:
                self.ser.write((msg + '\n').encode('utf-8'))
                return True
            except:
                return False
        return False

    def _listen(self):
        """Background thread loop for reading serial data."""
        while self.running:
            if self.ser and self.ser.is_open:
                try:
                    if self.ser.in_waiting > 0:
                        line = self.ser.readline().decode('utf-8', errors='replace').rstrip()
                        if line:
                            self.callback(f"\t: {line}")
                except Exception as e:
                    self.callback(f"SYSTEM ERROR: {e}")
                    self.running = False
                    break
            time.sleep(0.01)
