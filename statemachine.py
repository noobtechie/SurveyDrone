import asyncio
import sys

class StateMachine:
    def __init__(self):
        self.handlers = {}
        self.startState = None
        self.endStates = []

    async def add_state(self, name, handler, end_state=0):
        """
        Add a state to the FSM

        Parameters
        ----------
        name: str
            The name of the state
        handler: func()
            The handler function to be associated with the state name
        end_state: bool
            identify if the added state is an end state or not

        """
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    async def set_start(self, name):
        """
        Set the start state of the FSM referenced by the name

        Parameters
        ----------
        name: str
            The name of the state

        """
        self.startState = name.upper()

    def InitializationError(self, message):
        print(message)

    async def run(self, cargo):
        """
        Set the start state of the FSM referenced by the name

        Parameters
        ----------
        cargo: var
                Any argument that needs to be passed to the next state

        """
        try:
            handler = self.handlers[self.startState]
        except :
            raise self.InitializationError("must call .set_start() before .run()")
        if not self.endStates:
            raise self.InitializationError("at least one state must be an end_state")

        while True:
            (newState, cargo) = await handler(cargo)
            if newState.upper() in self.endStates:
                print("reached ", newState)
                break
            else:
                handler = self.handlers[newState.upper()]
