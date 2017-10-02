from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode

app = Flask(__name__)
ask = Ask(app, "/webbrowser")


@app.route('/')
def homepage():
    return "Hi there, how you doin?"

@ask.launch
def start_skill():
    welcome_message="Hello there, are you expecting me to do something?"
    return question(welcome_message)

@ask.intent("YesIntent")
def yes_intent():
    return statement("Then, keep dreaming")

@ask.intent("NoIntent")
def no_intent():
    return statement("Then, why did you call me?... Goodbye")

if __name__ == '__main__':
    app.run(debug=True)
