import argparse
from flask import Flask, jsonify, make_response, send_from_directory
from flask_cors import CORS
from routes import request_api
import os
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)
### end swagger specific ###


app.register_blueprint(request_api.get_blueprint())


@app.errorhandler(400)
def handle400Error(error):
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@app.errorhandler(401)
def handle401Error(error):
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@app.errorhandler(404)
def handle404Error(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(500)
def handle500Error(error):
    return make_response(jsonify({'error': 'Server error'}), 500)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Seans-Python-Flask-REST-Boilerplate")

    parser.add_argument('--debug', action='store_true',
                        help="Use flask debug/dev mode with file change reloading")
    args = parser.parse_args()

    port = int(os.environ.get('PORT', 5000))

    if args.debug:
        print("Running in debug mode")
        cors = CORS(app)
        app.run(host='0.0.0.0', port=port, debug=True)
    else:
        app.run(host='0.0.0.0', port=port, debug=False)
