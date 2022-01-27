from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "never-tell!"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

responses = []


@app.get("/")
def homepage():

    return render_template(
        "survey_start.html", title=survey.title, instructions=survey.instructions
    )


@app.get("/begin")
def start_survey():
    pass
