from flask import Flask, flash, redirect, render_template, request
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
    if ques_num != len(responses):
        flash("Invalid question.  Redirecting to the correct URL.", "status-message--error")
        return redirect(__next_page__())
    else:
        return render_template(
            "question.html", question=satisfaction_survey.questions[ques_num])

@app.route("/answer", methods=["post"])
def route_answer():
    responses.append(request.form["answer"])
    return redirect(__next_page__())

@app.route("/thankyou")
def route_thankyou():
    return render_template("thankyou.html")

# ==================================================

def __next_page__():
    if len(responses) < len(satisfaction_survey.questions):
        return f"/questions/{len(responses)}"
    else:
        return "/thankyou"
