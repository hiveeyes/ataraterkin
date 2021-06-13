'''Reading and setting the time'''
from machine import RTC

class atClock():
    
    def __init__(self, timesettings, busses):
        self.intRTC = RTC()
        self.extRTC = None

        # setting the time
        try:
            params = timesettings['RTC']
            if params['enabled']:
                from DS3231tokei import DS3231
                if params['bus'] == 'i2c0':
                    self.extRTC = DS3231(busses.i2c0)
                elif params['bus'] == 'i2c1':
                    self.extRTC = DS3231(busses.i2c1)
                else:
                    raise Exception
            (year,month,day,dotw,hour,minute,second) = self.extRTC.getDateTime() # get the current time
            print('Date: {}.{}.{}, Time: {}h {}m {}s'.format(day,month,year,hour,minute,second))
            if year < 2001:
                year = 2001 # sanity check, as of mpy 1.12 year must be >= 2001
            print('Setting internal RTC')
            self.intRTC.init((year,month,day,dotw,hour,minute,second,0)) # set time
        except:
            print('Fault reading RTC in settings.py')