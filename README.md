# Instalation

1. Install Python dependencies
```
pip install selenium flask flask-ask requests
```
2. Place your Chrome/Firefox [driver](http://selenium-python.readthedocs.io/installation.html#drivers) inside project.


## Only Flask-Selenium
If you just want to test controlling a browser with RESTful GET calls. Execute `selenium_flask.py`. Once executed, you'll be able to start making the following requests:

  * `/init` - Start browser
  * `/status` - Give current browser status
  * `/newtab` - Open tab
  * `/switchtab?tab={No.Tab}` - Switch to X tab
  * `/open?site={site as: google.com, yourube.com}` - Open site in current tab


## ADOP DEMO (Flask-Ask-Selenium)
This is an static skill that will load ADOP's demo in selected driver, and basically Alexa will only switch between tabs.   

Execute with:
```
py adop_alexa.py --host [ADOPHost] --user [ADOPUsername] --password [ADOPUserPasword] --driver [chrome|firefox|firefox-msl]
```

For defining Alexa's Schema, copy content from `Alexa_Skill.md` in I'ts respective place.

Once everything is set up, you can call for the following Intents:
* Pipeline...
* ...

And if you accidentally close web driver, you can call for:
* **Initialize** - To re-load ADOP demo in a new driver _(aka. window)_.
