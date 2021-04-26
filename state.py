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

    STATE_FILE = 'state.yml'

    WORTS_KEY = 'worts'
    CHILLER_SHELLY_ADDR_KEY = 'chiller_shelly_addr'

    def __init__(self):
        if self.__class__._instance:
            raise 'State is a singleton. Use get_instance()'

        if not self.restore_state():
            self.init_state()
        
        self.callbacks = []
    
    def add_callback(self, callback):
        self.callbacks.append(callback)
    
    def notify_callbacks(self):
        for cb in self. callbacks:
            cb()

    def init_state(self):
        self.chiller_shelly_addr = ''

        self.worts = []
        for id in range(self.__class__.NUM_WORTS):
            self.worts.append(Wort(id=id))
    
    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance
        
    def set_state(self, state):
        self.worts = []
        for wort in state[self.__class__.WORTS_KEY]:
            self.worts.append(Wort().set_with_obj(wort))
        
        self.chiller_shelly_addr = state[self.__class__.CHILLER_SHELLY_ADDR_KEY]

    def get_worts(self):
        return self.worts

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
    
    def set_temp_with_color(self, color, temp):
        wort = self.get_wort_by_tilt_color(color)
        if not wort:
            logging.warning(f'Got and update for {color} tilt. But there isnt a {color} tilt setup.')
        elif wort.temp != temp:
            wort.temp = temp
            self.save_state()

    def set_specific_gravity_with_color(self, color, specific_gravity):
        wort = self.get_wort_by_tilt_color(color)
        if not wort:
            logging.warning(f'Got and update for {color} tilt. But there isnt a {color} tilt setup.')
        elif wort.specific_gravity != specific_gravity:
            wort.specific_gravity = specific_gravity
            self.save_state()

    def set_rssi_with_color(self, color, rssi):
        wort = self.get_wort_by_tilt_color(color)
        if not wort:
            logging.warning(f'Got and update for {color} tilt. But there isnt a {color} tilt setup.')
        elif wort.rssi != rssi:
            wort.rssi = rssi
            self.save_state()

    def set_status_with_color(self, color, status):
        wort = self.get_wort_by_tilt_color(color)
        if not wort:
            logging.warning(f'Got and update for {color} tilt. But there isnt a {color} tilt setup.')
        elif wort.status != status:
            wort.status = status
            self.save_state()

    def print_state(self):
        print(f'chller_sh_addr: {self.chiller_shelly_addr}')
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

        self.set_state(state)
        return True

    def save_state(self):
        with open(self.__class__.STATE_FILE, 'w') as file:
            yaml.dump(self.get_state_obj(), file)
        self.notify_callbacks()

    def get_worts_obj(self):
        result = []
        for wort in self.worts:
            result.append(wort.get_obj())
        return result
    
    def get_chiller_shelly_addr(self):
        return self.chiller_shelly_addr
    
    def get_state_obj(self):
        return (
            {
                self.__class__.CHILLER_SHELLY_ADDR_KEY: self.chiller_shelly_addr,
                self.__class__.WORTS_KEY: self.get_worts_obj()
            }
        )


class Wort:
    ID = 'id'
    NAME = 'name'
    TILT_COLOR = 'tilt_color'
    TEMP = 'temp'
    SET_TEMP = 'set_temp'
    HYSTERESIS = 'hysteresis'
    STATUS = 'status'
    SPECIFIC_GRAVITY = 'specific_gravity'
    HEATER_SHELLY_ADDR = 'heater_shelly_addr'
    COOLER_SHELLY_ADDR = 'cooler_shelly_addr'
    RSSI = 'rssi'

    STATUS_HEAT = 'heat'
    STATUS_COOL = 'cool'
    STATUS_OFF = 'off'

    def __init__(
        self,
        id=None,
        name=None,
        tilt_color=None,
        temp=None,
        set_temp=None,
        hysteresis=None,
        specific_gravity=None,
        heater_shelly_addr=None,
        cooler_shelly_addr=None,
        rssi=None,
       ):

       self.id = id
       self.name = name
       self.tilt_color = tilt_color
       self.temp= float(temp) if temp else temp
       self.set_temp = float(set_temp) if set_temp else temp
       self.hysteresis = float(hysteresis) if hysteresis else hysteresis
       self.status = self.__class__.STATUS_OFF
       self.specific_gravity = float(specific_gravity) if specific_gravity else specific_gravity
       self.heater_shelly_addr = heater_shelly_addr
       self.cooler_shelly_addr = cooler_shelly_addr
       self.rssi = int(rssi) if rssi else rssi
    
    def get_obj(self):
        return {
            self.__class__.ID: self.id,
            self.__class__.NAME: self.name,
            self.__class__.TILT_COLOR: self.tilt_color,
            self.__class__.TEMP: self.temp,
            self.__class__.SET_TEMP: self.set_temp,
            self.__class__.HYSTERESIS: self.hysteresis,
            self.__class__.STATUS: self.status,
            self.__class__.SPECIFIC_GRAVITY: self.specific_gravity,
            self.__class__.HEATER_SHELLY_ADDR: self.heater_shelly_addr,
            self.__class__.COOLER_SHELLY_ADDR: self.cooler_shelly_addr,
            self.__class__.RSSI: self.rssi,
        }
    
    def get_float(self, obj):
        return float(obj) if obj else obj
        
    def get_int(self, obj):
        return int(obj) if obj else obj
        
    def set_with_obj(self, obj):
        if self.__class__.ID in obj:
            self.id = obj[self.__class__.ID]
        if self.__class__.NAME in obj:
            self.name = obj[self.__class__.NAME]
        if self.__class__.TILT_COLOR in obj:
            self.tilt_color = obj[self.__class__.TILT_COLOR]
        if self.__class__.TEMP in obj:
            self.temp = self.get_float(obj[self.__class__.TEMP])
        if self.__class__.SET_TEMP in obj:
            self.set_temp = self.get_float(obj[self.__class__.SET_TEMP])
        if self.__class__.HYSTERESIS in obj:
            self.hysteresis = self.get_float(obj[self.__class__.HYSTERESIS])
        if self.__class__.STATUS in obj:
            self.status = obj[self.__class__.STATUS]
        if self.__class__.SPECIFIC_GRAVITY in obj:
            self.specific_gravity = self.get_float(obj[self.__class__.SPECIFIC_GRAVITY])
        if self.HEATER_SHELLY_ADDR in obj:
            self.heater_shelly_addr = obj[self.__class__.HEATER_SHELLY_ADDR]
        if self.COOLER_SHELLY_ADDR in obj:
            self.cooler_shelly_addr = obj[self.__class__.COOLER_SHELLY_ADDR]
        if self.__class__.RSSI in obj:
            self.rssi = self.get_int(obj[self.__class__.RSSI])
        return self

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s: %(threadName)s %(module)s %(message)s', level=logging.DEBUG)
    State.get_instance()
    State.get_instance().print_state()
    State.get_instance().save_state()

