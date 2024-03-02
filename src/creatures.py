# Implementation of creatures: Pacman and Ghost
class Creature:
    def __init__(self, x: int, y: int, team: int) -> None:
        self._x = x 
        self._y = y
        self._team = team

    def move(self, x: int , y: int) -> None:
        self._x = x    
        self._y = y

    def getCoordinates(self) -> None:
        return (self._x, self._y)

    def getTeam(self) -> int:
        return self._team
    

class Pacman(Creature):
    def __init__(self, x: int, y: int, team: int) -> None:
        super().__init__(x, y, team)
        self._alive = True
        self._points = 0

    def addPoint(self) -> None:
        self._points += 1

    def getPoints(self) -> int:
        return self._points
    
    def isAlive(self) -> bool:
        return self._alive
    
    def killPacman(self) -> None:
        self._alive = False

    

class Ghost(Creature):
    def __init__(self, x: int, y: int, team: int) -> None:
        super().__init__(x, y, team)

def createPacmans() -> list[Pacman]:
    pacmans = []
    for i in range(2):
        pacmans.append(Pacman(0,0,2))
    pacmans[0]._team = 1
    return pacmans

def createGhosts(n: int = 3) -> list[Ghost]:
    ghosts = []
    for i in range(n * 2):
        ghosts.append(Ghost(0, 0, 2))
    for i in range(n):
        ghosts[i]._team = 1
    return ghosts
