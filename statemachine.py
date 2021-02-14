import asyncio
import sys

class StateMachine:
    def __init__(self):
        self.handlers = {}
        self.startState = None
        self.endStates = []

    async def add_state(self, name, handler, end_state=0):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    async def set_start(self, name):
        self.startState = name.upper()

    def InitializationError(self, message):
        print(message);

    async def run(self, cargo):
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
