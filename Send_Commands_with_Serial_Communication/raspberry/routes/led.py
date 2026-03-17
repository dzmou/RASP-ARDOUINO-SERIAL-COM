"""
This module defines the API routes for controlling the LEDs on the Arduino.
It provides endpoints to send commands via serial and to retrieve valid commands.
"""
from flask import Blueprint, jsonify, request
from serial_handler import send_command
from config import VALID_COMMANDS

# Create a Blueprint named 'led' to organize the LED-related routes
led_bp = Blueprint('led', __name__)

@led_bp.route('/led', methods=['POST']) # POST request to /led
def control_led():
    """
    Handle POST requests to /led to send a command to the Arduino.
    Expects a JSON payload with a 'command' field.
    """
    # Parse the incoming JSON payload
    data = request.get_json()

    # Validate that the payload exists and contains the required 'command' key
    if not data or "command" not in data:
        return jsonify({
            "status":        "error",
            "message":       "Missing 'command' field",
            "valid_commands": VALID_COMMANDS
        }), 400

    # Extract the command, converting to lowercase and stripping whitespace
    cmd = data["command"].lower().strip()

    # Verify that the requested command is in our list of valid commands
    if cmd not in VALID_COMMANDS:
        return jsonify({
            "status":        "error",
            "message":       f"Unknown command '{cmd}'",
            "valid_commands": VALID_COMMANDS
        }), 400

    # Send the validated command to the Arduino via the serial port
    response = send_command(cmd)

    # Check if the Arduino explicitly rejected the command
    if "bad command" in response.lower():
        return jsonify({"status": "error", "message": "Arduino rejected the command"}), 500

    # Return a success response with the original command and Arduino's reply
    return jsonify({
        "status":   "ok",
        "command":  cmd,
        "response": response
    }), 200


@led_bp.route('/led', methods=['GET'])
def led_commands():
    """
    Handle GET requests to /led.
    Returns the list of valid commands and usage instructions.
    """
    return jsonify({
        "status":         "ok",
        "valid_commands": VALID_COMMANDS,
        "usage": {
            "method": "POST",
            "body":   {"command": "green | blue | red | all | off"}
        }
    }), 200
