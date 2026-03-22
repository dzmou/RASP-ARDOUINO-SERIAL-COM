"""
csv_logger.py
Logs each streamed sensor packet to a rolling CSV file.
Files are stored in data/readings_YYYY-MM-DD.csv
"""

import os
import csv
import time
import logging
from datetime import datetime

log = logging.getLogger(__name__)

FIELDNAMES = ["timestamp", "streaming", "ts_ms",
              "temp", "hum", "wind_spd", "wind_dir", "lux",
              "led_red", "led_green", "led_blue"]


class CsvLogger:
    def __init__(self, config):
        self.csv_dir  = config.CSV_DIR
        self.max_rows = config.CSV_MAX_ROWS
        self._row_count = 0
        self._writer    = None
        self._file      = None
        os.makedirs(self.csv_dir, exist_ok=True)

    def log(self, data: dict):
        """Write one data packet to CSV."""
        try:
            self._ensure_file()
            leds = data.get("leds", {})
            self._writer.writerow({
                "timestamp":  datetime.utcnow().isoformat(),
                "streaming":  data.get("streaming", ""),
                "ts_ms":      data.get("ts", ""),
                "temp":       data.get("temp", ""),
                "hum":        data.get("hum", ""),
                "wind_spd":   data.get("wind_spd", ""),
                "wind_dir":   data.get("wind_dir", ""),
                "lux":        data.get("lux", ""),
                "led_red":    leds.get("red", ""),
                "led_green":  leds.get("green", ""),
                "led_blue":   leds.get("blue", ""),
            })
            self._file.flush()
            self._row_count += 1

            if self._row_count >= self.max_rows:
                self._rotate()

        except Exception as e:
            log.error(f"CSV write error: {e}")

    def list_files(self):
        """Return list of CSV filenames in data dir."""
        try:
            return sorted(
                [f for f in os.listdir(self.csv_dir) if f.endswith(".csv")],
                reverse=True
            )
        except Exception:
            return []

    def get_filepath(self, filename):
        return os.path.join(self.csv_dir, filename)

    # ── Internal ──────────────────────────────────────────────────
    def _ensure_file(self):
        today = datetime.utcnow().strftime("%Y-%m-%d")
        path  = os.path.join(self.csv_dir, f"readings_{today}.csv")

        if self._file is None or self._file.name != path:
            if self._file:
                self._file.close()
            exists = os.path.isfile(path)
            self._file   = open(path, "a", newline="")
            self._writer = csv.DictWriter(self._file, fieldnames=FIELDNAMES)
            if not exists:
                self._writer.writeheader()
            self._row_count = 0

    def _rotate(self):
        log.info("CSV max rows reached — rotating file")
        if self._file:
            self._file.close()
            self._file  = None
            self._writer = None
        self._row_count = 0
