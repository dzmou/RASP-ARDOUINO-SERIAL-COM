from flask import Blueprint, render_template

web_bp = Blueprint("web", __name__)

@web_bp.route("/", methods=["GET"])
def index():
    # index.html is in the './templates' folder, 
    return render_template("index.html")
