from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode

app = Flask(__name__)
ask = Ask(app, "/")


@app.route('/')
def homepage():
    return "Hi there, how you doin?"

@ask.launch
def start_skill():
    welcome_message="Hello there, would you like to open Chrome?"
    return question(welcome_message)

@ask.intent("YesIntent")
    return statement("Ok, opneing...")

@ask.intent("NoIntent")
    return statement("Then, why did you ask me to open Chrome?")

if __name__ == '__main__':
    app.run(debug=True)
