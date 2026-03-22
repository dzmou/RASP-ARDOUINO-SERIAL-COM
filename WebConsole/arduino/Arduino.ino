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

// ── Interactive Menu ──────────────────────────────────────────
void printMenu() {
  Serial.println(F("[MENU]"));
  Serial.println(F("  read              - Read all sensors"));
  Serial.println(F("  read temp         - Temperature only"));
  Serial.println(F("  read hum          - Humidity only"));
  Serial.println(F("  read wind         - Wind speed & direction"));
  Serial.println(F("  read lux          - Luminosity only"));
  Serial.println(F("  led <color> on/off- Control LED (red/green/blue)"));
  Serial.println(F("  led all on/off    - All LEDs on or off"));
  Serial.println(F("  interval <s>      - Set stream interval in seconds (1-60)"));
  Serial.println(F("  status            - Device info & current state"));
  Serial.println(F("  stream on         - Start continuous sensor streaming"));
  Serial.println(F("  stream off        - Stop continuous sensor streaming"));
  Serial.println(F("  reset             - Soft reset device"));
  Serial.println(F("  ping              - Health check"));
  Serial.println(F("  menu              - Show this menu"));
  Serial.println(F("[END MENU]"));
}

// ── Setup ─────────────────────────────────────────────────────
void setup() {
  Serial.begin(9600);
  setupLeds();
  setupSensors();    // initialise AM2302 (includes 2 s warm-up)
  randomSeed(analogRead(A5));

  delay(500);   // Let serial settle after reset
  Serial.println(F("[BOOT] WebConsole_Serial_Communication_with_Raspberry_Pi v1.0"));
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
    Serial.print(F("[STATUS] streaming=")); Serial.println(isStreaming ? "ON" : "OFF");
    Serial.print(F("[STATUS] interval="));  Serial.print(streamInterval / 1000); Serial.println(F("s"));
    Serial.print(F("[STATUS] uptime="));    Serial.print(millis()/1000);  Serial.println(F("s"));
    Serial.print(F("[STATUS] fw=v1.0 port=9600"));
    Serial.println();
    printLedStatus();
    return;
  }

  if (cmd == "read") {
    updateSimulatedSensors();
    printAllSensors();
    printLedStatus();
    return;
  }
  if (cmd == "read temp") {
    Serial.print(F("[DATA] temp=")); Serial.println(readTemp(), 1);
    return;
  }
  if (cmd == "read hum") {
    Serial.print(F("[DATA] hum=")); Serial.println(readHumidity(), 1);
    return;
  }
  if (cmd == "read wind") {
    Serial.print(F("[DATA] wind_spd=")); Serial.print(readWindSpeed(), 1);
    Serial.print(F(" wind_dir="));       Serial.println(readWindDir());
    return;
  }
  if (cmd == "read lux") {
    Serial.print(F("[DATA] lux=")); Serial.println(readLux());
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
