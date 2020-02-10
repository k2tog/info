import logging
import os
import sys
import flask
from flask import request, jsonify

"""
Takes /info and returns, in JSON format, the following: 
- application name, level and git_commit_sha
- environment (service_port and log_level)
"""

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['JSON_SORT_KEYS'] = False

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)


class BadDataError(Exception):
    """Custom exception class to be thrown when environment parameters are invalid."""
    def __init__(self, message, status=422, payload=None):
        self.message = message
        self.status = status
        self.payload = payload

@app.errorhandler(BadDataError)
def handle_invalid_input(error):
    """Catch BadDataError globally, serialize into JSON, and respond with 400."""
    payload = {}
    payload['status'] = error.status
    payload['message'] = error.message
    return jsonify(payload), 400

@app.route('/', methods=['GET'])
def invalid_route():
    """Prompt enduser to append /info"""
    logger.error('Error Occured - incomplete URL path')
    raise BadDataError('Try appending /info', 400)
    return jsonify(last_insert_id=1)



def get_input(source):
    """Read in environment parameters from os.environ."""
    logger.info('getting value for: %s', source)
    value = os.environ.get(source)
    logger.debug('value obtained: %s', value)
    if value is None:
        raise BadDataError("Environment Information is not currently available")
    return value

def check_log_level(level):
    """Validate log_level from environment variables is valid"""
    logger.info('validating logging level')
    logger.debug('logging level is: %s', level)
    if not (level.upper() in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")):
        raise BadDataError("log_level should be Debug, Info, Warning, Error or Critical")

def check_port_value(port):
    """Validate port from environment variables is within valid range of 0 thru 65535"""
    logger.info('validating port number')
    logger.debug('port provided is: %s', port)
    if not port.isdigit():
        raise BadDataError("port contains non-numeric value")
    if not '0' <= port <= '65535':
        raise BadDataError("port should be between 0 and 65535")



@app.route('/info', methods=['GET']) # to be absolutely true to the requirements
@app.route('/api/v1.0/info', methods=['GET'])
def app_info():
    """Returns information about a service"""
    logger.info('processing begins')
    try:
        service_name = get_input('SERVICE_NAME')
        version = get_input('VERSION')
        sha = get_input('GIT_COMMIT_SHA')
        level = get_input('LOG_LEVEL')
        port = get_input('SERVICE_PORT')
        check_log_level(level)
        check_port_value(port)

    except Exception as err:
        logger.error('Error Occured - returning data error')
        payload = {}
        payload['status'] = err.status
        payload['message'] = err.message
        return jsonify(payload), 422

    else:
        logger.info('Successful - returning result data')
        result = {}
        result['service_name'] = service_name
        result['version'] = version
        result['git_commit_sha'] = sha
        environment = {}
        environment['service_port'] = port
        environment['log_level'] = level
        result['environment'] = environment
        return jsonify(result), 200

    finally:
        logger.info('processing ends')

app.run(host='0.0.0.0')