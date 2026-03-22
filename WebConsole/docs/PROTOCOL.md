# 📡 Serial Communication Protocol

**Port:** `/dev/ttyUSB0`  **Baud:** `9600`  **Line ending:** `\n`

---

## 1. Sensor Streaming

When streaming is enabled (`stream on`), the Arduino sends a JSON line every `STREAM_INTERVAL` s (default 2 s):

```json
{"streaming":true,"ts":12345,"temp":24.3,"hum":58.1,"wind_spd":3.2,"wind_dir":"NE","lux":812,"leds":{"red":false,"green":true,"blue":false}}
```

| Field | Type | Unit | Description |
|-------|------|------|-------------|
| `streaming` | bool | — | Always `true` when sent from the autonomous stream |
| `ts` | int | ms | `millis()` timestamp |
| `temp` | float | °C | Temperature |
| `hum` | float | % | Humidity |
| `wind_spd` | float | m/s | Wind speed |
| `wind_dir` | string | — | Cardinal direction (N/NE/E/SE/S/SW/W/NW) |
| `lux` | int | lux | Sun luminosity |
| `leds` | object | — | LED states |

---

## 2. Serial Commands

### Commands sent by Raspberry Pi → Arduino

| Command | Description |
|---------|-------------|
| `menu` | Print interactive menu |
| `read` | Read all sensors once |
| `read temp` | Read temperature only |
| `read hum` | Read humidity only |
| `read wind` | Read wind speed + direction |
| `read lux` | Read luminosity only |
| `led red on` | Turn red LED on |
| `led red off` | Turn red LED off |
| `led green on` | Turn green LED on |
| `led green off` | Turn green LED off |
| `led blue on` | Turn blue LED on |
| `led blue off` | Turn blue LED off |
| `led all on` | All LEDs on |
| `led all off` | All LEDs off |
| `interval <s>` | Set stream interval in seconds (e.g. `interval 5`) |
| `status` | Device info + current streaming state |
| `stream on` | Start continuous sensor streaming |
| `stream off` | Stop continuous sensor streaming |
| `reset` | Soft reset Arduino |
| `ping` | Health check |

### Arduino Responses

```
[MENU]
  read              - Read all sensors
  read temp         - Temperature only
  read hum          - Humidity only
  read wind         - Wind speed & direction
  read lux          - Luminosity only
  led <color> on/off- Control LED (red/green/blue)
  led all on/off    - All LEDs on or off
  interval <s>      - Set stream interval in seconds (1-86400(24h))
  status            - Device info & current state
  stream on         - Start continuous sensor streaming
  stream off        - Stop continuous sensor streaming
  reset             - Soft reset device
  ping              - Health check
  menu              - Show this menu
[END MENU]
```

---

## 4. Error Responses

```
[ERR] Unknown command: <cmd>
[ERR] Invalid LED color: <color>
[ERR] Interval out of range (1-86400(24h))
```
