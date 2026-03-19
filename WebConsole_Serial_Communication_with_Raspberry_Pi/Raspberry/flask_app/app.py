"""
app.py — Flask entry point
"""

from flask import Flask, request
from config import Config
from serial_handler_rasp import SerialHandler
from csv_logger import CsvLogger
from routes import register_routes

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


if __name__ == "__main__":
    app = create_app()
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
