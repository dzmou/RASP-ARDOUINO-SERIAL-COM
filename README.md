# RASP-ARDOUINO-SERIAL-COM

This repository demonstrates bi-directional **Serial Communication between a Raspberry Pi and an Arduino**. It consists of two main projects: one for reading sensor data from the Arduino, and another for sending control commands from the Raspberry Pi to the Arduino via a Web API.

---

## 📁 Project Structure

```text
RASP-ARDOUINO-SERIAL-COM/
├── Read_Serial_Communication_with_Raspberry_Pi/  # Part 1: Arduino -> Raspberry Pi
│   ├── Ardouino sketch.txt                       # Arduino code to read temp sensor
│   └── Python Script.py                          # Python script to read serial data
└── Send_Commands_with_Serial_Communication/      # Part 2: Raspberry Pi -> Arduino
    ├── Ardouino/                                 # Arduino code for LED control
    │   └── sketch.txt                            
    └── raspberry/                        # Flask Web API to handle commands
        ├── api.py                                # Main Flask server
        ├── serial_handler.py                     # Serial communication logic
        └── README.md                             # Sub-project specific documentation
```

---

## Part 1: Reading Serial Communication (Arduino -> Raspberry Pi)

This section focuses on retrieving analog sensor data (e.g., Temperature) read by the Arduino and logging it on the Raspberry Pi.

### How it works:
- **Arduino**: Reads the analog voltage from `A0` (Temperature Sensor LM35/TMP36), converts the voltage into degrees Celsius and Fahrenheit, and outputs this data through the serial port (`9600` baud rate).
- **Raspberry Pi**: Uses the `pyserial` library to listen to `/dev/ttyACM0` and continuously prints the streamed data in real-time.

### Running it:
1. Upload the `Ardouino sketch.txt` content to your Arduino UNO/Mega.
2. Connect your Arduino to the Raspberry Pi via USB.
3. Run the Python script on your Raspberry Pi:
   ```bash
   cd Read_Serial_Communication_with_Raspberry_Pi
   python3 "Python Script.py"
   ```

---

## Part 2: Sending Commands (Raspberry Pi -> Arduino)

This section demonstrates how to control hardware attached to an Arduino (like RGB LEDs) via network requests directed to the Raspberry Pi.

### How it works:
- **Arduino (`Ardouino/sketch.txt`)**: Listens to the Serial port (`9600` baud rate). Based on the string command received (`white`/`blue`/`red`/`all`/`off`), it toggles digital pins `8`, `9`, and `10` HIGH or LOW to control LED states.
- **Raspberry Pi (`raspberry/api.py`)**: Runs a **Flask Web API** server that accepts HTTP POST/GET requests. The routing logic captures the command and uses `serial_handler.py` to transmit it via the USB serial connection (`/dev/ttyUSB0` or `/dev/ttyACM0`) using `pyserial`. It also offers a web interface (`index.html`).

### Running it:
1. Wire up your LEDs to pins 8, 9, and 10 of the Arduino and upload the sketch.
2. Connect the Arduino to your Raspberry Pi via USB.
3. On the Raspberry Pi, navigate to the Web API folder and run it:
   ```bash
   cd Send_Commands_with_Serial_Communication/raspberry
   pip install -r requirements.txt
   python3 api.py
   ```
4. Access the web interface at `http://<raspberrypi-ip>:5000/` or send an API POST request:
   ```bash
   curl -X POST http://localhost:5000/led \
        -H "Content-Type: application/json" \
        -d '{"command": "red"}'
   ```

_For detailed documentation on the API endpoints and setup for Part 2, refer to [Send_Commands_with_Serial_Communication/raspberry/README.md](Send_Commands_with_Serial_Communication/raspberry/README.md)._
