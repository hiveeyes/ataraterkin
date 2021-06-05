from pysm import State, StateMachine, Event

class atStateMachine():

    def __init__(self) -> None:
        # define states - in '' is the states name string
        self.BaseConfig = State('Read settings and set time')
        self.Phase2 = State('Phase2')
        self.Phase3 = State('Phase3')
        self.Phase4 = State('Phase4')
        self.Phase5 = State('Phase5')

        # define the state machine
        self.machine = StateMachine('sm')

        # ad states to the machine - exactly one needs to be initial
        self.machine.add_state(self.BaseConfig, initial=True)
        self.machine.add_state(self.Phase2)
        self.machine.add_state(self.Phase3)
        self.machine.add_state(self.Phase4)
        self.machine.add_state(self.Phase5)

        # add the transitions and which events trigger it
        self.machine.add_transition(self.BaseConfig, self.Phase2, events=['ToPhase2'])
        self.machine.add_transition(self.Phase2, self.Phase3, events=['ToPhase3'])
        self.machine.add_transition(self.Phase3, self.Phase4, events=['ToPhase4'])
        self.machine.add_transition(self.Phase4, self.Phase5, events=['ToPhase5'])
        self.machine.add_transition(self.Phase5, self.BaseConfig, events=['ToBaseConfig'])

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

