"""
serial_handler.py
Background thread that manages the serial connection to Arduino.
Parses incoming JSON (default/hybrid) and raw lines (interactive).
"""

import serial
import threading
import time
import json
import logging
from collections import deque

log = logging.getLogger(__name__)


class SerialHandler:
    def __init__(self, config):
        self.port      = config.SERIAL_PORT
        self.baud      = config.SERIAL_BAUD
        self.timeout   = config.SERIAL_TIMEOUT
        self.reset_delay = config.SERIAL_RESET_DELAY

        self._ser      = None
        self._thread   = None
        self._lock     = threading.Lock()
        self._running  = False

        # Latest parsed sensor snapshot
        self.latest    = {}
        # Raw log ring-buffer (last 200 lines)
        self.rx_log    = deque(maxlen=200)
        # Callbacks: list of callables(data_dict)
        self._on_data  = []

    # ── Lifecycle ────────────────────────────────────────────────
    def start(self):
        self._running = True
        self._thread  = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        log.info(f"SerialHandler started on {self.port} @ {self.baud}")

    def stop(self):
        self._running = False
        if self._ser and self._ser.is_open:
            self._ser.close()

    # ── Send ─────────────────────────────────────────────────────
    def send(self, cmd: str) -> bool:
        with self._lock:
            if self._ser and self._ser.is_open:
                try:
                    self._ser.write((cmd.strip() + "\n").encode())
                    log.debug(f"TX: {cmd}")
                    return True
                except serial.SerialException as e:
                    log.error(f"Send error: {e}")
        return False

    @property
    def connected(self):
        return self._ser is not None and self._ser.is_open

    # ── Register callback ─────────────────────────────────────────
    def on_data(self, fn):
        self._on_data.append(fn)

    # ── Background thread ─────────────────────────────────────────
    def _run(self):
        while self._running:
            try:
                self._connect()
                self._read_loop()
            except Exception as e:
                log.warning(f"Serial error: {e} — reconnecting in 3s")
                time.sleep(3)

    def _connect(self):
        if self._ser and self._ser.is_open:
            return
        log.info(f"Opening {self.port}…")
        self._ser = serial.Serial(self.port, self.baud, timeout=self.timeout)
        time.sleep(self.reset_delay)   # wait for Arduino reset
        log.info("Serial connected")

    def _read_loop(self):
        """
        Continuously read from serial. 
        Groups textual lines into single multi-line log entries but 
        processes JSON sensor data immediately.
        """
        buffer = []
        while self._running and self._ser.is_open:
            try:
                # Read a line (blocks for up to self.timeout seconds)
                raw = self._ser.readline().decode("utf-8", errors="replace").strip()
                
                if not raw:
                    # Timeout reached: if we have a text buffer, commit it now
                    if buffer:
                        self._commit_buffer(buffer)
                        buffer = []
                    continue

                # Is it a JSON packet? (usually sensor data)
                if raw.startswith("{"):
                    # Flush any pending text before processing JSON
                    if buffer:
                        self._commit_buffer(buffer)
                        buffer = []
                    self._process_json(raw)
                else:
                    # It's a regular text line
                    log.debug(f"RX (text): {raw}")
                    buffer.append(raw)
                    
                    # If we see a block-end marker, flush immediately for responsiveness
                    if "[END" in raw or "Unknown" in raw or "[PONG]" in raw:
                        self._commit_buffer(buffer)
                        buffer = []

            except serial.SerialException as e:
                log.error(f"Read error: {e}")
                break

    def _commit_buffer(self, buffer):
        """Joins lines and adds to the log as a single entry."""
        if not buffer:
            return
        combined = "\n".join(buffer)
        self.rx_log.appendleft({"ts": time.time(), "line": combined})
        log.debug(f"RX (committed block):\n{combined}")

    def _process_json(self, raw):
        """Parses JSON data packets and triggers callbacks."""
        try:
            data = json.loads(raw)
            self.latest = data
            for fn in self._on_data:
                try:
                    fn(data)
                except Exception as e:
                    log.error(f"Callback error: {e}")
        except json.JSONDecodeError:
            # If not valid JSON after all, treat as text
            self._commit_buffer([raw])
