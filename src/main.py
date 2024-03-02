# Imports
import maze

m = 10
n = 10

def main():
    myMaze = maze.Maze(m, n, 4)
    for i in range(m):
        for j in range(n):
            print(myMaze.getNode(i, j).getState(), end = '')
        print()

if __name__ == '__main__':
    main()


