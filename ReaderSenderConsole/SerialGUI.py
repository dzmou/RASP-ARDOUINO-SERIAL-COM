import serial
import threading
import tkinter as tk
from tkinter import scrolledtext

class SerialGui:
    def __init__(self, root, serial_port):
        self.root = root
        self.ser = serial_port
        self.root.title("Serial Monitor")

        # 0. UI Responsiveness setup
        root.grid_rowconfigure(0, weight=1)      # Row 0 (display) expands
        root.grid_columnconfigure(0, weight=1)   # Column 0 (entry box) expands

        # 1. UI Setup: Scrolled Text area for reading
        self.display = scrolledtext.ScrolledText(root, state='disabled', height=15, width=50)
        self.display.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky='nsew')

        # 2. UI Setup: Entry box for sending
        self.input_field = tk.Entry(root)
        self.input_field.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        self.input_field.bind("<Return>", self.send_command) # Press Enter to send

        # 3. UI Setup: Send Button
        self.send_button = tk.Button(root, text="Send", command=self.send_command)
        self.send_button.grid(row=1, column=1, padx=10, pady=10, sticky='e')

        # Start the background reading thread
        self.read_thread = threading.Thread(target=self.listen_serial, daemon=True)
        self.read_thread.start()

    def listen_serial(self):
        """Continuously reads from serial and updates the GUI."""
        while True:
            if self.ser.in_waiting > 0:
                try:
                    line = self.ser.readline().decode('utf-8').rstrip()
                    self.update_display(f"DEVICE: {line}")
                except Exception as e:
                    self.update_display(f"SYSTEM ERROR: {e}")
                    break

    def send_command(self, event=None):
        """Gets text from entry box and writes to serial port."""
        msg = self.input_field.get()
        if msg:
            self.ser.write((msg + '\n').encode('utf-8'))
            self.update_display(f"YOU: {msg}")
            self.input_field.delete(0, tk.END)

    def update_display(self, text):
        """Safely updates the text area from any thread."""
        self.display.configure(state='normal')
        self.display.insert(tk.END, text + '\n')
        self.display.configure(state='disabled')
        self.display.see(tk.END) # Auto-scroll to bottom

if __name__ == '__main__':
    # Configuration
    PORT = '/dev/ttyACM0'
    BAUD = 9600

    try:
        # Initialize Serial
        ser = serial.Serial(PORT, BAUD, timeout=1)
        ser.flush()

        # Initialize GUI
        root = tk.Tk()
        gui = SerialGui(root, ser)
        root.mainloop()

    except serial.SerialException as e:
        print(f"Failed to connect on {PORT}: {e}")