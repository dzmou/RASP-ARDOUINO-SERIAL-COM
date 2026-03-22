from flask import Flask, render_template
from serial_handler import connect, disconnect
from routes import status_bp, led_bp, other_bp
from config import HOST, PORT, DEBUG

app = Flask(__name__)

app.register_blueprint(status_bp) # register the status blueprint.
app.register_blueprint(led_bp) # register the led commands blueprint.
app.register_blueprint(other_bp) # register the other commands blueprint.

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