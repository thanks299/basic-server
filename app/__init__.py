from flask import Flask
from .routes import hello

app = Flask(__name__)

app.register_blueprint(hello)

