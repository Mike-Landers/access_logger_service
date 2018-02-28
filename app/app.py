import os
import logging
from flask import Flask
from flask import jsonify
from flask import request
from db_utility import DatabaseUtility


ROOT_DIR = str(os.path.abspath(os.getcwd()))
format_string = '%(asctime)s %(name)s %(levelname)s %(message)s'

# set default logging (to console)
logging.basicConfig(level=logging.DEBUG, format=format_string)
log = logging.getLogger()
log.info('Starting Access Logger Service')
log.setLevel(logging.DEBUG)

app = Flask(__name__)


@app.route('/status', methods=['GET'])
def get_status():
    return 'Access Logger Service is up and running'


@app.route('/api/v1/hello_world', methods=['GET'])
def get_hello_world():
    db_util.start_hello_world_timer(request.remote_addr)
    return jsonify(message='hello world')


@app.route('/api/v1/hello/<string:name>', methods=['GET'])
def get_hello_name(name):
    db_util.start_hello_name_timer(request.remote_addr, name)
    return jsonify(message='hello ' + name)


@app.route('/api/v1/logs/hello', methods=['GET'])
def get_hello_logs():
    results = db_util.get_hello_name_logs()
    return jsonify(status='ok', data=results)


@app.route('/api/v1/logs/hello_world', methods=['GET'])
def get_hello_world_logs():
    results = db_util.get_hello_world_logs()
    return jsonify(status='ok', data=results)


@app.route('/api/v1/logs', methods=['GET'])
def get_all_logs():
    results = db_util.get_all_logs()
    return jsonify(status='ok', data=results)


db_util = DatabaseUtility()
db_util.initialize_db(app)


if __name__ == "__main__":
    app.run(host='localhost', debug=True, port=8081)
