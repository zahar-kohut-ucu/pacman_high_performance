# Class of node
#Imports
import nodeStates

class Node:
    def __init__(self, x: int, y: int, team: int, state = nodeStates.noneState):
        self._x = x
        self._y = y
        self.team = team
        self._stateClass = state
        self._state = state()
        self._isTaken = False

    def changeState(self, opt):
        self._state = self._state.changeState(opt)
        self._stateClass = nodeStates.states[opt]
        
    def getState(self):
        return self._state

    def getCoordinates(self):
        return (self._x, self._y)

    def isTaken(self):
        return self._isTaken

    def getStateClass(self):
        return self._stateClass