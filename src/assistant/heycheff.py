from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)


@app.route('/run-assistant', methods=['POST'])
def run_assistant():
    print("assistant running...")
