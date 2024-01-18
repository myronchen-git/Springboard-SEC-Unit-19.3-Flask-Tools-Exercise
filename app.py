from flask import Flask, flash, redirect, render_template, request, session
from flask_debugtoolbar import DebugToolbarExtension

from surveys import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)

# ==================================================

@app.route("/")
def route_root():
    """Display the start of the survey."""

    return render_template("index.html", survey=satisfaction_survey)

@app.route("/questions", methods=["post"])
def route_questions():
    """Set up environment and redirect to first question."""

    session["responses"] = []
    return redirect("/questions/0")

@app.route("/questions/<int:ques_num>")
def route_question_num(ques_num):
    """Display a question."""

    if ques_num != len(session["responses"]):
        flash("Invalid question.  Redirecting to the correct URL.", "status-message--error")
        return redirect(__next_page__())
    else:
        return render_template(
            "question.html",
            survey_title=satisfaction_survey.title,
            question_number=ques_num,
            question=satisfaction_survey.questions[ques_num])

@app.route("/answer", methods=["post"])
def route_answer():
    """Handle an answer."""

    responses = session["responses"]
    responses.append(request.form["answer"])
    session["responses"] = responses

    return redirect(__next_page__())

@app.route("/thankyou")
def route_thankyou():
    """Display a survey completion page."""

    return render_template("thankyou.html", survey_title=satisfaction_survey.title)

# ==================================================

def __next_page__():
    """Helper function to find the next page to go to."""

    responses_length = len(session["responses"])

    if responses_length < len(satisfaction_survey.questions):
        return f"/questions/{responses_length}"
    else:
        return "/thankyou"
