import logging
import yaml
import requests
from state import Wort, State
import time

class Shelly:

    URL = 'https://shelly-22-eu.shelly.cloud/device/relay/control'
    AUTH_FILE = 'shelly_auth.yml'

    ON = 'on'
    OFF = 'off'

    @classmethod
    def get_auth(cls):
        with open(cls.AUTH_FILE) as file:
                auth = yaml.load(file, Loader=yaml.FullLoader)
        return auth

    @classmethod
    def heat_on_off(cls, wort: Wort, on_off):
        time.sleep(1.1)
        resp = cls.turn(wort.heater_shelly_addr, on_off)
        logging.info(f'shelly heat {on_off} {resp}')

    @classmethod
    def cool_on_off(cls, wort: Wort, on_off):
        time.sleep(1.1)
        resp = cls.turn(wort.cooler_shelly_addr, on_off)
        logging.info(f'shelly cool {on_off} {resp}')
    
    @classmethod
    def chiller_on_off(cls, on_off):
        time.sleep(1.1)
        resp = cls.turn(State.get_instance().get_chiller_shelly_addr(), on_off)
        logging.info(f'shelly chiller {on_off} {resp}')

    @classmethod
    def turn(cls, id, on_off):
        data = {
            'auth_key': cls.get_auth(),
            'channel': 0,
            'id': id,
            'turn': on_off,

        }
        logging.debug(data)
        return requests.post(cls.URL, data)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(threadName)s %(module)s %(message)s',)
    Shelly.chiller_on_off(Shelly.ON)
    Shelly.heat_on_off(State.get_instance().get_worts()[0], Shelly.ON)
    Shelly.cool_on_off(State.get_instance().get_worts()[0], Shelly.ON)