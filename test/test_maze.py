import unittest
from random import randint

from maze.maze import Maze, Cell, MazeStatus


class MyTestCase(unittest.TestCase):
    def test_neighbours_origin(self):
        maze = Maze()
        length = randint(1, 10)
        maze.set_board([[Cell(i, j, False) for i in range(length)] for j in range(length)])
        neighbours_to_origin = maze.get_cell_neighbours(0, 0)
        self.assertEqual(2, len(neighbours_to_origin))

    def test_neighbours_center(self):
        maze = Maze()
        length = randint(1, 10)
        maze.set_board([[Cell(i, j, False) for i in range(length)] for j in range(length)])
        neighbours_to_center = maze.get_cell_neighbours(1, 1)
        self.assertEqual(4, len(neighbours_to_center))

    def test_get_status_INIT(self):
        maze = Maze()
        length = randint(1, 10)
        maze.set_board([[Cell(i, j, False) for i in range(length)] for j in range(length)])
        self.assertEqual(MazeStatus.INIT, maze.get_status())

    def test_get_status_GENERATING(self):
        maze = Maze()
        length = randint(1, 10)
        maze.set_board([[Cell(i, j, False) for i in range(length)] for j in range(length)])
        maze.set_track({maze.get_cell(0, 0): []})
        maze.set_cell_value(0, 0, True)
        self.assertEqual(MazeStatus.GENERATING, maze.get_status())

    def test_get_status_READY(self):
        maze = Maze()
        length = randint(1, 10)
        maze.set_board([[Cell(i, j, True) for i in range(length)] for j in range(length)])
        maze.set_track({maze.get_cell(0, 0): []})
        self.assertEqual(MazeStatus.READY, maze.get_status())


if __name__ == '__main__':
    unittest.main()
