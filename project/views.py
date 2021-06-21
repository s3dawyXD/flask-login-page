from . import app
from flask import render_template, jsonify


@app.route('/')
def index():
    return render_template("login.html")

