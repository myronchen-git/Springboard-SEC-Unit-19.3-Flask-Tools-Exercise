from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension

from surveys import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)

# ==================================================

responses = []

@app.route("/")
def route_root():
    return render_template("root.html", survey=satisfaction_survey)
