# Class of node
#Imports
from creatures2 import Creature
import nodeStates2 as nodeStates2

class Node:
    def __init__(self, x: int, y: int, team: int = 0, state = nodeStates2.noneState):
        self._x = x
        self._y = y
        self._team = team
        self._stateClass = state
        self._state = state()
        self._taken = False

    def changeState(self, opt):
        self._state = self._state.changeState(opt)
        self._stateClass = nodeStates2.states[opt]
        
    def getState(self):
        return self._state

    def getCoordinates(self):
        return (self._x, self._y)

    def isTaken(self):
        return self._taken
    
    def placeCreatue(self, creature: Creature):
        # self._team = creature.getTeam()
        self._taken = True
    
    def setFree(self):
        self._taken = False
        self._team = 0
    
    def getTeam(self):
        return self._team

    def getStateClass(self):
        return self._stateClass