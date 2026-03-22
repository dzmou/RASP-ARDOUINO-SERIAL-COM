"""
This module defines the API routes for controlling other things.
It provides endpoints to send commands via serial.
"""
from flask import Blueprint, jsonify, request
from serial_handler import send_command

# Create a Blueprint named 'other' to organize the other-related routes
other_bp = Blueprint('other', __name__)

@other_bp.route('/other', methods=['POST'])
def other_commands():
    """
    Handle POST requests to /other to send a command to the Arduino. 
    but the is not mentioned in the valid commands list.
    Expects a JSON payload with a 'command' field.
    """
    
    # Parse the incoming JSON payload
    # eg. {"command": "shutdown"}
    data = request.get_json()

    # Validate that the payload exists and contains the required 'command' field
    
    if not data or "command" not in data:
        return jsonify({
            "status":        "error",
            "message":       "Missing 'command' field",
            "valid_format": "'command': 'your_command'"
        }), 400

    # Extract the command, converting to lowercase and stripping whitespace
    cmd = data["command"].lower().strip()

    # Send the validated command to the Arduino via the serial port
    response = send_command(cmd)

    # Check if the Arduino explicitly rejected the command
    if "bad command" in response.lower():
        return jsonify({"status": "error", "message": "Arduino rejected the command"}), 500

    # Return a success response with the original command and Arduino's reply
    return jsonify({
        "status":   "ok",
        "command":  cmd,
        "response": response if response else "No response from Arduino"
    }), 200
