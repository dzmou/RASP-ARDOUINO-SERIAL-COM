# 🍓 Raspberry Pi — WebConsole

Flask API server + Web Console for the Arduino sensor station.

## 📂 Structure

```
Raspberry/
├── flask_app/
│   ├── app.py               # Entry point
│   ├── config.py            # Port, baud, CSV settings
│   ├── serial_handler_rasp.py    # Background serial thread
│   ├── csv_logger_rasp.py        # Automatic CSV data logging
│   ├── routes_rasp/
│   │   ├── api.py           # REST endpoints
│   │   └── web.py           # Serves web console
│   └── templates/
│       └── index.html       # Web console UI
├── requirements.txt
└── run.sh
```

## 🚀 Quick Start

```bash
# 1. Grant serial port access (once)
sudo usermod -a -G dialout $USER
# Log out and back in for the group change to take effect

# 2. Install & run
cd Raspberry
chmod +x run.sh
./run.sh
```

Open browser at `http://localhost:5000` (or `http://<pi-ip>:5000` from another device).

## 🔧 Configuration

Edit `flask_app/config.py` or set environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `SERIAL_PORT` | `/dev/ttyUSB0` | Arduino serial port |
| `SERIAL_BAUD` | `9600` | Baud rate |
| `FLASK_PORT` | `5000` | Web server port |
| `CSV_DIR` | `data` | Directory for CSV logs |
| `CSV_MAX_ROWS` | `10000` | Rows before CSV rotates |

## 📡 REST API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/status` | Connection status + latest data |
| GET | `/api/data` | Latest sensor snapshot |
| GET | `/api/log?n=100` | Last N raw serial lines |
| POST | `/api/send` | Send raw command `{"command":"ping"}` |
| POST | `/api/led` | LED control `{"color":"red","state":"on"}` |
| POST | `/api/stream` | Toggle stream `{"state":"on"}` |
| POST | `/api/interval` | Set interval `{"s":5}` |
| GET | `/api/csv` | List CSV data files |
| GET | `/api/csv/<file>` | Download CSV file |

## 📊 CSV Data

Sensor readings are auto-logged to `flask_app/data/readings_YYYY-MM-DD.csv`.

Columns: `timestamp, streaming, ts_ms, temp, hum, wind_spd, wind_dir, lux, led_red, led_green, led_blue`

Files rotate daily and when they exceed `CSV_MAX_ROWS`.
Download files via the web console or `GET /api/csv/<filename>`.
