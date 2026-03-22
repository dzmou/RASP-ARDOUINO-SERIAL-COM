# 🤖 Arduino — WebConsole

Sensor station firmware with real-time JSON streaming.

## 📂 Files

| File | Description |
|------|-------------|
| `Arduino.ino` | Main sketch — setup, loop, command handler |
| `sensors.h` | Sensor read functions (integrates AM2302) |
| `am2302.h` | AM2302 / DHT22 driver wrapper |
| `led_control.h` | LED pin control + state tracking |

## ⚙️ Streaming

Arduino is idle by default. When streaming is enabled (`stream on`), it sends a JSON packet every `streamInterval` seconds:

```json
{"streaming":true,"ts":4521000,"temp":24.3,"hum":58.1,"wind_spd":3.2,"wind_dir":"NE","lux":812,"leds":{"red":false,"green":true,"blue":false}}
```

### Commands
| Command | Behaviour |
|------|-----------|
| `stream on` | Start continuous streaming |
| `stream off` | Stop streaming (idle) |
| `interval <s>` | Set interval in seconds (1-86400) |
| `menu` | Show all available commands |
| `status` | Show connection and interval status |

## 🔌 Pin Map

| Pin | Component |
|-----|-----------|
| D4  | DHT22 data |
| D8  | Blue LED |
| D9  | Green LED |
| D10 | Red LED |
| A0  | Anemometer (analog) |
| A1  | Wind vane (analog) |
| A2  | LDR luminosity |

## 🛠️ Upload

1. Open `Arduino.ino` in Arduino IDE
2. **Tools → Board** → Arduino Uno (or your board)
3. **Tools → Port** → select your COM / ttyUSB port
4. Click **Upload**
5. Open Serial Monitor at `9600` baud to observe

## 🔧 Replacing Simulated Sensors

In `sensors.h`, replace the body of each `readXxx()` function with real sensor reads:

```cpp
// Example: DHT22 real read
#include <DHT.h>
DHT dht(DHT_PIN, DHT22);
inline float readTemp()     { return dht.readTemperature(); }
inline float readHumidity() { return dht.readHumidity(); }
```
