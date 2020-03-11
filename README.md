Maze-python
==============================

Project of a maze generator in Python 3.8+

Getting Started
------------
Just launch in your favorite terminal,

`python main.py` 

You will see two drawings : the first one is the maze representation and the second one is the maze with the result path solving the maze

Algorithms
------------
The maze is composed of:

      a board which is a 2-dimensional array 40x30 (each cell has coordinate and a boolean value)
      
      a starting point
      
      a finishing point
      
      a track which is a dictionnary where each cell is mapped with the cell it leads to.
      
The starting point and the finishing point are randomly selected.

### Building
To build the maze, I use the depth-first search algorithm: for each point a random neighbour is selected and stored.
While all points have not been seen, we continue. When we arrive to a point having all its neighbours selected,
we get back to the most recent point having unseen neighbours. The finish point is selected randomly among
these points. 
This algorithm has the advantage to be fast to implement and quick but generates simple mazes.

### Solving
To solve the maze and get a track as a result from the starting point and the finishing point, the algorithm is based on
a binary search trees algorithm. We look for the finish point among the children of a point. While it is not
found, we recursively look for it in the children of the children, etc.
The first path that get to the finishing point is rendered.
