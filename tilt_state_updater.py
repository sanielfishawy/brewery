import logging
from threading import Thread
from state import State
from tilt_sniffer import TiltSniffer


class TiltStateUpdater(Thread):

    def run(self):
        tilt_sniffer = TiltSniffer.get_instance()
        state = State.get_instance()

        while(True):
            tilt_data = tilt_sniffer.get_tilt_data()
            for tilt in tilt_data:
                state.set_temp_with_color(tilt.get_color(), tilt.get_temp())
                state.set_specific_gravity_with_color(tilt.get_color(), tilt.get_specific_gravity())
                state.set_rssi_with_color(tilt.get_color(), tilt.get_rssi())

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s: %(threadName)s %(module)s %(message)s', level=logging.DEBUG)
    TiltStateUpdater().start()
                
