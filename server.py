import logging
import argparse
from flask import Flask, request, json
from werkzeug.serving import is_running_from_reloader
from state import State
from tilt_state_updater import TiltStateUpdater
from thermostat import Thermostat

HOST = '0.0.0.0'

class RequestPaths:
    BREW_PATH = '/brew'
    SAVE_STATE_PATH = BREW_PATH + '/save_state'
    STATE_KEY = 'state'

arg_parser = argparse.ArgumentParser(description='Start fence server.')
arg_parser.add_argument('-p', '--port',
                        default=80,
                        type=int,
                        help='Port to use for server.',
                        metavar='port',)

PORT = arg_parser.parse_known_args()[0].port

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')


state_manager = State.get_instance()
TiltStateUpdater().start()
thermostat = Thermostat.get_instance()

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route(RequestPaths.BREW_PATH)
def brew():
    return state_manager.get_state_obj()

@app.route(RequestPaths.SAVE_STATE_PATH, methods=['POST'])
def save_state():
    state = getObjectFromRequest(request)[RequestPaths.STATE_KEY]
    logging.debug(f'server got pos: {state}')
    state_manager.set_state(state)
    state_manager.save_state()
    return state_manager.get_state_obj()

def getObjectFromRequest(request):
    return json.loads(request.data.decode())

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(threadName)s %(modeule)s %(message)s',)
    app.run(host= HOST, debug=True, port=PORT)