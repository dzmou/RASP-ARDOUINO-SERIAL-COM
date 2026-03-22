// ════════════════════════════════════════════════════════════════
//  am2302.h — Real AM2302 / DHT22 Sensor Driver
//  Requires: DHT sensor library by Adafruit (DHT.h)
// ════════════════════════════════════════════════════════════════
#ifndef AM2302_H
#define AM2302_H

#include <DHT.h>

// ── Pin (defined in sensors.h, must be included first) ────────
#ifndef DHT_PIN
  #define DHT_PIN 4
#endif

// ── Sensor object — AM2302 is the wired variant of DHT22 ──────
static DHT _dht(DHT_PIN, DHT22);

// ── Last valid readings (cached when sensor returns NaN) ──────
static float _lastTemp = 0.0;
static float _lastHum  = 0.0;

// ── Initialise — call once in setup() ─────────────────────────
inline void am2302Begin() {
  _dht.begin();
}

// ── Read temperature (°C), returns last valid value on error ──
inline float am2302Temp() {
  float t = _dht.readTemperature();
  if (!isnan(t)) _lastTemp = t;
  return _lastTemp;
}

// ── Read relative humidity (%), returns last valid value on error
inline float am2302Hum() {
  float h = _dht.readHumidity();
  if (!isnan(h)) _lastHum = h;
  return _lastHum;
}

#endif // AM2302_H
