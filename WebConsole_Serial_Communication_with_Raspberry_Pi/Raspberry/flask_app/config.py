import os

class Config:
    # ── Serial ────────────────────────────────────────────────
    SERIAL_PORT     = os.environ.get("SERIAL_PORT", "/dev/ttyACM0")
    SERIAL_BAUD     = int(os.environ.get("SERIAL_BAUD", 9600))
    SERIAL_TIMEOUT  = 2          # seconds
    SERIAL_RESET_DELAY = 2       # seconds after open before sending

    # ── Flask ─────────────────────────────────────────────────
    SECRET_KEY      = os.environ.get("SECRET_KEY", "rasp-arduino-dev-key")
    DEBUG           = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
    HOST            = os.environ.get("FLASK_HOST", "0.0.0.0")
    PORT            = int(os.environ.get("FLASK_PORT", 5000))

    # ── CSV Logger ────────────────────────────────────────────
    CSV_DIR         = os.environ.get("CSV_DIR", "data")
    CSV_MAX_ROWS    = int(os.environ.get("CSV_MAX_ROWS", 10000))  # rotate after N rows

    # ── CORS ──────────────────────────────────────────────────
    CORS_ORIGINS    = ["*"]
