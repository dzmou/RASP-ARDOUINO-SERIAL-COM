# 🔌 WebConsole

A full-stack serial communication project between a **Raspberry Pi** (Flask API + Web Console) and an **Arduino** (sensor station).

---

## 📁 Project Structure

```
WebConsole/
├── Arduino/
│   ├── Arduino.ino                        # Main sketch
│   ├── sensors.h                          # Sensor read functions
│   ├── am2302.h                           # AM2302 / DHT22 driver
│   ├── led_control.h                      # LED control functions
│   └── README.md
├── Raspberry/
│   ├── flask_app/
│   │   ├── app.py                         # Flask entry point
│   │   ├── config.py                      # Configuration
│   │   ├── serial_handler_rasp.py         # Serial read/write thread
│   │   ├── csv_logger_rasp.py             # CSV data logger
│   │   ├── routes_rasp/
│   │   │   ├── __init__.py
│   │   │   ├── api.py                     # REST API routes
│   │   │   └── web.py                     # Web UI routes
│   │   └── templates/
│   │       └── index.html                 # Web console
│   ├── requirements.txt
│   ├── run.sh
│   └── README.md
├── docs/
│   └── PROTOCOL.md                        # Serial protocol specification
└── README.md                              # ← You are here
```

---

## ⚙️ Streaming Sensor Data

By default, the Arduino is completely idle and only acts when commands are sent. It can be toggled to continuously stream sensor data to the web console:

| Command | Behaviour |
|------|-----------|
| `stream on` | Arduino streams sensor data continuously at the configured interval |
| `stream off` | Stops sensor streaming and returns to idle state |

---

## 🚀 Quick Start

### 1. Flash Arduino
- Open `Arduino/Arduino.ino` in Arduino IDE
- Select your board & port, upload

### 2. Setup Raspberry Pi
```bash
cd Raspberry
pip install -r requirements.txt --break-system-packages
chmod +x run.sh
./run.sh
```

### 3. Open Console
Navigate to `http://<raspberry-ip>:5000` in your browser.

---

## 🔌 Hardware

| Component | Connection |
|-----------|-----------|
| Arduino Uno/Nano | USB → Raspberry Pi (`/dev/ttyUSB0`) |
| Green LED | Pin 9 |
| Blue LED | Pin 8 |
| Red LED | Pin 10 |
| DHT22 / AM2302 | Pin 4 |
| Anemometer (analog) | A0 |
| Wind vane (analog) | A1 |
| LDR / BH1750 | A2 |

---

## 📡 Serial Protocol

See [`docs/PROTOCOL.md`](docs/PROTOCOL.md) for full message format specification.

---

## 📋 Requirements

- Raspberry Pi (any model with USB)
- Arduino Uno / Nano / Mega
- Python 3.8+
- Arduino IDE 1.8+
