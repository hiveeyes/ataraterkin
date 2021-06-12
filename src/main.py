from time import sleep
import uasyncio as asyncio
import settings
import network
from statemachine import atStateMachine
from pysm import Event


def BusAndTime():
    # create bus objects
    from bus import atBus
    global busses
    busses = atBus(settings.bus)

    # setting the time
    try:
        params = settings.time['RTC']
        if params['enabled']:
            from DS3231tokei import DS3231
            if params['bus'] == 'i2c0':
                DS3231 = DS3231(busses.i2c0)
            elif params['bus'] == 'i2c1':
                DS3231 = DS3231(busses.i2c1)
            else:
                raise Exception
        (year,month,day,dotw,hour,minute,second) = DS3231.getDateTime() # get the current time
        print('Date: {}.{}.{}, Time: {}h {}m {}s'.format(day,month,year,hour,minute,second))
        from machine import RTC
        rtc = RTC() # create RTC
        if year < 2001:
            year = 2001 # sanity check, as of mpy 1.12 year must be >= 2001
        print('Setting internal RTC')
        rtc.init((year,month,day,dotw,hour,minute,second,0)) # set time
        state.machine.dispatch(Event('ToWifiMeasure'))
    except:
        print('Fault reading RTC in settings.py')

async def WifiAndMeasure():
    res = None
    tasks = [Wan(), MeasureBus0(), MeasureBus1(), MeasureBus2()]
    try:
        res = await asyncio.gather(*tasks, return_exceptions=True)
    except asyncio.TimeoutError:  # These only happen if return_exceptions is False
        print('Timeout')  # With the default times, cancellation occurs first
    except asyncio.CancelledError:
        print('Cancelled') 
    state.machine.dispatch(Event('ToPhase3'))

async def Wan():
    print('Wan')

async def MeasureBus0():
    print('Measuring on Bus0')
    await asyncio.sleep(1)
    print('Done measuring on Bus0')

async def MeasureBus1():
    print('Measuring on Bus1')
    await asyncio.sleep(4)
    print('Done measuring on Bus1')

async def MeasureBus2():
    print('Measuring on Bus2')
    await asyncio.sleep(7)
    print('Done measuring on Bus2')

def doPhase3():
    print('Data crunching.')
    sleep(2)
    state.machine.dispatch(Event('ToPhase4'))

async def SendZeData():
    print('Connecting to server...')
    await asyncio.sleep(1)
    print('Sending data...')
    await asyncio.sleep(2)
    print('Closing connection.')

async def DoingDishes():
    print('Updating web server')
    await asyncio.sleep(2)
    print('Do whatever')
    await asyncio.sleep(1)
    print('Finished the dishes.')

async def doPhase4():
    print('Sending data and doing the dishes.')
    res = None
    tasks = [SendZeData(), DoingDishes()]
    try:
        res = await asyncio.gather(*tasks, return_exceptions=True)
    except asyncio.TimeoutError:  # These only happen if return_exceptions is False
        print('Timeout')  # With the default times, cancellation occurs first
    except asyncio.CancelledError:
        print('Cancelled')    
    state.machine.dispatch(Event('ToPhase5'))

def doPhase5():
    print('Deciding how to sleep.')
    sleep(2)
    state.machine.dispatch(Event('ToWifiMeasure'))

async def ataraterkin():
   # create the statemachine
    global state
    state = atStateMachine()

    # Attach enter/exit handlers - if you want different handlers for a state you need to overwrite them
    for machinestate in state.machine.states:
        machinestate.handlers = {'enter': state.on_enter, 'exit': state.on_exit}

    #do_connect()

    # create the statemachine
    state = atStateMachine()

    # Attach enter/exit handlers - if you want different handlers for a state you need to overwrite them
    for machinestate in state.machine.states:
        machinestate.handlers = {'enter': state.on_enter, 'exit': state.on_exit}

    while True:
        if state.machine.state == None:
            BusAndTime()
        if state.machine.state == state.BusAndTime:
            BusAndTime()
        elif state.machine.state == state.WifiAndMeasure:
            await WifiAndMeasure()
        elif state.machine.state == state.Phase3:
            doPhase3()
        elif state.machine.state == state.Phase4:
            asyncio.run(doPhase4())
        elif state.machine.state == state.Phase5:
            doPhase5()


if __name__ == '__main__':

    asyncio.run(ataraterkin())

