from flask import Flask

app = Flask(__name__)
app.config.from_object('flask_app.config')

import flask_app.views