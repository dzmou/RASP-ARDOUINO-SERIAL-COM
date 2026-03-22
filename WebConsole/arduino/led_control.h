#ifndef LED_CONTROL_H
#define LED_CONTROL_H

// ── Pin Definitions ───────────────────────────────────────────
#define LED_RED   10
#define LED_GREEN  9
#define LED_BLUE   8

// ── State ─────────────────────────────────────────────────────
struct LedState {
  bool red   = false;
  bool green = false;
  bool blue  = false;
};

extern LedState leds;

// ── Setup ─────────────────────────────────────────────────────
inline void setupLeds() {
  pinMode(LED_RED,   OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_BLUE,  OUTPUT);
  digitalWrite(LED_RED,   LOW);
  digitalWrite(LED_GREEN, LOW);
  digitalWrite(LED_BLUE,  LOW);
}

// ── Control ───────────────────────────────────────────────────
inline void setLed(const char* color, bool state) {
  if (strcmp(color, "red") == 0) {
    leds.red = state;
    digitalWrite(LED_RED, state ? HIGH : LOW);
  } else if (strcmp(color, "green") == 0) {
    leds.green = state;
    digitalWrite(LED_GREEN, state ? HIGH : LOW);
  } else if (strcmp(color, "blue") == 0) {
    leds.blue = state;
    digitalWrite(LED_BLUE, state ? HIGH : LOW);
  } else if (strcmp(color, "all") == 0) {
    leds.red = leds.green = leds.blue = state;
    digitalWrite(LED_RED,   state ? HIGH : LOW);
    digitalWrite(LED_GREEN, state ? HIGH : LOW);
    digitalWrite(LED_BLUE,  state ? HIGH : LOW);
  }
}

// ── LED Status String ─────────────────────────────────────────
inline void printLedStatus() {
  Serial.print(F("[LED] red="));   Serial.print(leds.red   ? "ON" : "OFF");
  Serial.print(F(" green="));      Serial.print(leds.green ? "ON" : "OFF");
  Serial.print(F(" blue="));       Serial.println(leds.blue  ? "ON" : "OFF");
}

// ── LED JSON fragment ─────────────────────────────────────────
// Writes: "leds":{"red":false,"green":true,"blue":false}
inline void printLedJson() {
  Serial.print(F("\"leds\":{\"red\":"));
  Serial.print(leds.red   ? "true" : "false");
  Serial.print(F(",\"green\":"));
  Serial.print(leds.green ? "true" : "false");
  Serial.print(F(",\"blue\":"));
  Serial.print(leds.blue  ? "true" : "false");
  Serial.print(F("}"));
}

#endif
