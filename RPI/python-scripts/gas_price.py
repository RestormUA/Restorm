import appdaemon.plugins.hass.hassapi as hass
import datetime

class gas_price(hass.Hass):
    def initialize(self):
        runtime = datetime.time(0, 0, 0)
        self.run_minutely(self.getGasValue, runtime)

    def getGasValue(self, kwargs):
        entityID = "input_text.value"
        self.gasInputEntity = self.get_entity(entityID)
        gasPrice = self.gasInputEntity.get_state
        
        self.gasEntity = self.get_entity("sensor.gasprice")
        self.gasEntity.set_state(state=gasPrice)