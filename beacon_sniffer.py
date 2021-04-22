import subprocess
from threading import Thread
import time

class BeaconSniffer:

    _instance = None

    def __init__(self):
        if self.__class__._instance:
            raise "BeaconSniffer is a singleton. Use get_instance()"

        LeScan().start()
    
    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    
    def get_beacon_data(self):
        try:
            proc = subprocess.Popen(['hcidump', '-R', 'hci'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            proc.communicate(timeout=2)
        except subprocess.TimeoutExpired:
            proc.kill()
            data, errs = proc.communicate()
        data = data.decode().lower().split('\n>')[2:]
        data_nw = []
        for d in data:
            data_nw.append(''.join(d.split()))
        return data_nw


class LeScan(Thread):
    def run(self):
        subprocess.run(['hcitool', 'lescan', '--duplicates'], stdout=subprocess.DEVNULL)
        print('hcitool lescan started')