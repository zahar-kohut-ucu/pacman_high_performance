# Pac-Man game high performance implementations
Final project for course "Computer Systems Architechture" in UCU.

This project includes different implementaions of the same Pac-Man simulation (stored in ```default```, ```multithread```, ```numbafastver``` and ```max_perf``` folders). The game is modified, it includes 2 Pac-Man's and 2 teams of ghosts. Pac-Mans are controlled by Dijkstra's and A-Star algorithm.

There are visualisation modules based on PyGame library. To start the simulation with visualisation, you may set desired initial conditions in ```game.py``` and run it. 

```simulation.py``` is used for time and game performance testing, described below.

Also the project includes script for testing implementation's game and time performance (```testing/testing.py```). ```testing``` folder also contains modules for proper work of script. The results are stored in ```.txt``` files and may be plotted using ```perfplot.py``` and ```plot.py```.

Authors: Dmytryshyn Serhii and Kohut Zahar.