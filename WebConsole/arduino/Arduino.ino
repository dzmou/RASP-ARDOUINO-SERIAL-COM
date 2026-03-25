// ════════════════════════════════════════════════════════════════
//  WebConsole_Serial_Communication_with_Raspberry_Pi
//  Arduino Sensor Station — Default / Interactive / Hybrid Mode
//  github.com/dzmou/RASP-ARDOUINO-SERIAL-COM
// ════════════════════════════════════════════════════════════════

#include "sensors.h"
#include "led_control.h"

// ── Globals ───────────────────────────────────────────────────
bool          isStreaming    = false;
unsigned long streamInterval = 2000;       // ms between stream packets (default 2 s)
unsigned long lastStream     = 0;
String        cmdBuffer      = "";
LedState      leds;
char          lineDelim      = '\n';   // Default breakline char

// ── Delimiter Helper ──────────────────────────────────────────
void printlnDelim(const __FlashStringHelper* s, bool isLast = false) {
  Serial.print(s);
  if (lineDelim == '\n' || isLast) Serial.println();
  else Serial.print(lineDelim);
}
void printlnDelim(const String &s, bool isLast = false) {
  Serial.print(s);
  if (lineDelim == '\n' || isLast) Serial.println();
  else Serial.print(lineDelim);
}

// ── Interactive Menu ──────────────────────────────────────────
void printMenu() {
  printlnDelim(F("[MENU]"));
  printlnDelim(F("  read              - Read all sensors"));
  printlnDelim(F("  read temp         - Temperature only"));
  printlnDelim(F("  read hum          - Humidity only"));
  printlnDelim(F("  read wind         - Wind speed & direction"));
  printlnDelim(F("  read lux          - Luminosity only"));
  printlnDelim(F("  led <color> on/off- Control LED (red/green/blue)"));
  printlnDelim(F("  led all on/off    - All LEDs on or off"));
  printlnDelim(F("  interval <s>      - Set stream interval in seconds (1-60)"));
  printlnDelim(F("  delim <char>      - Set breakline char (e.g. '|' or '\\n')"));
  printlnDelim(F("  status            - Device info & current state"));
  printlnDelim(F("  stream on         - Start continuous sensor streaming"));
  printlnDelim(F("  stream off        - Stop continuous sensor streaming"));
  printlnDelim(F("  reset             - Soft reset device"));
  printlnDelim(F("  ping              - Health check"));
  printlnDelim(F("  menu              - Show this menu"));
  printlnDelim(F("[END MENU]"), true);
}

// ── Setup ─────────────────────────────────────────────────────
void setup() {
  Serial.begin(9600);
  setupLeds();
  setupSensors();    // initialise AM2302 (includes 2 s warm-up)
  randomSeed(analogRead(A5));

  delay(500);   // Let serial settle after reset
  Serial.println(F("[BOOT] RA WEB-CONSOLE v1.0"));
  Serial.println(F("[BOOT] Idle — streaming OFF by default"));
  Serial.print(F("[BOOT] Interval: "));
  Serial.print(streamInterval / 1000);
  Serial.println(F(" s"));
  printMenu();  // Show available commands on boot
}

// ── Main Loop ─────────────────────────────────────────────────
void loop() {
  readSerial();
  updateSimulatedSensors();

  unsigned long now = millis();

  if (isStreaming) {
    if (now - lastStream >= streamInterval) {
      lastStream = now;
      streamPacket();
    }
  }
}

// ── Stream JSON Packet ────────────────────────────────────────
void streamPacket() {
  Serial.print(F("{\"streaming\":true,\"ts\":"));
  Serial.print(millis());
  Serial.print(F(",\"temp\":"));
  Serial.print(readTemp(), 1);
  Serial.print(F(",\"hum\":"));
  Serial.print(readHumidity(), 1);
  Serial.print(F(",\"wind_spd\":"));
  Serial.print(readWindSpeed(), 1);
  Serial.print(F(",\"wind_dir\":\""));
  Serial.print(readWindDir());
  Serial.print(F("\",\"lux\":"));
  Serial.print(readLux());
  Serial.print(F(","));
  printLedJson();
  Serial.println(F("}"));
}

// ── Serial Command Reader ─────────────────────────────────────
void readSerial() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n' || c == '\r') {
      cmdBuffer.trim();
      if (cmdBuffer.length() > 0) {
        handleCommand(cmdBuffer);
        cmdBuffer = "";
      }
    } else {
      cmdBuffer += c;
    }
  }
}

