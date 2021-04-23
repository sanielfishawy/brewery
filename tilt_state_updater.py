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
                wort = state.get_wort_by_tilt_color(tilt.color)
                if not wort:
                    logging.warning(f'Got and update for {tilt.color} tilt. But there isnt a {tilt.color} in wort.')
                else:
                    wort.temp = tilt.get_temp()
                    wort.specific_gravity = tilt.get_specific_gravity()
                    wort.rssi = tilt.get_rssi()
                    state.print_state()

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s: %(threadName)s %(module)s %(message)s', level=logging.DEBUG)
    TiltStateUpdater().start()
                
