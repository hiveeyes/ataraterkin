import gc
from time import sleep, time
import uasyncio as asyncio
import settings
import network
from mqtt import atMQTTClient
from statemachine import atStateMachine
from pysm import Event
from measurements import atMeasurements

gc.collect()

measurements = atMeasurements() # all measurement methods
if settings.networking['wifi']['enabled']:
    wlan = network.WLAN(network.STA_IF) # create station interface
    wlan.active(True)       # activate the interface
if settings.networking['mqtt']['enabled']:
    mqttclient = atMQTTClient(settings.networking['mqtt'])

gc.collect()

def BusAndTime():
    # create bus objects
    from bus import atBus
    global busses
    busses = atBus(settings.bus)

    # setting the time
    from clock import atClock
    global intRTC, extRTC   # internal & external RTC
    atRTC = atClock(settings.time, busses)
    intRTC = atRTC.intRTC
    extRTC = atRTC.extRTC

    # to next state
    state.machine.dispatch(Event('ToConnectAndMeasure'))

async def ConnectAndMeasure():
    '''connect to the outside and start measuring'''
    tasks = [Wan()] # for now always connect to Wifi but this is not mandatory
    global results = []

    for sensor in settings.sensors:     # all measuring function have to be appended to tasks[] and will be executed concurrently
        if sensor == 'DS3231' and settings.sensors[sensor]['enabled']:
            tasks.append(measurements.getDS3231temperature(extRTC))
        elif sensor == 'somethingelse':
            pass
    try:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        print('Measurement results: ',results)
    except asyncio.TimeoutError:  # These only happen if return_exceptions is False
        print('Timeout')  # With the default times, cancellation occurs first
    except asyncio.CancelledError:
        print('Cancelled') 
    state.machine.dispatch(Event('ToDataManipulation'))

async def Wan():

    try:
        if settings.networking['wifi']['enabled']:
            global wlan
            if not wlan.isconnected():      # check if the station is connected to an AP
                wlan.connect(settings.networking['wifi']['ssid'], settings.networking['wifi']['wifi_pw']) # connect to an AP
                print('wlan.ifconfig()')         # get the interface's IP/netmask/gw/DNS addresses
                for _ in range(3):
                    if not wlan.isconnected():
                        raise OSError  # in 1st secs
                    await asyncio.sleep(1)
                print('Wifi is reliable')
        else:
            print('TODO: other WAN connections...')   # TODO
    except OSError:
        print('connection to wifi failed')

def DataManipulation():
    print('Data crunching.')
    print results
    sleep(2)
    state.machine.dispatch(Event('ToSending'))

def Sending():
    '''send data to Kotori'''
    print('Connecting')
    mqttclient.connect()
    print('publishing')
    mqttclient.publish('topic/time', '{}'.format(123), qos = 1)
    print('Published data to broker')
    mqttclient.disconnect()

    state.machine.dispatch(Event('ToSleepingDecision'))

def SleepingDecision():
    print('Deciding how to sleep.')
    sleep(2)
    state.machine.dispatch(Event('ToConnectAndMeasure'))

async def ataraterkin():
   # create the statemachine
    global state
    state = atStateMachine()

    # Attach enter/exit handlers - if you want different handlers for a state you need to overwrite them
    for machinestate in state.machine.states:
        machinestate.handlers = {'enter': state.on_enter, 'exit': state.on_exit}

    while True:
        if state.machine.state == state.BusAndTime:
            BusAndTime()
            gc.collect()
        elif state.machine.state == state.ConnectAndMeasure:
            await ConnectAndMeasure()
            gc.collect()
        elif state.machine.state == state.DataManipulation:
            DataManipulation()
            gc.collect()
        elif state.machine.state == state.Sending:
            Sending()
            gc.collect()
        elif state.machine.state == state.SleepingDecision:
            SleepingDecision()
            gc.collect()


if __name__ == '__main__':

    asyncio.run(ataraterkin())
