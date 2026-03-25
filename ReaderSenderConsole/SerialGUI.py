import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
from serial_backend import SerialBackend

class SerialGui:
    """Manages the Tkinter interface and interacts with SerialBackend."""
    def __init__(self, root):
        self.root = root
        self.root.title("Serial Monitor Pro")
        self.root.geometry("700x500")
        
        self.backend = SerialBackend(self.on_receive)
        self.font_size = 11
        self.is_connected = False

        self.setup_ui()
        self.refresh_ports()

    def setup_ui(self):
        """Initializes the UI components and responsiveness settings."""
        # 0. Grid Responsiveness
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # 1. Toolbar (Top)
        toolbar = tk.Frame(self.root, padx=10, pady=5, relief=tk.RAISED, borderwidth=1)
        toolbar.grid(row=0, column=0, sticky='ew')

        tk.Label(toolbar, text="PORT:").pack(side=tk.LEFT)
        self.port_combo = ttk.Combobox(toolbar, width=20, state="readonly")
        self.port_combo.pack(side=tk.LEFT, padx=5)
        
        self.conn_btn = tk.Button(toolbar, text="Connect", command=self.toggle_connection, width=12, bg="#e1e1e1")
        self.conn_btn.pack(side=tk.LEFT, padx=5)

        # Spacer
        tk.Frame(toolbar, width=20).pack(side=tk.LEFT)

        tk.Button(toolbar, text="Clear Log", command=self.clear_log).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="WakeUP", command=self.wake_up, bg="#fffec8").pack(side=tk.LEFT, padx=10) # Dedicated WakeUp button
        tk.Button(toolbar, text="Font +", command=lambda: self.change_font(1)).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="Font -", command=lambda: self.change_font(-1)).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="Reset Font", command=lambda: self.change_font(0)).pack(side=tk.LEFT, padx=2)

        # 2. Terminal Display (Middle)
        self.display = scrolledtext.ScrolledText(self.root, state='disabled', font=("Consolas", self.font_size), bg="#1e1e1e", fg="#d4d4d4")
        self.display.grid(row=1, column=0, padx=10, pady=(0,5), sticky='nsew')
        
        # Tag coloring
        self.display.tag_config("system", foreground="#569cd6")
        self.display.tag_config("user", foreground="#ce9178")
        self.display.tag_config("device", foreground="#b5cea8")
        self.display.tag_config("error", foreground="#f44747")

        # 3. Command Input (Bottom)
        input_frame = tk.Frame(self.root, padx=10, pady=10)
        input_frame.grid(row=2, column=0, sticky='ew')
        input_frame.grid_columnconfigure(0, weight=1)

        self.input_field = tk.Entry(input_frame, font=("Segoe UI", 10))
        self.input_field.grid(row=0, column=0, sticky='ew', padx=(0,5))
        self.input_field.bind("<Return>", self.send_command)

        self.send_btn = tk.Button(input_frame, text="SEND COMMAND", command=self.send_command, width=15, bg="#007acc", fg="white", font=("Segoe UI", 9, "bold"))
        self.send_btn.grid(row=0, column=1)

    def on_receive(self, text):
        """Thread-safe callback to handle received data."""
        self.root.after(0, self._update_display, text)

    def _update_display(self, text):
        """Appends text to the display widget with appropriate tagging."""
        self.display.configure(state='normal')
        
        tag = None
        if text.startswith("SYSTEM"): tag = "system"
        elif text.startswith("YOU"): tag = "user"
        elif text.startswith("\t:"): tag = "device" # Match the new tab prefix
        elif "ERROR" in text: tag = "error"
        
        self.display.insert(tk.END, text + '\n', tag)
        self.display.configure(state='disabled')
        self.display.see(tk.END)

    def send_command(self, event=None):
        """Reads input field and writes to serial through backend."""
        msg = self.input_field.get().strip()
        if msg:
            if self.backend.write(msg):
                self._update_display(f"YOU: {msg}")
                self.input_field.delete(0, tk.END)
            elif not self.is_connected:
                messagebox.showwarning("Warning", "Serial is not connected.")
            else:
                self._update_display("SYSTEM: Write failed.")

    def toggle_connection(self):
        """Connects or disconnects the serial port based on current state."""
        if not self.is_connected:
            port = self.port_combo.get()
            if not port:
                messagebox.showwarning("Warning", "Select a port first.")
                return
            
            ok, msg = self.backend.connect(port)
            if ok:
                self.is_connected = True
                self.conn_btn.config(text="Disconnect", bg="#ffcccb")
                self._update_display(f"SYSTEM: Connected to {port} @ 9600 baud.")
            else:
                messagebox.showerror("Error", f"Could not open {port}: {msg}")
        else:
            self.backend.disconnect()
            self.is_connected = False
            self.conn_btn.config(text="Connect", bg="#e1e1e1")
            self._update_display("SYSTEM: Disconnected.")

    def clear_log(self):
        """Clears the terminal window."""
        self.display.configure(state='normal')
        self.display.delete('1.0', tk.END)
        self.display.configure(state='disabled')

    def wake_up(self):
        """Sends a numeric key ('1') to wake up the device without newline."""
        #if self.backend.write_raw("1"):
        if self.backend.write_nb_1():
            self._update_display("YOU: [WakeUP] 1 (raw)")
        elif not self.is_connected:
            messagebox.showwarning("Warning", "Serial is not connected.")

    def change_font(self, delta):
        """Adjusts font size or resets to default."""
        if delta == 0:
            self.font_size = 11
        else:
            self.font_size = max(6, min(30, self.font_size + delta))
        self.display.config(font=("Consolas", self.font_size))

    def refresh_ports(self):
        """Periodically scans for available COM ports."""
        current = self.port_combo.get()
        ports = self.backend.list_ports()
        self.port_combo['values'] = ports
        
        if current in ports:
            self.port_combo.set(current)
        elif ports and not current:
            self.port_combo.current(0)
            
        # Rescan every 3 seconds
        self.root.after(3000, self.refresh_ports)

if __name__ == '__main__':
    root = tk.Tk()
    app = SerialGui(root)
    root.mainloop()