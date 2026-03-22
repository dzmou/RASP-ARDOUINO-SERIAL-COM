#ifndef SENSORS_H
#define SENSORS_H

#include "am2302.h"   // Real AM2302 / DHT22 driver

// ── Pin Definitions ───────────────────────────────────────────
#define DHT_PIN       4    // AM2302 data pin
#define WIND_SPD_PIN  A0   // Anemometer analog input
#define WIND_DIR_PIN  A1   // Wind vane analog input
#define LUX_PIN       A2   // LDR / BH1750 analog input

// ── Simulated Wind & Lux state (replace with real sensors later)
static float  _windSpd    = 0.0;
static int    _windDirIdx = 0;
static int    _lux        = 500;
static int    _simTick    = 0;

const char* windDirs[] = {"N","NE","E","SE","S","SW","W","NW"};

// ── Initialise all sensors — call once in setup() ─────────────
inline void setupSensors() {
  am2302Begin();   // warm-up AM2302 and start readings
}

// ── Simulate drifting wind & lux values ───────────────────────
inline void updateSimulatedSensors() {
  _simTick++;
  _windSpd = max(0.0f, _windSpd + (random(-5, 6)) * 0.1f);
  _lux    += random(-30, 31);
  _windSpd = constrain(_windSpd, 0.0f, 30.0f);
  _lux     = constrain(_lux, 0, 65000);
  // Rotate wind direction slowly
  if (_simTick % 10 == 0) _windDirIdx = (_windDirIdx + 1) % 8;
}

// ── Read Functions ─────────────────────────────────────────────
inline float readTemp()            { return am2302Temp(); }    // real AM2302
inline float readHumidity()        { return am2302Hum(); }     // real AM2302
inline float readWindSpeed()       { return _windSpd; }        // simulated
inline const char* readWindDir()   { return windDirs[_windDirIdx]; } // simulated
inline int   readLux()             { return _lux; }            // simulated

// ── Print helpers ──────────────────────────────────────────────
inline void printAllSensors() {
  Serial.print(F("[DATA] temp="));    Serial.print(readTemp(), 1);
  Serial.print(F(" hum="));           Serial.print(readHumidity(), 1);
  Serial.print(F(" wind_spd="));      Serial.print(readWindSpeed(), 1);
  Serial.print(F(" wind_dir="));      Serial.print(readWindDir());
  Serial.print(F(" lux="));           Serial.println(readLux());
}

#endif