// ── Command Handler ───────────────────────────────────────────
void handleCommand(String cmd) {
  cmd.toLowerCase();
  cmd.trim();

  // ── Streaming toggles ──
  if (cmd == "stream on") {
    isStreaming = true;
    lastStream = 0;
    Serial.println(F("[STREAM] Streaming ON"));
    return;
  }
  if (cmd == "stream off") {
    isStreaming = false;
    Serial.println(F("[STREAM] Streaming OFF"));
    return;
  }

  // ── Interactive / Hybrid commands ──
  if (cmd == "menu") {
    printMenu();
    return;
  }

  if (cmd == "ping") {
    Serial.print(F("[PONG] alive streaming="));
    Serial.print(isStreaming ? "ON" : "OFF");
    Serial.print(F(" uptime="));
    Serial.print(millis() / 1000);
    Serial.println(F("s"));
    return;
  }

  if (cmd == "status") {
    Serial.print(F("[STATUS] streaming=")); printlnDelim(isStreaming ? "ON" : "OFF");
    Serial.print(F("[STATUS] interval="));  Serial.print(streamInterval / 1000); printlnDelim(F("s"));
    Serial.print(F("[STATUS] uptime="));    Serial.print(millis()/1000);  printlnDelim(F("s"));
    Serial.print(F("[STATUS] fw=v1.0 delim='"));
    if (lineDelim == '\n') Serial.print(F("\\n")); else Serial.print(lineDelim);
    printlnDelim(F("'"), true);
    printLedStatus();
    return;
  }

  if (cmd == "read") {
    updateSimulatedSensors();
    printAllSensors();
    printLedStatus();
    Serial.println(); // Final flush
    return;
  }
  if (cmd == "read temp") {
    Serial.print(F("[DATA] temp=")); printlnDelim(String(readTemp(), 1), true);
    return;
  }
  if (cmd == "read hum") {
    Serial.print(F("[DATA] hum=")); printlnDelim(String(readHumidity(), 1), true);
    return;
  }
  if (cmd == "read wind") {
    Serial.print(F("[DATA] wind_spd=")); Serial.print(readWindSpeed(), 1);
    Serial.print(F(" wind_dir="));       printlnDelim(readWindDir(), true);
    return;
  }
  if (cmd == "read lux") {
    Serial.print(F("[DATA] lux=")); printlnDelim(String(readLux()), true);
    return;
  }

  // ── LED: led <color> <on|off> ──
  if (cmd.startsWith("led ")) {
    String args  = cmd.substring(4);
    int    space = args.indexOf(' ');
    if (space == -1) {
      Serial.println(F("[ERR] Usage: led <color> on/off"));
      return;
    }
    String color = args.substring(0, space);
    String state = args.substring(space + 1);
    state.trim(); color.trim();

    if (state != "on" && state != "off") {
      Serial.println(F("[ERR] State must be 'on' or 'off'"));
      return;
    }
    bool on = (state == "on");
    setLed(color.c_str(), on);
    Serial.print(F("[LED] ")); Serial.print(color);
    Serial.print(F(" -> ")); Serial.println(state);
    return;
  }

  // ── Interval: interval <s> ──
  if (cmd.startsWith("interval ")) {
    long val = cmd.substring(9).toInt();
    if (val < 1 || val > 24 * 60 * 60) { // min : 1s , max : 24h
      Serial.println(F("[ERR] Interval out of range (1s-86400s(24h)) "));
    } else {
      streamInterval = (unsigned long)(val * 1000); // Convert seconds to milliseconds
      Serial.print(F("[CFG] Interval set to "));
      Serial.print(val);
      Serial.println(F(" s"));
    }
    return;
  }

  // ── Delimiter: delim <char> ──
  if (cmd.startsWith("delim ")) {
    String arg = cmd.substring(6);
    arg.trim();
    if (arg == "\\n" || arg == "newline") {
      lineDelim = '\n';
    } else if (arg.length() > 0) {
      lineDelim = arg[0];
    }
    Serial.print(F("[CFG] Delimiter set to '"));
    if (lineDelim == '\n') Serial.print(F("\\n")); else Serial.print(lineDelim);
    Serial.println(F("'"));
    return;
  }

  // ── Reset ──
  if (cmd == "reset") {
    Serial.println(F("[RESET] Restarting in 1s…"));
    delay(1000);
    // Soft reset via watchdog — uncomment if avr/wdt.h is available
    // wdt_enable(WDTO_15MS); while(1) {}
    // Fallback: jump to 0
    asm volatile ("jmp 0");
    return;
  }

  // ── Unknown ──
  Serial.print(F("[ERR] Unknown command: "));
  Serial.println(cmd);
  if (!isStreaming) {
    Serial.println(F("      Type 'menu' for available commands."));
  }
}
