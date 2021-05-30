from pysm import State, StateMachine, Event
import time
import uasyncio as asyncio

Init = State('Init')
Wan = State('Wan')
Measure = State('Measure')
Sending = State('Sending')
Sleep = State('Sleep')


sm = StateMachine('sm')
sm.add_state(Init, initial=True)
sm.add_state(Wan)
sm.add_state(Measure)
sm.add_state(Sending)
sm.add_state(Sleep)

sm.add_transition(Init, Wan, events=['ToWan'])
sm.add_transition(Wan, Measure, events=['ToMeasure'])
sm.add_transition(Measure, Sending, events=['ToSend'])
sm.add_transition(Sending, Sleep, events=['ToSleep'])
sm.add_transition(Sleep, Init, events=['Wakeup'])


def on_enter(state, event):
    print('Enter state {0}'.format(state.name))

def on_exit(state, event):
    print('Exit state {0}'.format(state.name))

# Attach enter/exit handlers
states = [Init, Wan, Measure, Sending, Sleep]
for state in states:
    state.handlers = {'enter': on_enter, 'exit': on_exit}

sm.initialize()

def atInit():
    print('Initialising...')
    time.sleep(1)
    sm.dispatch(Event('ToWan'))

def atWan():
    print('Connectin WAN...')
    time.sleep(1)
    sm.dispatch(Event('ToMeasure'))

async def atMeasure():
    print('Measuring...')
    res = None
    tasks = [atMeasureBus0(), atMeasureBus1(), atMeasureBus2()]
    try:
        res = await asyncio.gather(*tasks, return_exceptions=True)
    except asyncio.TimeoutError:  # These only happen if return_exceptions is False
        print('Timeout')  # With the default times, cancellation occurs first
    except asyncio.CancelledError:
        print('Cancelled')    
    print('Measuring ended')
    sm.dispatch(Event('ToSend'))

async def atMeasureBus0():
    print('Measuring on Bus0')
    await asyncio.sleep(1)
    print('Done measuring on Bus0')

async def atMeasureBus1():
    print('Measuring on Bus1')
    await asyncio.sleep(2)
    print('Done measuring on Bus1')

async def atMeasureBus2():
    print('Measuring on Bus2')
    await asyncio.sleep(3)
    print('Done measuring on Bus2')

def atSending():
    print('Sending...')
    time.sleep(1)
    sm.dispatch(Event('ToSleep'))

def atSleep():
    print('Sleeping...')
    time.sleep(2)
    sm.dispatch(Event('Wakeup'))



if __name__ == '__main__':
    while True:
        if sm.state == None:
            atInit()
        if sm.state == Init:
            atInit()
        elif sm.state == Wan:
            atWan()
        elif sm.state == Measure:
            asyncio.run(atMeasure())
        elif sm.state == Sending:
            atSending()
        elif sm.state == Sleep:
            atSleep()

