# Raspberry Pi ↔ Arduino LED Controller

Control Arduino RGB LEDs via HTTP API from Raspberry Pi.
## Project Folders Tree
```
raspberry/
├── api.py
├── serial_handler.py
├── config.py
├── routes/
│   ├── status.py
│   ├── led.py
│   └── other.py
├── templates/
│   └── index.html
├── requirements.txt
└── README.md
```

## Setup

### 1. Install dependencies
```
pip3 install -r requirements.txt --break-system-packages
```

### 2. Check serial port
```
ls /dev/ttyUSB*
ls /dev/ttyACM*
```

### 3. Set port in config.py
```python
SERIAL_PORT = '/dev/ttyUSB0'  # or /dev/ttyACM0
```

### 4. Run
```
python3 api.py
```

---

## Endpoints

| Method | Endpoint | Description           |
|--------|----------|-----------------------|
| GET    | /status  | API and serial status |
| GET    | /led     | List valid commands   |
| POST   | /led     | Send LED command      |
| POST   | /other   | Send other command    |

---

## LED Commands

| Command | Effect                  |
|---------|-------------------------|
| green   | Green LED on, others off|
| blue    | Blue LED on, others off |
| red     | Red LED on, others off  |
| all     | All LEDs on             |
| off     | All LEDs off            |
| test    | Test command            |
|  ?      | any thing else          |

---

## Examples

### Turn on red LED
```
curl -X POST http://raspberrypi.local:5000/led \
     -H "Content-Type: application/json" \
     -d '{"command": "red"}'
```

### Turn off all
```
curl -X POST http://raspberrypi.local:5000/led \
     -H "Content-Type: application/json" \
     -d '{"command": "off"}'
```

### Send an other command
```
curl -X POST http://raspberrypi.local:5000/other \
     -H "Content-Type: application/json" \
     -d '{"command": "shutdown"}'
```

### status check
```
curl http://raspberrypi.local:5000/status
```

---

## Wiring

| Arduino Pin | LED   |
|-------------|-------|
| 8           | Blue  |
| 9           | Green |
| 10          | Red   |
| GND         | GND   |

---

## Auto-start on Boot

```
crontab -e
# Add:
@reboot python3 /home/pi/raspberry/api.py &
```