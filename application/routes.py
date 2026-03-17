from app  import app
from .model import db 

from flask import render_template

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")