from flask import Flask, flash, redirect, render_template, request, session
from flask_debugtoolbar import DebugToolbarExtension

from surveys import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

debug = DebugToolbarExtension(app)

# ==================================================


@app.route("/")
def route_root():
    """Display all the surveys and allows a user to select one."""

    return render_template("index.html", survey_codes=surveys.keys())


@app.route("/survey/<survey_code>", methods=["post"])
def survey(survey_code):
    """Display the start of the survey."""

    survey = surveys[survey_code]

    return render_template(
        "survey-start.html",
        survey={
            "code": survey_code,
            "title": survey.title,
            "instructions": survey.instructions,
        },
    )


@app.route("/survey/<survey_code>/questions", methods=["post"])
def route_questions(survey_code):
    """Set up environment and redirect to first question."""

    session["current_survey_code"] = survey_code

    responses = session.get("responses", {})
    responses[survey_code] = []
    session["responses"] = responses

    return redirect(f"/survey/{survey_code}/questions/0")


@app.route("/survey/<survey_code>/questions/<int:ques_num>")
def route_question_num(survey_code, ques_num):
    """Display a question."""

    if survey_code != session["current_survey_code"]:
        flash(
            "Invalid survey.  Please complete the current survey first.",
            "status-message--error",
        )
        return redirect(__next_page__())

    elif ques_num != len(session["responses"][survey_code]):
        flash(
            "Invalid question.  Redirecting to the correct URL.",
            "status-message--error",
        )
        return redirect(__next_page__())

    else:
        survey = surveys[survey_code]

        return render_template(
            "question.html",
            survey={
                "code": survey_code,
                "title": survey.title,
            },
            question={
                "number": ques_num,
                "question_instance": survey.questions[ques_num],
            },
        )


@app.route("/survey/<survey_code>/answer", methods=["post"])
def route_answer(survey_code):
    """Handle an answer."""

    responses = session["responses"]
    responses[survey_code].append(
        {
            "answer": request.form.get("answer", ""),
            "comment": request.form.get("comment", ""),
        }
    )
    session["responses"] = responses

    return redirect(__next_page__())


@app.route("/survey/<survey_code>/thankyou")
def route_thankyou(survey_code):
    """Display a survey completion page."""

    survey = surveys[survey_code]

    return render_template(
        "thankyou.html",
        survey_title=survey.title,
        questions=survey.questions,
        responses=session["responses"][survey_code],
    )


# ==================================================


def __next_page__():
    """Helper function to find the next page to go to."""

    survey_code = session["current_survey_code"]
    survey = surveys[survey_code]
    responses_length = len(session["responses"][survey_code])

    if responses_length < len(survey.questions):
        return f"/survey/{survey_code}/questions/{responses_length}"
    else:
        return f"/survey/{survey_code}/thankyou"
