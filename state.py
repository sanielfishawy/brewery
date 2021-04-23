import yaml
import logging

class State:
    _instance = None
    NUM_WORTS = 4

    RED = 'red'
    GREEN = 'green'
    BLACK = 'black'
    PURPLE = 'purple'
    ORANGE = 'orange'
    BLUE = 'blue'
    YELLOW = 'yellow'
    PINK = 'pink'

    TILT_COLORS = [BLACK, PURPLE, ORANGE, BLUE]

    STATE_FILE = 'state.yml'

    def __init__(self):
        if self.__class__._instance:
            raise 'State is a singleton. Use get_instance()'

        if not self.restore_state():
            self.init_state()
    
    def init_state(self):
        self.worts = []
        for id in range(self.__class__.NUM_WORTS):
            self.worts.append(Wort(id=id, tilt_color=self.__class__.TILT_COLORS[id]))
    
    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance
        
    def get_wort_by_id(self, id):
        result = None
        for wort in self.worts:
            if wort.id == id:
                result = wort
        return result
    
    def get_wort_by_tilt_color(self, color):
        result = None
        for wort in self.worts:
            if wort.tilt_color == color:
                result = wort
        return result

    def print_state(self):
        for wort in self.worts:
            print(f'WORT {wort.id}')
            print(wort.get_obj())
    
    def restore_state(self):
        try:
            with open(self.__class__.STATE_FILE) as file:
                state = yaml.load(file, Loader=yaml.FullLoader)
        except FileNotFoundError:
            logging.info('State file not found')
            return False

        self.worts = []
        for wort in state:
            self.worts.append(Wort().set_with_obj(wort))

        return True

    def save_state(self):
        with open(self.__class__.STATE_FILE, 'w') as file:
            yaml.dump(self.get_obj(), file)

    def get_obj(self):
        result = []
        for wort in self.worts:
            result.append(wort.get_obj())
        return result

class Wort:
    ID = 'id'
    NAME = 'name'
    TILT_COLOR = 'tilt_color'
    TEMP = 'temp'
    SET_TEMP = 'set_temp'
    HYSTERESIS = 'hysteresis'
    SPECIFIC_GRAVITY = 'specific_gravity'
    HEATER_SHELBY_ADDR = 'heater_shelby_addr'
    COOLER_SHELBY_ADDR = 'cooler_shelby_addr'
    RSSI = 'rssi'

    def __init__(
        self,
        id=None,
        name=None,
        tilt_color=None,
        temp=None,
        set_temp=None,
        hysteresis=None,
        specific_gravity=None,
        heater_shelby_addr=None,
        cooler_shelby_addr=None,
        rssi=None,
       ):

       self.id = id
       self.name = name
       self.tilt_color = tilt_color
       self.temp= temp
       self.set_temp = set_temp
       self.hysteresis = hysteresis
       self.specific_gravity = specific_gravity
       self.heater_shelby_addr = heater_shelby_addr
       self.cooler_shelby_addr = cooler_shelby_addr
       self.rssi = rssi
    
    def get_obj(self):
        return {
            self.__class__.ID: self.id,
            self.__class__.NAME: self.name,
            self.__class__.TILT_COLOR: self.tilt_color,
            self.__class__.TEMP: self.temp,
            self.__class__.SET_TEMP: self.set_temp,
            self.__class__.HYSTERESIS: self.hysteresis,
            self.__class__.SPECIFIC_GRAVITY: self.specific_gravity,
            self.__class__.HEATER_SHELBY_ADDR: self.heater_shelby_addr,
            self.__class__.COOLER_SHELBY_ADDR: self.cooler_shelby_addr,
            self.__class__.RSSI: self.rssi,
        }
    
    def set_with_obj(self, obj):
        if self.__class__.ID in obj:
            self.id = obj[self.__class__.ID]
        if self.__class__.NAME in obj:
            self.name = obj[self.__class__.NAME]
        if self.__class__.TILT_COLOR in obj:
            self.tilt_color = obj[self.__class__.TILT_COLOR]
        if self.__class__.TEMP in obj:
            self.temp = obj[self.__class__.TEMP]
        if self.__class__.SET_TEMP in obj:
            self.set_temp = obj[self.__class__.SET_TEMP]
        if self.__class__.HYSTERESIS in obj:
            self.hysteresis = obj[self.__class__.HYSTERESIS]
        if self.__class__.SPECIFIC_GRAVITY in obj:
            self.specific_gravity = obj[self.__class__.SPECIFIC_GRAVITY]
        if self.HEATER_SHELBY_ADDR in obj:
            self.heater_shelby_addr = obj[self.__class__.HEATER_SHELBY_ADDR]
        if self.COOLER_SHELBY_ADDR in obj:
            self.cooler_shelby_addr = obj[self.__class__.COOLER_SHELBY_ADDR]
        if self.__class__.RSSI in obj:
            self.rssi = obj[self.__class__.RSSI]
        return self

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s: %(threadName)s %(module)s %(message)s', level=logging.DEBUG)
    State.get_instance()
    State.get_instance().print_state()

