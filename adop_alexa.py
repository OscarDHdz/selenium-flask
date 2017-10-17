# Flask Dependencies
from flask import Flask, jsonify, request
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import random
# Selenium dependencies
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

# Arguments
import argparse
import sys

# Argument parser ----------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--host", help="ADOP public IP")
parser.add_argument("--user", help="ADOP username")
parser.add_argument("--password", help="ADOP password")
parser.add_argument("--driver", help="Specify chrome/firefox/firefox-esr")
args = parser.parse_args()
#Validations
if args.host:
    print ("ADOP host:", args.host)
else:
    print ("Missing [--host] flag:", args.host)
    sys.exit(0)
if args.user:
    print ("ADOP user:", args.user)
else:
    print ("Missing [--user] flag:", args.user)
    sys.exit(0)
if args.password:
    print ("ADOP password:", args.password)
else:
    print ("Missing [--password] flag:", args.password)
    sys.exit(0)
if args.driver:
    print ("Using driver:", args.driver)
else:
    print ("Missing [--driver chrome|firerfox|firefox-esr] flag:", args.driver)
    sys.exit(0)


sys.stdout.flush()

# Web Wervice ---------------------------------------------
app = Flask(__name__)
ask = Ask(app, "/platform")

# Global Variables
driver = None
tabs = None
ADOP_HOST = args.host
ADOP_USER = args.user
ADOP_PASS = args.password
SELENIUM_DRIVER = args.driver
BINARY = FirefoxBinary("/usr/lib/firefox-esr/firefox-esr")


# Pages that will be opened at Browser
pages = {
    'adop': {'page': 'http://{}:{}@{}/'.format(ADOP_USER, ADOP_PASS, ADOP_HOST), 'tab': ''},
    'jenkins': {'page': 'http://{}:{}@{}/jenkins'.format(ADOP_USER, ADOP_PASS, ADOP_HOST), 'tab': ''},
    'pipeline': {'page': 'http://{}:{}@{}/jenkins/job/MDC/job/DEMO/view/Java_Reference_Application/?auto_refresh=true'.format(ADOP_USER, ADOP_PASS, ADOP_HOST), 'tab': ''},
    'gerrit': {'page': 'http://{}:{}@{}/gerrit/#/admin/projects/MDC/DEMO/demo-base-spring-petclinic'.format(ADOP_USER, ADOP_PASS, ADOP_HOST), 'tab': ''},
    'deploy': {'page': 'http://{}:{}@mdc_demo_ci.{}.nip.io/petclinic/ '.format(ADOP_USER, ADOP_PASS, ADOP_HOST), 'tab': ''},
    'prodA': {'page': 'http://{}:{}@mdc_demo_proda.{}.nip.io/petclinic/ '.format(ADOP_USER, ADOP_PASS, ADOP_HOST), 'tab': ''},
    'prodB': {'page': 'http://{}:{}@mdc_demo_prodb.{}.nip.io/petclinic/ '.format(ADOP_USER, ADOP_PASS, ADOP_HOST), 'tab': ''},
    'cucumber': {'page': 'http://{}:{}@{}/jenkins/job/MDC/job/DEMO/job/Reference_Application_Regression_Tests/1/cucumber-html-reports/feature-overview.html'.format(ADOP_USER, ADOP_PASS, ADOP_HOST), 'tab': ''},
    'gattling': {'page': 'http://{}:{}@{}/jenkins/job/MDC/job/DEMO/job/Reference_Application_Performance_Tests/gatling/'.format(ADOP_USER, ADOP_PASS, ADOP_HOST), 'tab': ''},
    'sonarq': {'page': 'http://{}:{}@{}/sonar/dashboard/index/1 '.format(ADOP_USER, ADOP_PASS, ADOP_HOST), 'tab': ''}
}

# Set Driver function
def set_driver(selected_driver):
    global driver
    if ( selected_driver == "chrome" ):
        driver = webdriver.Chrome()
        return True;
    elif ( selected_driver == "firefox"):
        driver = webdriver.Firefox()
        return True;
    elif ( selected_driver == "firefox-esr"):
        driver = webdriver.Firefox(firefox_binary=BINARY)
        return True;
    else:
        return False

# Return a random Success Message
def random_ok_message():
    messages = [
        "Got It!",
        "It's already on screen",
        "There you go",
        "Done",
        "All right"
    ]
    return random.choice(messages)

