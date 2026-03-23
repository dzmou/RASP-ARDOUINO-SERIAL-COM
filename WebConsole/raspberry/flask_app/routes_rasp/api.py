"""
routes/api.py — REST API
"""

import os
from flask import Blueprint, jsonify, request, current_app, send_from_directory

api_bp = Blueprint("api", __name__)

def serial():
    return current_app.serial

def csv_log():
    return current_app.csv


# ── Status ────────────────────────────────────────────────────
@api_bp.route("/status", methods=["GET"])
def status():
    return jsonify({
        "connected": serial().connected,
        "latest":    serial().latest,
        "port":      current_app.config["SERIAL_PORT"],
        "baud":      current_app.config["SERIAL_BAUD"],
    })


# ── Latest sensor snapshot ────────────────────────────────────
@api_bp.route("/data", methods=["GET"])
def get_data():
    return jsonify(serial().latest or {})


# ── Raw RX log ────────────────────────────────────────────────
@api_bp.route("/log", methods=["GET"])
def get_log():
    n = min(int(request.args.get("n", 100)), 200)
    return jsonify(list(serial().rx_log)[:n])


# ── Send command ──────────────────────────────────────────────
@api_bp.route("/send", methods=["POST"])
def send_cmd():
    body = request.get_json(force=True, silent=True) or {}
    cmd  = body.get("command", "").strip()
    if not cmd:
        return jsonify({"ok": False, "error": "No command provided"}), 400
    ok = serial().send(cmd)
    return jsonify({"ok": ok, "command": cmd})


# ── LED shortcut ──────────────────────────────────────────────
@api_bp.route("/led", methods=["POST"])
def led():
    body  = request.get_json(force=True, silent=True) or {}
    color = body.get("color", "").lower()
    state = body.get("state", "").lower()   # "on" | "off"
    if color not in ("red", "green", "blue", "all"):
        return jsonify({"ok": False, "error": "Invalid color"}), 400
    if state not in ("on", "off"):
        return jsonify({"ok": False, "error": "State must be on or off"}), 400
    cmd = f"led {color} {state}"# f: means formatted string, eg. led red on
    ok  = serial().send(cmd)
    return jsonify({"ok": ok, "command": cmd})


# -- Stream toggle -------------------------------------------
@api_bp.route("/stream", methods=["POST"])
def set_stream():
    body  = request.get_json(force=True, silent=True) or {}
    state = body.get("state", "").lower()
    if state not in ("on", "off"):
        return jsonify({"ok": False, "error": "State must be 'on' or 'off'"}), 400
    ok = serial().send(f"stream {state}")
    return jsonify({"ok": ok, "streaming": state == "on"})


# -- Stream interval (seconds) --------------------------------
@api_bp.route("/interval", methods=["POST"])
def set_interval():
    body = request.get_json(force=True, silent=True) or {}
    s    = body.get("s")
    try:
        s = int(s)
        assert 1 <= s <= 86400
    except Exception:
        return jsonify({"ok": False, "error": "s must be 1-86400 (seconds)"}), 400
    ok = serial().send(f"interval {s}")
    return jsonify({"ok": ok, "interval_s": s})


# ── CSV: list files ───────────────────────────────────────────
@api_bp.route("/csv", methods=["GET"])
def csv_list():
    return jsonify({"files": csv_log().list_files()})


# ── CSV: download file ────────────────────────────────────────
@api_bp.route("/csv/<filename>", methods=["GET"])
def csv_download(filename):
    # Safety: only allow our generated filenames
    if not filename.startswith("readings_") or not filename.endswith(".csv"):
        return jsonify({"error": "Invalid filename"}), 400
    directory = os.path.abspath(csv_log().csv_dir)
    return send_from_directory(directory, filename, as_attachment=True)
