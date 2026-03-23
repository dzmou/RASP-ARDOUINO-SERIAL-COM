"""
app.py — Flask entry point
"""

from flask import Flask, request
from config import Config
from serial_handler_rasp import SerialHandler
from csv_logger_rasp import CsvLogger
from routes_rasp import register_routes
import socket
import fcntl
import struct

# ── App factory ───────────────────────────────────────────────
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # ── CORS headers (no flask_cors needed) ──
    @app.after_request
    def add_cors_headers(response):
        origin = request.headers.get('Origin', '*')
        allowed = Config.CORS_ORIGINS
        if allowed == ['*'] or origin in allowed:
            response.headers['Access-Control-Allow-Origin']  = origin
        response.headers['Access-Control-Allow-Methods']     = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers']     = 'Content-Type'
        return response

    # ── Shared services ──
    serial = SerialHandler(Config)
    csv    = CsvLogger(Config)

    # Wire CSV logging to incoming stream data
    serial.on_data(csv.log)

    # Start serial background thread
    serial.start()

    # Attach to app context
    app.serial = serial
    app.csv    = csv

    # Register blueprints
    register_routes(app)

    return app

def get_ip_address(ifname):
    """
    Directly queries the Linux kernel for the IP of a specific interface.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 0x8915 is the SIOCGIFADDR ioctl command to get the IP address
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,
            struct.pack('256s', ifname[:15].encode('utf-8'))
        )[20:24])
    except IOError:
        return "Not Found"

def display_ip_addresses():
    wlan_ip = get_ip_address('wlan0')
    eth_ip = get_ip_address('eth0')

    print("-" * 30)
    print(f"Wi-Fi (wlan0): {wlan_ip}")
    print(f"Ethernet (eth0): {eth_ip}")
    print("-" * 30)

if __name__ == "__main__":
    print("\n" + "="*40)
    print("RA-SERIAL WEB CONSOLE")
    print("="*40)
    display_ip_addresses()
    app = create_app()
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
    
