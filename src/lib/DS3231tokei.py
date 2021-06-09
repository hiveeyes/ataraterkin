# DS3231 library for Micropython
#
# Derived from DS3213 libraries by Sebastian Maerker & ww.micropython.org.cn
# License: MIT
# 
# only 24h mode is supported
#


DS3231_I2C_ADDR   = (0x68)
DS3231_REG_SEC    = (0x00)
DS3231_REG_MIN    = (0x01)
DS3231_REG_HOUR   = (0x02)
DS3231_REG_WEEKDAY= (0x03)
DS3231_REG_DAY    = (0x04)
DS3231_REG_MONTH  = (0x05)
DS3231_REG_YEAR   = (0x06)
DS3231_REG_A1SEC  = (0x07)
DS3231_REG_A1MIN  = (0x08)
DS3231_REG_A1HOUR = (0x09)
DS3231_REG_A1DAY  = (0x0A)
DS3231_REG_A2MIN  = (0x0B)
DS3231_REG_A2HOUR = (0x0C)
DS3231_REG_A2DAY  = (0x0D)
DS3231_REG_CTRL   = (0x0E)
DS3231_REG_STA    = (0x0F)
DS3231_REG_AGOFF  = (0x10)
DS3231_REG_TEMP   = (0x11)

# Alarm 1
A1_EVERY_SECOND                    = (1)   # every second
A1_ON_SECOND                       = (2)   # when second match
A1_A2_ON_MINUTE_SECOND                = (3)   # when minute & second match
A1_ON_HOUR_MINUTE_SECOND           = (4)   # when hour, minute & second match
A1_ON_DAY_HOUR_MINUTE_SECOND       = (5)   # when day of the month, hour, minute & second match
A1_ON_WEEKDAY_HOUR_MINUTE_SECOND   = (6)   # when day of the week, hour and minute match
# Alarm 2 (all Alarm 2 alarms are triggered when second = 0)
A2_EVERY_MINUTE                    = (11)  # when second = 0
A2_ON_MINUTE                       = (12)  # when minute match
A2_ON_HOUR_MINUTE                  = (13)  # when hour and minute match
A2_ON_DAY_HOUR_MINUTE              = (14)  # when day of the month, hour and minute match
A2_ON_WEEKDAY_HOUR_MINUTE          = (15)  # when day of the week, hour and minute match

