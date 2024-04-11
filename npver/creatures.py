# Implementation of creatures: Pacman and Ghost
import numpy as np

def createPacmans():
    pacmans = np.array([[0, 0, 1, 1, 0], [0, 0, 2, 1, 0]], dtype=int) # i j team alive points
    return pacmans

def createGhosts(n: int = 4):
    ghosts = np.empty((n*2, 6), dtype=int)
    for i in range(n * 2):
        ghost = np.array([0, 0, 2, 1, 0, -1]) # i j team cntInRow lastI lastJ
        ghosts[i] = ghost
    for i in range(n):
        ghosts[i][2] = 1
    return ghosts
