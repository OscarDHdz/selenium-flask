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
On It...
