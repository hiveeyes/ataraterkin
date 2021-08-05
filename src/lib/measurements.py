# measurements

class atMeasurements():

    def __init__(self) -> None:
        self.IntTemperature = 0.0

    async def getDS3231temperature(self, DS3231):
        self.IntTemperature = DS3231.getTemperature()
        print('Internal Temperature: {}°C'.format(self.IntTemperature))
        return ['temperature.inside', self.IntTemperature]