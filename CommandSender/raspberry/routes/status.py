from flask import Blueprint, jsonify
from serial_handler import is_connected

status_bp = Blueprint('status', __name__)

@status_bp.route('/status', methods=['GET'])
def status():
    return jsonify({
        "status": "ok",
        "serial": is_connected()
    }), 200
