from flask import Blueprint, jsonify
from serial_handler import is_connected

command_bp = Blueprint('command', __name__)

@command_bp.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "serial": is_connected()
    }), 200
