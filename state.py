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

    def __init__(self):
        if self.__class__._instance:
            raise 'State is a singleton. Use get_instance()'
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


    

