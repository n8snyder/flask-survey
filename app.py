from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import personality_quiz as survey
from surveys import Answer

app = Flask(__name__)
app.config["SECRET_KEY"] = "never-tell!"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)


@app.get("/")
def homepage():
    """Survey homepage with start survey button"""

    return render_template(
        "survey_start.html", title=survey.title, instructions=survey.instructions
    )


@app.post("/begin")
def start_survey():
    """Redirect to first question"""

    session["responses"] = []
    session["question_number"] = 0
    return redirect("/questions/0")


@app.get("/questions/<int:question_number>")
def get_question(question_number):
    """Displays form for the given question or redirects to thanks page"""

    if session["question_number"] != question_number:
        flash(f"Question number {question_number} is out of order")
        return redirect(f"/questions/{session['question_number']}")

    elif question_number == len(survey.questions):
        return redirect("/thanks")

    else:
        question = survey.questions[question_number]
        return render_template(
            "question.html",
            question = question.question,
            question_choices = question.choices,
            allow_text = question.allow_text,
        )


@app.get("/thanks")
def get_thanks_page():
    """Displays thanks page"""

    return render_template("completion.html")


@app.post("/answer")
def answer():
    """Record answer and redirect to next question"""

    form_data = request.form
    answer = form_data.get("answer")
    text_response = form_data.get("response", "")
    session["responses"] += [Answer(answer, text_response)]
    session["question_number"] += 1

    return redirect(f"/questions/{session['question_number']}")
