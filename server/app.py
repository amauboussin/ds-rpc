from flask import Flask, jsonify, request, send_from_directory
import logging
from logging.handlers import RotatingFileHandler
import os

from ds_rpc_server import clean_old_scripts, deserialize_call

app = Flask(__name__)
LOG_FILE = 'logs.log'
clean_old_scripts()
app.debug = True

demo_dir = os.path.join(os.getcwd(), 'js-client')


@app.route('/', methods=['POST'])
def rpc():
    data = request.get_data()
    return jsonify(deserialize_call(data))


@app.route('/demo', methods=['GET'])
def demo_html():
    return send_from_directory(demo_dir, 'demo.html')


@app.route('/js_bindings.js', methods=['GET'])
def js_bindings():
    demo_dir = os.path.join(os.getcwd(), 'js-client')
    return send_from_directory(demo_dir, 'ds_rpc.js')


@app.errorhandler(500)
def internal_error(exception):
    app.logger.error(exception)
    return '500 Error: %s' % (exception), 500

if __name__ == '__main__':
    handler = RotatingFileHandler(LOG_FILE, maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    app.run()
