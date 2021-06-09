# create the defined busses/interfces

class atBus():

    def __init__(self, bussettings):
        self.bussettings = bussettings
        self.i2c0 = None
        self.i2c1 = None
        self.onewire = None # not supported yet
    
        # create bus objects
        #try:
        for bus in self.bussettings:
            params = self.bussettings[bus]
            if params['type'] == 'i2c' and params['enabled']:
                print('Found i2c bus ',bus)
                if bus == 'i2c0':
                    self.i2c0 = self.create_i2c_bus(params['soft_i2c'], params['pin_scl'], params['pin_sda'])
                elif bus == 'i2c1':
                    self.i2c1 = self.create_i2c_bus(params['soft_i2c'], params['pin_scl'], params['pin_sda'])
                else:
                    print('Unknown i2c bus')
        #except:
         #   print('Fault reading bus in settings.py')

    def create_i2c_bus(self, soft=True, scl=18, sda=19):
        if soft:
            from machine import Pin, SoftI2C
            i2cbus = SoftI2C(scl=Pin(scl), sda=Pin(sda), freq=100000)
        else:
            from machine import Pin, I2C
            i2cbus = I2C(scl=Pin(scl), sda=Pin(sda), freq=100000)
        return i2cbus
