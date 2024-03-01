# Class of node
#Imports
import nodeStates

class Node:
    def __init__(self, x: int, y: int, state = nodeStates.noneState):
        self._x = x
        self._y = y
        self._state = state

    def changeState(self, opt):
        self.state = self.state.changeState(opt)

    def getState(self):
        return self.state

    def getCoordinates(self):
        return (self._x, self._y)