from pysm import State, StateMachine, Event
import time
import uasyncio as asyncio

Phase1 = State('Phase1')
Phase2 = State('Phase2')
Phase3 = State('Phase3')
Phase4 = State('Phase4')
Phase5 = State('Phase5')


sm = StateMachine('sm')
sm.add_state(Phase1, initial=True)
sm.add_state(Phase2)
sm.add_state(Phase3)
sm.add_state(Phase4)
sm.add_state(Phase5)

sm.add_transition(Phase1, Phase2, events=['ToPhase2'])
sm.add_transition(Phase2, Phase3, events=['ToPhase3'])
sm.add_transition(Phase3, Phase4, events=['ToPhase4'])
sm.add_transition(Phase4, Phase5, events=['ToPhase5'])
sm.add_transition(Phase5, Phase1, events=['ToPhase1'])

def on_enter(state, event):
    print('')
    print('Enter state {0}'.format(state.name))

def on_exit(state, event):
    print('Exit state {0}'.format(state.name))

# Attach enter/exit handlers
states = [Phase1, Phase2, Phase3, Phase4]
for state in states:
    state.handlers = {'enter': on_enter, 'exit': on_exit}

sm.initialize()

def doPhase1():
    print('Reading config.')
    time.sleep(1)
    print('If RTC: Read & set time')
    time.sleep(1)
    sm.dispatch(Event('ToPhase2'))

async def doPhase2():
    res = None
    tasks = [Wan(), MeasureBus0(), MeasureBus1(), MeasureBus2()]
    try:
        res = await asyncio.gather(*tasks, return_exceptions=True)
    except asyncio.TimeoutError:  # These only happen if return_exceptions is False
        print('Timeout')  # With the default times, cancellation occurs first
    except asyncio.CancelledError:
        print('Cancelled')    
    sm.dispatch(Event('ToPhase3'))

async def Wan():
    print('Connectin WAN (Wifi, LoRa...)')
    await asyncio.sleep(10)
    print('WAN connected.')

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
    sm.dispatch(Event('ToPhase4'))

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
    sm.dispatch(Event('ToPhase5'))

def doPhase5():
    print('Deciding how to sleep.')
    time.sleep(2)
    sm.dispatch(Event('ToPhase1'))



if __name__ == '__main__':

    while True:
        if sm.state == None:
            doPhase1()
        if sm.state == Phase1:
            doPhase1()
        elif sm.state == Phase2:
            asyncio.run(doPhase2())
        elif sm.state == Phase3:
            doPhase3()
        elif sm.state == Phase4:
            asyncio.run(doPhase4())
        elif sm.state == Phase5:
            doPhase5()


