from app  import app
from .model import db 



@app.route("/home")
def home():
    return "welcome home"