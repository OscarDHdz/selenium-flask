# Flask Dependencies
from flask import Flask, jsonify, request
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode
# Selenium dependencies
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# Arguments
import argparse
import sys

# Argument parser ----------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--host", help="ADOP public IP")
args = parser.parse_args()
if args.host:
    print ("ADOP host:", args.host)
else:
    print ("Missing [--host] flag:", args.host)
    sys.exit(0)

sys.stdout.flush()

# Web Wervice ---------------------------------------------
app = Flask(__name__)
ask = Ask(app, "/platform")

# Global Variables
driver = None
tabs = None
ADOP_HOST = args.host

pages = {
    'adop': {'page': 'http://{}/'.format(ADOP_HOST), 'tab': ''},
    'jenkins': {'page': 'https://{}/jenkins'.format(ADOP_HOST), 'tab': ''},
    'pipeline': {'page': 'http://{}/jenkins/job/MDC/job/DEMO/view/Java_Reference_Application/?auto_refresh=true'.format(ADOP_HOST), 'tab': ''},
    'gerrit': {'page': 'http://{}/gerrit/#/admin/projects/MDC/DEMO/demo-base-spring-petclinic'.format(ADOP_HOST), 'tab': ''},
    'projectdemo': {'page': 'http://{}'.format(ADOP_HOST), 'tab': ''},
    'deploy': {'page': 'http://mdc_demo_ci.{}.nip.io/petclinic/ '.format(ADOP_HOST), 'tab': ''},
    'prodA': {'page': 'http://mdc_demo_proda.{}.nip.io/petclinic/ '.format(ADOP_HOST), 'tab': ''},
    'prodB': {'page': 'http://mdc_demo_prodb.{}.nip.io/petclinic/ '.format(ADOP_HOST), 'tab': ''},
    'cucumber': {'page': 'http://{}/jenkins/job/MDC/job/DEMO/job/Reference_Application_Regression_Tests/2/cucumber-html-reports/feature-overview.html'.format(ADOP_HOST), 'tab': ''},
    'gattling': {'page': 'http://{}/jenkins/job/MDC/job/DEMO/job/Reference_Application_Performance_Tests/gatling/'.format(ADOP_HOST), 'tab': ''},
    'sonarq': {'page': 'http://{}/sonar/dashboard/index/1 '.format(ADOP_HOST), 'tab': ''}
}

# Initialize
def open_adop():
    global driver
    global tabs
    driver = webdriver.Chrome()
    # Open pages
    for index, (key, value) in enumerate(pages.items()):
        if ( index is 0 ):
            driver.get(value['page'])
            value['tab'] = driver.window_handles[index]
        else:
            pageScript = 'window.open("{}", "_blank");';
            driver.execute_script(pageScript.format(value['page']))
            value['tab'] = driver.window_handles[index]
    tabs = driver.window_handles


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

@app.route('/pages', methods=['GET'])
def get_openbrowser():
    return jsonify(pages)

@app.route('/switchtab', methods=['GET'])
def get_switchpage():
    tab = request.args.get('tab')
    driver.switch_to_window(tab)
    return jsonify(pages)

@ask.launch
def start_skill():
    welcome_message="Hello there, what you want me to do?"
    return question(welcome_message)

# @ask.intent("Initialize")
# def init_intent():
#     status = validateDriver();
#     if ( status['status'] is False ):
#         #open_adop()
#         return statement("Its Opening!")
#     return statement("It's already open")


@ask.intent("Status")
def status_intent():
    status = validateDriver();
    message = status['message']
    return statement(message)

@ask.intent("Platform")
def platform_intent():
    status = validateDriver();
    if ( status['status'] is True ):
        driver.switch_to_window(pages['adop']['tab'])
        return statement(status['message'])

@ask.intent("Pipeline")
def pipeline_intent():
    status = validateDriver();
    if ( status['status'] is True ):
        driver.switch_to_window(pages['pipeline']['tab'])
    return statement(status['message'])

@ask.intent("Jenkins")
def jenkins_intent():
    status = validateDriver();
    if ( status['status'] is True ):
        driver.switch_to_window(pages['jenkins']['tab'])
    return statement(status['message'])

@ask.intent("Gerrit")
def gerrit_intent():
    status = validateDriver();
    if ( status['status'] is True ):
        driver.switch_to_window(pages['gerrit']['tab'])
    return statement(status['message'])



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
    open_adop()
    app.run(debug=False)