# Initialize
def open_adop():
    global driver
    global tabs

    # Set web driver
    if ( set_driver(SELENIUM_DRIVER) is False ):
        print ("Invalid WebDriver. Please use [chrome|firefox|firefox-esr].")
        sys.exit(0)

    # Open Brwoser with all tabs and bind 'tabs' to each 'page'
    for index, (key, value) in enumerate(pages.items()):
        time.sleep(1)
        if ( index is 0 ):
            driver.get(value['page'])
            value['tab'] = driver.window_handles[index]
            actions = ActionChains(driver)
            actions.send_keys('hola')
            actions.perform()
        else:
            pageScript = 'window.open("{}", "_blank");';
            driver.execute_script(pageScript.format(value['page']))
            value['tab'] = driver.window_handles[index]
    tabs = driver.window_handles

# Validate current statos function. Avoid missing driver conection lost
def validateDriver():
    global driver
    if ( driver is None ):
    	return {'status': False, 'message': 'Driver not initialized'}
    try:
    	title = driver.current_url
    except:
    	return {'status': False, 'message': 'Disconnected Driver'}
    return {'status': True, 'message': 'Driver initiated'}


### Endpoints available at your browser ----------------------------------------
@app.route('/')
def homepage():
    return jsonify(pages)

@app.route('/status', methods=['GET'])
def get_openbrowser():
    status = validateDriver();
    return jsonify(status)

### Intets available for Alexa. Alexa MUST aknowledge each of these Intents it
###   Her Schema

# This intent is displayed if you only call for teh aleksa skill
@ask.launch
def start_skill():
    welcome_message="Hello there, right now you should be able to see ADOP demo. If not, ask me to Initialize demo"
    return statement(welcome_message)

# Initialize will re-open DEMO. Use onl if closed original browser
@ask.intent("Initialize")
def init_intent():
    status = validateDriver();
    if ( status['status'] is False ):
        open_adop()
        return statement(random_ok_message())
    return statement("It's already open")


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
        return statement(random_ok_message())
    return statement(status['message'])

@ask.intent("Pipeline")
def pipeline_intent():
    status = validateDriver();
    if ( status['status'] is True ):
        driver.switch_to_window(pages['pipeline']['tab'])
        return statement(random_ok_message())
    return statement(status['message'])

@ask.intent("Jenkins")
def jenkins_intent():
    status = validateDriver();
    if ( status['status'] is True ):
        driver.switch_to_window(pages['jenkins']['tab'])
        return statement(random_ok_message())
    return statement(status['message'])

@ask.intent("Gerrit")
def gerrit_intent():
    status = validateDriver();
    if ( status['status'] is True ):
        driver.switch_to_window(pages['gerrit']['tab'])
        return statement(random_ok_message())
    return statement(status['message'])

@ask.intent("Cucumber")
def gerrit_intent():
    status = validateDriver();
    if ( status['status'] is True ):
        driver.switch_to_window(pages['cucumber']['tab'])
        return statement(random_ok_message())
    return statement(status['message'])

@ask.intent("Gattling")
def gerrit_intent():
    status = validateDriver();
    if ( status['status'] is True ):
        driver.switch_to_window(pages['gattling']['tab'])
        return statement(random_ok_message())
    return statement(status['message'])

@ask.intent("Sonarqube")
def gerrit_intent():
    status = validateDriver();
    if ( status['status'] is True ):
        driver.switch_to_window(pages['sonarq']['tab'])
        return statement(random_ok_message())
    return statement(status['message'])

@ask.intent("ProdA")
def gerrit_intent():
    status = validateDriver();
    if ( status['status'] is True ):
        driver.switch_to_window(pages['prodA']['tab'])
        return statement(random_ok_message())
    return statement(status['message'])

@ask.intent("ProdB")
def gerrit_intent():
    status = validateDriver();
    if ( status['status'] is True ):
        driver.switch_to_window(pages['prodB']['tab'])
        return statement(random_ok_message())
    return statement(status['message'])

@ask.intent("Deploy")
def gerrit_intent():
    status = validateDriver();
    if ( status['status'] is True ):
        driver.switch_to_window(pages['deploy']['tab'])
        return statement(random_ok_message())
    return statement(status['message'])

if __name__ == '__main__':
    open_adop()
    app.run(debug=False)
