# Implementation of state of nodes in maze

class State:
    def __init__(self):
        pass

    def changeState(self, opt):
        pass

# 0 - default state
class noneState(State):
    def changeState(self, opt: int):
        if opt == 0:
            return self
        elif 0 < opt < len(states):
            return states[opt]()
        else:
            raise ValueError("Such state do not exist or it cannot be set for this node!")

    def __str__(self):
        return "n"

# 1
class wallState(State):
    def changeState(self, opt: int):
        if opt == 0:
            return self
        elif opt == 2:
            return freeState()
        else:
            raise ValueError("Such state do not exist or it cannot be set for this node!")

    def __str__(self):
        return "wall"

# 2
class freeState(State):
    def changeState(self, opt: int):
        if opt == 2:
            return self
        elif opt == 3:
            return dotState()
        else:
            raise ValueError("Such state do not exist or it cannot be set for this node!")

    def __str__(self):
        return "free"

# 3
class dotState(State):
    def changeState(self, opt: int):
        if opt == 3:
            return self
        elif opt == 2:
            return freeState()
        else:
            raise ValueError("Such state do not exist or it cannot be set for this node!")

    def __str__(self):
        return "dot"


states = [noneState, wallState, freeState, dotState]


