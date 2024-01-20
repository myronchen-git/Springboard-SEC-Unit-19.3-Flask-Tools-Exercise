from flask import Flask, flash, redirect, render_template, request, session
from flask_debugtoolbar import DebugToolbarExtension

from surveys import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

debug = DebugToolbarExtension(app)

CURRENT_SURVEY_CODE_KEY = "current_survey_code"
RESPONSES_KEY = "responses"

# ==================================================


@app.route("/")
def route_root():
    """Display all the surveys and allows a user to select one."""

    return render_template("index.html", survey_codes=surveys.keys())


@app.route("/survey/<survey_code>", methods=["post"])
def survey(survey_code):
    """Display the start of the survey."""

    survey = surveys[survey_code]

    begin_button_text = "Start"
    responses_length = len(session.get(RESPONSES_KEY, {}).get(survey_code, []))
    if 0 < responses_length and responses_length < len(survey.questions):
        begin_button_text = "Continue"
    elif responses_length >= len(survey.questions):
        begin_button_text = "Results"

    return render_template(
        "survey-start.html",
        survey={
            "code": survey_code,
            "title": survey.title,
            "instructions": survey.instructions,
        },
        begin_button_text=begin_button_text,
    )


@app.route("/survey/<survey_code>/questions", methods=["post"])
def route_questions(survey_code):
    """Set up environment and redirect to first question."""

    session[CURRENT_SURVEY_CODE_KEY] = survey_code

    responses = session.get(RESPONSES_KEY, {})
    if not responses.get(survey_code):
        responses[survey_code] = []
        session[RESPONSES_KEY] = responses

    session.permanent = True

    return redirect(__next_unvisited_page__())


@app.route("/survey/<survey_code>/questions/<int:ques_num>")
def route_question_num(survey_code, ques_num):
    """Display a question."""

    responses = session.get(RESPONSES_KEY, {}).get(survey_code)

    if survey_code != session.get(CURRENT_SURVEY_CODE_KEY, "") or responses is None:
        flash(
            "Wrong page location.",
            "alert-warning status-message--error",
        )
        return redirect("/")

    elif ques_num < 0 or ques_num > len(responses):
        flash(
            "Invalid question.  Redirecting to the correct URL.",
            "alert-warning status-message--error",
        )
        return redirect(__next_unvisited_page__())

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

    ques_num = int(request.form.get("ques_num"))
    response = {
        "answer": request.form.get("answer", ""),
        "comment": request.form.get("comment", ""),
    }

    responses = session[RESPONSES_KEY]

    if ques_num == len(responses[survey_code]):
        responses[survey_code].append(response)
    else:
        responses[survey_code][ques_num] = response

    session[RESPONSES_KEY] = responses

    if request.form.get("go") == "next":
        if ques_num < len(surveys[survey_code].questions) - 1:
            return redirect(f"/survey/{survey_code}/questions/{ques_num + 1}")
        else:
            return redirect(f"/survey/{survey_code}/thankyou")

    elif request.form.get("go") == "previous":
        return redirect(f"/survey/{survey_code}/questions/{ques_num - 1}")


@app.route("/survey/<survey_code>/thankyou")
def route_thankyou(survey_code):
    """Display a survey completion page."""

    survey = surveys[survey_code]

    return render_template(
        "thankyou.html",
        survey_title=survey.title,
        questions=survey.questions,
        responses=session.get(RESPONSES_KEY, {}).get(survey_code, []),
    )


# ==================================================


def __next_unvisited_page__():
    """Helper function to find the next page to go to."""

    survey_code = session[CURRENT_SURVEY_CODE_KEY]
    survey = surveys[survey_code]
    responses_length = len(session[RESPONSES_KEY][survey_code])

    if responses_length < len(survey.questions):
        return f"/survey/{survey_code}/questions/{responses_length}"
    else:
        return f"/survey/{survey_code}/thankyou"
