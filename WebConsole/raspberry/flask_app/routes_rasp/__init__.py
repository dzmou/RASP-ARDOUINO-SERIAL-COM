from routes_rasp.api import api_bp
from routes_rasp.web import web_bp

def register_routes(app):
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(web_bp)
