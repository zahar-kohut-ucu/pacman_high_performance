# Imports
import maze

m = 20
n = 20

def main():
    myMaze = maze.Maze(m, n, 100, setSeed = True, seed = 100)
    for i in range(m + 2):
        for j in range(n * 2 + 3):
            print(myMaze.getNode(i, j).getState(), end = '')
        print()

if __name__ == '__main__':
    main()


