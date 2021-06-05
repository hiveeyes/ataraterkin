import time
import uasyncio as asyncio
import settings
import network
from statemachine import atStateMachine
from pysm import Event



def doBaseConfig():
    # decide where to get time
    if settings.main.get('RTC'):
        print('Reading the time from the DS3231')
        time.sleep(1)
        print('Set internal RTC')
    time.sleep(1)
    state.machine.dispatch(Event('ToPhase2'))

async def doPhase2():
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
    pass

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
    time.sleep(2)
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
    time.sleep(2)
    state.machine.dispatch(Event('ToBaseConfig'))

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('Zippen 24','{redacted}')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


if __name__ == '__main__':

    #do_connect()

    # create the statemachine
    state = atStateMachine()

    # Attach enter/exit handlers - if you want different handlers for a state you need to overwrite them
    for machinestate in state.machine.states:
        machinestate.handlers = {'enter': state.on_enter, 'exit': state.on_exit}

    while True:
        if state.machine.state == None:
            doBaseConfig()
        if state.machine.state == state.BaseConfig:
            doBaseConfig()
        elif state.machine.state == state.Phase2:
            asyncio.run(doPhase2())
        elif state.machine.state == state.Phase3:
            doPhase3()
        elif state.machine.state == state.Phase4:
            asyncio.run(doPhase4())
        elif state.machine.state == state.Phase5:
            doPhase5()


 

 