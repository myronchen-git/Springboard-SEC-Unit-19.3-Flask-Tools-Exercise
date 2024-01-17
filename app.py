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

@app.route("/questions/<int:ques_num>")
def route_questions(ques_num):
    return render_template(
        "question.html", question=satisfaction_survey.questions[ques_num])