from flask import Flask, redirect, render_template, request
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

@app.route("/answer", methods=["post"])
def route_answer():
    responses.append(request.form["answer"])
    if len(responses) < len(satisfaction_survey.questions):
        return redirect(f"/questions/{len(responses)}")
    else:
        return redirect("/thankyou")

@app.route("/thankyou")
def route_thankyou():
    return render_template("thankyou.html")