class DS3231:
    
    def __init__(self, i2c):

        self.i2c = i2c
        # sanitize control register, set INTCN to 1, rest to 0, don't touch A1IE & A2IE
        REG_CTRL = self.getReg(DS3231_REG_CTRL)
        REG_CTRL = REG_CTRL & 0b00000111    # zero unwanted bits
        REG_CTRL = REG_CTRL | 0b00000100    # set INTCN

        self.setReg(DS3231_REG_CTRL,REG_CTRL)
        # set to 24h mode - 12h not supported
        A109 = self.getReg(DS3231_REG_A1HOUR)
        A109 = A109 & 0b10111111    # set bit 6 to 0
        self.setReg(DS3231_REG_A1HOUR,A109)
        A20C = self.getReg(DS3231_REG_A2HOUR)
        A20C = A20C & 0b10111111    # set bit 6 to 0
        self.setReg(DS3231_REG_A2HOUR,A20C)
        # check if time is valid
        STA_CTRL = self.getReg(DS3231_REG_STA)
        self.TimeIsValid = not (STA_CTRL & 0b10000000)  # if OSF is set to one the oscillator has been stopped

    # register functions ---------------------------------------------------------------------------------------------------------
    def setReg(self, reg, dat): # write a byte to a register
        self.i2c.writeto_mem(DS3231_I2C_ADDR, reg, bytes([dat]))

    def getReg(self, reg):      # read a byte from a register
        return self.i2c.readfrom_mem(DS3231_I2C_ADDR, reg, 1)[0]

    def DecToBCD(self, dat):    
        return (dat//10) * 16 + (dat%10)

    def BCDToDec(self, dat):    
        return (dat//16) * 10 + (dat%16)

    # get times functions -------------------------------------------------------------------------------------------------------
    def getYear(self):
        '''the DS3231 works with only 2-digit years'''
        return self.BCDToDec(self.getReg(DS3231_REG_YEAR)) + 2000

    def getMonth(self):
        return self.BCDToDec(self.getReg(DS3231_REG_MONTH))

    def getDay(self):
        return self.BCDToDec(self.getReg(DS3231_REG_DAY))

    def getDayOfWeek(self):
        return self.BCDToDec(self.getReg(DS3231_REG_WEEKDAY))

    def getHour(self):
        return self.BCDToDec(self.getReg(DS3231_REG_HOUR))    

    def getMinute(self):
        return self.BCDToDec(self.getReg(DS3231_REG_MIN))    

    def getSecond(self):
        return self.BCDToDec(self.getReg(DS3231_REG_SEC))
    
    def getDate(self):
        return [self.getYear(), self.getMonth(), self.getDay()]

    def getTime(self):
        return [self.getHour(), self.getMinute(), self.getSecond()]            

    def getDateTime(self):
        return self.getDate() + [self.getDayOfWeek()] + self.getTime()

    # set times functions -------------------------------------------------------------------------------------------------------
    
    def setYear(self, year): 
        '''the DS3231 works with only 2-digit years'''
        if year > 2000:
            year -= 2000
        self.setReg(DS3231_REG_YEAR, self.DecToBCD(year%100))        
        
    def setMonth(self, month):
        self.setReg(DS3231_REG_MONTH, self.DecToBCD(month%13))
    
    def setDay(self, day):
        self.setReg(DS3231_REG_DAY, self.DecToBCD(day%32))
    
    def setDayOfWeek(self, dayOfWeek):
        self.setReg(DS3231_REG_WEEKDAY, self.DecToBCD(dayOfWeek%8))
        
    def setHour(self, hour):
        self.setReg(DS3231_REG_HOUR, self.DecToBCD(hour%24))
        
    def setMinute(self, minute):
        self.setReg(DS3231_REG_MIN, self.DecToBCD(minute%60))
    
    def setSecond(self, second):
        self.setReg(DS3231_REG_SEC, self.DecToBCD(second%60))
    
    def setDate(self, dat=(2020,1,1)):
        self.setYear(dat[0]%100)
        self.setMonth(dat[1]%13)
        self.setDay(dat[2]%32)      

    def setTime(self, dat =(0,0,0)):
        self.setHour(dat[0]%24)
        self.setMinute(dat[1]%60)
        self.setSecond(dat[2]%60)  

    def setDateTime(self, dat=(2020,1,1,1,0,0,0)):
        self.setYear(dat[0])
        self.setMonth(dat[1])
        self.setDay(dat[2])
        self.setWeekday(dat[3])
        self.setHour(dat[4])
        self.setMinute(dat[5])
        self.setSecond(dat[6])        
        
    def setDateTime(self, year, month, day, dayOfWeek, hour, minute, second): 
        # set all the date and times (year is last two digits of year)
        self.setYear(year)
        self.setMonth(month)
        self.setDay(day)
        self.setDayOfWeek(dayOfWeek)
        self.setHour(hour)
        self.setMinute(minute)
        self.setSecond(second)
        
    # get alarm functions ------------------------------------------------------------------------------------------------------
    def getAlarm1Triggerd(self):
        # check if alarm 1 triggerd
        REG_STA = self.getReg(DS3231_REG_STA)
        return (REG_STA & 0b00000001) == 1

    def getAlarm2Triggerd(self):
        # check if alarm 2 triggerd
        REG_STA = self.getReg(DS3231_REG_STA)
        return (REG_STA & 0b00000010) == 2

    def getAlarm1Enabled(self):
        return self.getReg(DS3231_REG_CTRL) & 0b00000001 == 1    # check if enabled bit is set

    def getAlarm2Enabled(self):
        return self.getReg(DS3231_REG_CTRL) & 0b00000010 == 2    # check if enabled bit is set

    def getAlarmSecMinHour(self,dat):    # get second, minute or hour - same procedure
        SecMinHour = dat & 0b01111111
        return self.BCDToDec(SecMinHour)

    def getAlarm1State(self):
        '''
        Get the state bits for alarm 1
        Returns a tupel with (day, hour, minute, second, type, enabled)
        '''
        A1SEC = self.getReg(DS3231_REG_A1SEC)    # read register
        A1M1 = (A1SEC & 0b10000000) == 128       # analyse bit
        A1SEC = self.getAlarmSecMinHour(A1SEC)             # convert to readable format
        A1MIN = self.getReg(DS3231_REG_A1MIN)
        A1M2 = (A1MIN & 0b10000000) == 128
        A1MIN = self.getAlarmSecMinHour(A1MIN)
        A1HOUR = self.getReg(DS3231_REG_A1HOUR)
        A1M3 = (A1HOUR & 0b10000000) == 128
        A1HOUR = self.getAlarmSecMinHour(A1HOUR)
        A1DAY = self.getReg(DS3231_REG_A1DAY)
        A1M4 = (A1DAY & 0b10000000) == 128
        A1DOTW = (A1DAY & 0b01000000) == 64      # True: day of the week, False: day of the month
        A1DAY = self.getAlarmSecMinHour(A1DAY)

        ENABLED = self.getAlarm1Enabled()
        TRIGGERD = self.getAlarm1Triggerd()

        # analyse mask bits - assuming all bits have been set correctly
        if A1M1:
            return (A1DAY, A1HOUR, A1MIN, A1SEC, A1_EVERY_SECOND, ENABLED, TRIGGERD)
        elif A1M2:
            return (A1DAY, A1HOUR, A1MIN, A1SEC, A1_ON_SECOND, ENABLED, TRIGGERD)
        elif A1M3:
            return (A1DAY, A1HOUR, A1MIN, A1SEC, A1_A2_ON_MINUTE_SECOND, ENABLED, TRIGGERD)
        elif A1M4:
            return (A1DAY, A1HOUR, A1MIN, A1SEC, A1_ON_HOUR_MINUTE_SECOND, ENABLED, TRIGGERD)
        elif A1DOTW:
            return (A1DAY, A1HOUR, A1MIN, A1SEC, A1_ON_WEEKDAY_HOUR_MINUTE_SECOND, ENABLED, TRIGGERD)
        else:
            return (A1DAY, A1HOUR, A1MIN, A1SEC, A1_ON_DAY_HOUR_MINUTE_SECOND, ENABLED, TRIGGERD)

    def getAlarm2State(self):
        '''
        Get the state bits for alarm 2
        Returns a tupel with (day, hour, minute, second, type) - second always 0 for alarm 2
        '''
        A2MIN = self.getReg(DS3231_REG_A2MIN)    # read register
        A2M2 = (A2MIN & 0b10000000) == 128       # analyse bit
        A2MIN = self.getAlarmSecMinHour(A2MIN)             # convert to readable format
        A2HOUR = self.getReg(DS3231_REG_A2HOUR)
        A2M3 = (A2HOUR & 0b10000000) == 128
        A2HOUR = self.getAlarmSecMinHour(A2HOUR)
        A2DAY = self.getReg(DS3231_REG_A2DAY)
        A2M4 = (A2DAY & 0b10000000) == 128
        A2DOTW = (A2DAY & 0b01000000) == 64      # True: day of the week, False: day of the month
        A2DAY = self.getAlarmSecMinHour(A2DAY)

        ENABLED = self.getAlarm2Enabled()
        TRIGGERD = self.getAlarm2Triggerd()

        # analyse mask bits - assuming all bits have been set correctly
        if A2M2:
            return (A2DAY, A2HOUR, A2MIN, 0, A2_EVERY_MINUTE, ENABLED, TRIGGERD)
        elif A2M3:
            return (A2DAY, A2HOUR, A2MIN, 0, A2_ON_MINUTE, ENABLED, TRIGGERD)
        elif A2M4:
            return (A2DAY, A2HOUR, A2MIN, 0, A2_ON_HOUR_MINUTE, ENABLED, TRIGGERD)
        elif A2DOTW:
            return (A2DAY, A2HOUR, A2MIN, 0, A2_ON_WEEKDAY_HOUR_MINUTE, ENABLED, TRIGGERD)
        else:
            return (A2DAY, A2HOUR, A2MIN, 0, A2_ON_WEEKDAY_HOUR_MINUTE, ENABLED, TRIGGERD)
    
        
    # set alarm functions -------------------------------------------------------------------------------------------------------
    
    def setAlarm1(self, day, hour, minute, second = 0, alarmType = A1_ON_SECOND):
        M1 = M2 = M3 = M4 = 0x80    # set masking bits
        DT = 0x0
        if alarmType == A1_EVERY_SECOND:
            pass
        elif alarmType == A1_ON_SECOND:
            M1 = 0x0
        elif alarmType == A1_A2_ON_MINUTE_SECOND:
            M1 = M2 = 0x0
        elif alarmType == A1_ON_HOUR_MINUTE_SECOND:
            M1 = M2 = M3 = 0x0
        else:
            M1 = M2 = M3 = M4 = 0x0
            if alarmType == A1_ON_WEEKDAY_HOUR_MINUTE_SECOND:
                DT = 0x40

        self.setReg(DS3231_REG_A1SEC,  self.DecToBCD(second%60)|M1)
        self.setReg(DS3231_REG_A1MIN,  self.DecToBCD(minute%60)|M2)
        self.setReg(DS3231_REG_A1HOUR, self.DecToBCD(hour%24)|M3)
        self.setReg(DS3231_REG_A1DAY,  self.DecToBCD(day%32)|M4|DT)

    def setAlarm2(self, day, hour, minute, alarmType = A2_EVERY_MINUTE): 
        M2 = M3 = M4 = 0x80    # set masking bits
        DT = 0x0
        if alarmType == A2_EVERY_MINUTE:
            pass
        elif alarmType == A2_ON_MINUTE:
            M2 = 0x0
        elif alarmType == A2_ON_HOUR_MINUTE:
            M2 = M3 = 0x0
        else:
            M2 = M3 = M4 = 0x0
            if alarmType == A2_ON_WEEKDAY_HOUR_MINUTE:
                DT = 0x40

        self.setReg(DS3231_REG_A2MIN,  self.DecToBCD(minute%60)|M2)
        self.setReg(DS3231_REG_A2HOUR, self.DecToBCD(hour%24)|M3)
        self.setReg(DS3231_REG_A2DAY,  self.DecToBCD(day%32)|M4|DT)

    def enableAlarm1(self):        # enable alarm interrupt
        CTRL_REG = self.getReg(DS3231_REG_CTRL)
        CTRL_REG = CTRL_REG | 0b00000001
        self.setReg(DS3231_REG_CTRL, CTRL_REG)

    def enableAlarm2(self):        # enable alarm interrupt
        CTRL_REG = self.getReg(DS3231_REG_CTRL)
        CTRL_REG = CTRL_REG | 0b00000010
        self.setReg(DS3231_REG_CTRL, CTRL_REG)

    def disableAlarm1(self):        # disable alarm interrupt
        CTRL_REG = self.getReg(DS3231_REG_CTRL)
        CTRL_REG = CTRL_REG & 0b11111110
        self.setReg(DS3231_REG_CTRL, CTRL_REG)

    def disableAlarm2(self):        # disable alarm interrupt
        CTRL_REG = self.getReg(DS3231_REG_CTRL)
        CTRL_REG = CTRL_REG & 0b11111101
        self.setReg(DS3231_REG_CTRL, CTRL_REG)

    def resetAlarm1(self):          # will pull SQW high if no alarm is set
        STA_REG = self.getReg(DS3231_REG_STA)
        STA_REG = STA_REG & 0b11111110
        self.setReg(DS3231_REG_STA, STA_REG)

    def resetAlarm2(self):          # will pull SQW high if no alarm is set
        STA_REG = self.getReg(DS3231_REG_STA)
        STA_REG = STA_REG & 0b11111101
        self.setReg(DS3231_REG_STA, STA_REG)

    # temperature
    def getTemperature(self):
        t1 = self.getReg(DS3231_REG_TEMP)
        t2 = self.getReg(DS3231_REG_TEMP + 1)
        if t1>0x7F:
            return t1 - t2/256 -256
        else:
            return t1 + t2/256
        
