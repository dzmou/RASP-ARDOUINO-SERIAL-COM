from flask import Flask, render_template
from serial_handler import connect, disconnect
from routes import led_bp, command_bp
from config import HOST, PORT, DEBUG

app = Flask(__name__)

app.register_blueprint(led_bp) # register the led blueprint, it's a group of routes for led.
app.register_blueprint(command_bp) # register the command blueprint, it's a group of routes for commands.

@app.route('/') 
def index():
    return render_template('index.html') # render the index.html template

if __name__ == '__main__':
    try:
        # Attempt to establish hardware connection
        if connect(): 
            print("Successfully connected to Arduino.")
        else:
            print("Warning: Arduino not found. Running in offline mode.")
            
        app.run(host=HOST, port=PORT, debug=DEBUG)
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
        disconnect()