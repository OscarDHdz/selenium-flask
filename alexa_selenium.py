from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode
# Selenium dependencies
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from flask import jsonify

app = Flask(__name__)
ask = Ask(app, "/webbrowser")
driver = None
tabs = None

def validateDriver():
    global driver
    if ( driver is None ):
    	return {'status': False, 'message': 'Driver not initialized'}
    try:
    	title = driver.current_url
    except:
    	return {'status': False, 'message': 'Disconnected Driver'}
    return {'status': True, 'message': 'Driver initiated'}


@app.route('/')
def homepage():
    return "Hi there, how you doin?"

@ask.launch
def start_skill():
    welcome_message="Hello there, what you want me to do?"
    return question(welcome_message)

@ask.intent("Initialize")
def yes_intent():
    global driver
    global tabs
    status = validateDriver();
    if ( status['status'] is False ):
        driver = webdriver.Chrome()
        tabs = driver.window_handles
        return statement("Its Opening!")
    return statement("It's already open")

@ask.intent("Status")
def status_intent():
    status = validateDriver();
    message = status['message']
    return statement(message)

@ask.intent("NewTab")
def newtab_intent():
    global driver
    global tabs
    status = validateDriver();
    if ( status['status'] is False ):
        return statement(status['message'])
    driver.execute_script('''window.open("", "_blank");''');
    tabs = driver.window_handles
    return statement("Opening new tab...")

if __name__ == '__main__':
    app.run(debug=True)
