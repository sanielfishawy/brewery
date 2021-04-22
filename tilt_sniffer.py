from beacon_sniffer import BeaconSniffer
from state import State

class TiltSniffer:
    _instance = None

    TILT_UUIDS = {
        'a495bb10c5b14b44b5121370f02d74de': State.RED,
        'a495bb20c5b14b44b5121370f02d74de': State.GREEN,
        'a495bb30c5b14b44b5121370f02d74de': State.BLACK,
        'a495bb40c5b14b44b5121370f02d74de': State.PURPLE,
        'a495bb50c5b14b44b5121370f02d74de': State.ORANGE,
        'a495bb60c5b14b44b5121370f02d74de': State.BLUE,
        'a495bb70c5b14b44b5121370f02d74de': State.YELLOW,
        'a495bb80c5b14b44b5121370f02d74de': State.PINK,
    }

    def __init__(self):
        if self.__class__._instance:
            raise "TiltSniffer is a singleton. Use get_instance()"

        self.beacon_sniffer = BeaconSniffer.get_instance()

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance
    
    def get_tilt_data(self):
        data = self.beacon_sniffer.get_beacon_data()
        data = self.get_data_matching_tilt_uuids(data)
        return data
        
    def get_data_matching_tilt_uuids(self, data):
        result = []
        for d in data: 
            for uuid in self.__class__.TILT_UUIDS.keys():
                if uuid in d:
                    result.append(TiltData(self.__class__.TILT_UUIDS[uuid], d))
        return result

class TiltData:
    def __init__(self, color, raw_data):
        self.color = color
        self.raw_data = raw_data
    
    def get_color(self):
        return self.color
    
    def get_raw_data(self):
        return self.raw_data
    
    def get_major(self):
        return int(self.raw_data[-12:-8], 16)
    
    def get_minor(self):
        return int(self.raw_data[-8:-4], 16)
    
    def get_rssi(self):
        return - (256 - int(self.raw_data[-2:], 16))

if __name__ == '__main__':
    data = TiltSniffer.get_instance().get_tilt_data()
    print('data')
    for d in data:
        print(d.get_raw_data())
        print(d.get_rssi())
        print(d.get_minor())
        print(d.get_major())
    pass
