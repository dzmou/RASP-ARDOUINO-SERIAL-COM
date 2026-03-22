# Arduino LED Controller

This folder contains the Arduino sketch for the Raspberry Pi ↔ Arduino LED Controller project. The Arduino listens for string commands over the serial port (USB) to control three separate LEDs.

## Wiring

The default sketch uses the following pins:

| Pin | LED Color | Note |
|-----|-----------|------|
| 8   | Blue      | Output Pin |
| 9   | Green     | Output Pin |
| 10  | Red       | Output Pin |
| GND | GND       | Connect to LED common cathode/ground |

## Serial Configuration

- **Baud Rate**: 9600
- **Line Ending**: Newline (`\n`)

## Commands

Send these string values ending with a newline character (`\n`) via the Serial Monitor or the Raspberry Pi script:

| Command | Action |
|---------|--------|
| `green` | Turns ON the green LED (pin 9) and turns OFF others |
| `blue`  | Turns ON the blue LED (pin 8) and turns OFF others |
| `red`   | Turns ON the red LED (pin 10) and turns OFF others |
| `all`   | Turns ON all three LEDs |
| `off`   | Turns OFF all three LEDs |

*Note: Any unknown command will be met with a `bad command` response over the serial line.*
