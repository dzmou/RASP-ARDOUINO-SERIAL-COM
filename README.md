# RASP-ARDUINO-SERIAL-COM

This repository demonstrates bi-directional **Serial Communication between a Raspberry Pi and an Arduino**. It consists of three parts: one for reading sensor data, one for sending control commands via a simple Web API, and a full-featured Web Console.

---

## 📁 Project Structure

```text
RASP-ARDUINO-SERIAL-COM/
├── SerialReader/             # Part 1: Arduino -> Raspberry Pi (Simple Stream)
│   ├── "Ardouino sketch.txt"  # Arduino code to read temp sensor
│   └── "Python Script.py"     # Python script to read serial data
├── CommandSender/            # Part 2: Raspberry Pi -> Arduino (Command Execution)
│   ├── arduino/              # Arduino code for LED control
│   │   └── sketch.txt                            
│   └── raspberry/            # Flask Web API to handle commands
│       ├── api.py            # Main Flask server
│       ├── serial_handler.py # Serial communication logic
│       └── README.md         # Sub-project documentation
└── WebConsole/               # Part 3: Raspberry Pi <=> Arduino (Full-featured Console)
    ├── Arduino/              # Sensor station firmware (JSON Streaming)
    │   ├── Arduino.ino       # Main sketch
    │   ├── sensors.h         # Sensor logic (includes real AM2302)
    │   └── am2302.h          # DHT22/AM2302 driver
    └── Raspberry/            # Flask API + Modern Web Console
        ├── flask_app/        # Web application backend & frontend
        │   ├── app.py        # Entry point
        │   └── templates/    # HTML UI (Console)
        ├── run.sh            # One-click startup script
        └── requirements.txt  # Dependencies
```

---

## Part 1: Reading Serial Communication (Arduino -> Raspberry Pi)

This section focuses on retrieving analog sensor data (e.g., Temperature) read by the Arduino and logging it on the Raspberry Pi.

### How it works:
- **Arduino**: Reads the analog voltage from `A0` (Temperature Sensor LM35/TMP36), converts it to Celsius, and outputs to serial (`9600` baud).
- **Raspberry Pi**: Uses `pyserial` to listen to `/dev/ttyACM0` and prints the streamed data in real-time.

### Running it:
1. Upload `SerialReader/"Ardouino sketch.txt"` to your Arduino.
2. Run the script: `cd SerialReader && python3 "Python Script.py"`.

---

## Part 2: Sending Commands (Raspberry Pi -> Arduino)

Control hardware attached to an Arduino (like RGB LEDs) via network requests directed to the Raspberry Pi.

### How it works:
- **Arduino**: Listens for commands (`red`, `green`, `blue`, etc.) and toggles pins 8, 9, 10.
- **Raspberry Pi**: Runs a Flask server that translates HTTP POST requests to Serial commands.

### Running it:
1. Upload the sketch from `CommandSender/arduino/sketch.txt`.
2. Start the API: `cd CommandSender/raspberry && python3 api.py`.
3. Control via browser or `curl`:
   ```bash
   curl -X POST http://localhost:5000/led -d '{"command": "red"}'
   ```

---

## Part 3: Web Console (Bi-directional)

A modern web interface with real-time JSON streaming, automatic CSV logging, and full command control.

### Features:
- **Streaming ON/OFF**: Toggle continuous sensor updates from the UI.
- **Custom Interval**: Set reading speed in seconds (1s to 24h).
- **Auto Logging**: Readings are saved to `Raspberry/flask_app/data/` as CSV files.
- **Real-time Terminal**: See raw serial traffic in the browser.

### Running it:
1. Flash the Arduino: `cd WebConsole/Arduino && upload Arduino.ino`.
2. Start the Pi: `cd WebConsole/Raspberry && ./run.sh`.
3. Open `http://<pi-ip>:5000/`.

_For detailed documentation on the API and setup, refer to [WebConsole/README.md](WebConsole/README.md)._
