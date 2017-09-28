from flask import Flask
from flask import jsonify
from flask import request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys


app = Flask(__name__)
driver = None

def validateDriver():
	global driver
	if ( driver is None ):
		return {'status': False, 'message': 'Driver not initialized'}
	try:
		title = driver.current_url
	except:
		return {'status': False, 'message': 'Disconnected Driver'}
	return {'status': True, 'message': 'Driver initiated'}


@app.route('/status', methods=['GET'])
def get_status():
	return jsonify(validateDriver())

@app.route('/init', methods=['GET'])
def get_init():
	global driver
	status = validateDriver();
	if ( status['status'] is False ):
		driver = webdriver.Chrome()
		tabs = driver.window_handles
		return jsonify({'status': True, 'message': 'Initialized'})
	return jsonify({'status': True, 'message': 'Already Initiated'})
	

@app.route('/open', methods=['GET'])
def get_open():
	status = validateDriver()
	site = request.args.get('site')
	if ( site is None ):
		return jsonify({'status': False, 'message': 'Missing site parameter'}) 
	if ( status['status'] is True ):
		driver.get('http://' + site)
		return jsonify({'status': True})
	return jsonify(status)
	
@app.route('/close', methods=['GET'])
def get_close():
	global driver
	status = validateDriver()
	if ( status['status'] is True ):
		driver.close();
		driver = None;
		return jsonify({'status': True})
	return jsonify(status)

@app.route('/')
def index():
    return "Hello, World!"
	
	
if __name__ == '__main__':
    app.run(debug=True)