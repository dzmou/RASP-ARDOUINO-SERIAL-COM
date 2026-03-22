#!/bin/bash
# run.sh — Start the Flask API server

# Exit immediately if a command exits with a non-zero status.
set -e

# Change to the directory containing the script.
cd "$(dirname "$0")/flask_app" 

# Install dependencies.
#echo "Installing dependencies…"
#pip install -r ../requirements.txt --quiet

# Start the WebConsole API server.
echo "Starting WebConsole server on port 5000…"
python app.py
