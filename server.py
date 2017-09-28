from flask import Flask
from flask import jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/openbrowser', methods=['GET'])
def get_openbrowser():
    return jsonify({'action': True})
	
if __name__ == '__main__':
    app.run(debug=True)