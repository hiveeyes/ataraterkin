from pysm import State, StateMachine, Event

class atStateMachine():

    def __init__(self) -> None:
        # define states - in '' is the states name string
        self.BusAndTime = State('Create bus and set time')
        self.ConnectAndMeasure = State('Connect Wifi and measure')
        self.DataManipulation = State('Manipulate measurement data')
        self.Sending = State('Send data upstream')
        self.SleepingDecision = State('What to do until next measurement')

        # define the state machine
        self.machine = StateMachine('sm')

        # ad states to the machine - exactly one needs to be initial
        self.machine.add_state(self.BusAndTime, initial=True)
        self.machine.add_state(self.ConnectAndMeasure)
        self.machine.add_state(self.DataManipulation)
        self.machine.add_state(self.Sending)
        self.machine.add_state(self.SleepingDecision)

        # add the transitions and which events trigger it
        self.machine.add_transition(self.BusAndTime, self.ConnectAndMeasure, events=['ToConnectAndMeasure'])
        self.machine.add_transition(self.ConnectAndMeasure, self.DataManipulation, events=['ToDataManipulation'])
        self.machine.add_transition(self.DataManipulation, self.Sending, events=['ToSending'])
        self.machine.add_transition(self.Sending, self.SleepingDecision, events=['ToSleepingDecision'])
        self.machine.add_transition(self.SleepingDecision, self.BusAndTime, events=['ToConnectAndMeasure'])

        # initialize it
        self.machine.initialize()

    #standard handler
    def on_enter(self, state, event):
        print('')
        print('Enter state {0}'.format(state.name))

    #standard handler
    def on_exit(self, state, event):
        print('Exit state {0}'.format(state.name))
        print('')

