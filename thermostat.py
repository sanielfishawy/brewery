import logging
from state import State
from state import Wort
from shelly import Shelly

class Thermostat:

    _instance = None

    def __init__(self) -> None:
        if self.__class__._instance:
            raise 'Thermostat is a singleton. Use get_instance()'

        self.state = State.get_instance()
        self.state.add_callback(self.on_state_change)

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def on_state_change(self): 
        worts = self.state.get_worts()
        for wort in worts:
            self.set_heat_cool(wort)

    def set_heat_cool(self, wort):
        if not self.can_control(wort):
            self.log_warning(wort)
            return
        
        if self.wort_requires_heat(wort):
            self.heat(wort)
        elif self.wort_requires_cool(wort):
            self.cool(wort)
        else:
            self.off(wort)
    
    def wort_requires_heat(self, wort):
        return wort.temp < wort.set_temp - wort.hysteresis / 2
    
    def wort_requires_cool(self, wort):
        return wort.temp > wort.set_temp + wort.hysteresis / 2

    def log_warning(self, wort):
        logging.warning(f'Trying to control Wort[{wort.id}] which is not fully setup.')

    def heat(self, wort):
        logging.debug('Heating')
        self.state.set_status_with_color(wort.tilt_color, Wort.STATUS_HEAT)
        Shelly.heat_on_off(wort, Shelly.ON)
        Shelly.cool_on_off(wort, Shelly.OFF)
        self.set_chiller()

    def cool(self, wort):
        logging.debug('Cooling')
        self.state.set_status_with_color(wort.tilt_color, Wort.STATUS_COOL)
        Shelly.heat_on_off(wort, Shelly.OFF)
        Shelly.cool_on_off(wort, Shelly.ON)
        self.set_chiller()

    def off(self, wort):
        logging.debug('Off (heat/cool)')
        self.state.set_status_with_color(wort.tilt_color, Wort.STATUS_OFF)
        Shelly.heat_on_off(wort, Shelly.OFF)
        Shelly.cool_on_off(wort, Shelly.OFF)
        self.set_chiller()
    
    def set_chiller(self):
        chiller = Shelly.OFF
        for wort in self.state.worts:
            if wort.status == Wort.STATUS_COOL:
                chiller = Shelly.ON
        Shelly.chiller_on_off(chiller)

    def can_control(self, wort):
        if not wort:
            return False

        need = [wort.set_temp, wort.temp, wort.hysteresis]
        for num in need:
            if not self.is_number(num):
                return False
        
        return True

    def is_number(self, n):
        return type(n) is int or type(n) is float

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(threadName)s %(module)s %(message)s',)
    thermostat = Thermostat()
    state = State.get_instance()
    wort = state.get_wort_by_tilt_color('blue')
    temp = wort.temp
    hyst = wort.hysteresis
    wort.set_temp = 64.6
    state.save_state()
    print(wort.status)