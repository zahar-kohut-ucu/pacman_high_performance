# Imports
import maze

m = 20
n = 20

def main():
    myMaze = maze.Maze(m, n, 4, 101)
    for i in range(m):
        for j in range(n):
            print(myMaze.getNode(i, j).getState(), end = '')
        print()

if __name__ == '__main__':
    main()


