from abc import ABC, abstractmethod
import time
from random import randint, choice

from maze.maze import Maze, Cell, MazeStatus


class MazeBuilderException(Exception):
    pass


class Builder(ABC):

    @property
    @abstractmethod
    def maze(self):
        pass

    @abstractmethod
    def init_board(self, width, height):
        pass

    @abstractmethod
    def build(self):
        pass


class MazeBuilderWithRandomStart(Builder):
    """
    Builder getting the maze as input and setting the starting and finishing points, initializing the board of the maze
    and building the maze.
    """
    def __init__(self):
        self._maze = Maze()

    @property
    def maze(self):
        return self._maze

    def init_board(self, width, height):
        if width < 1 or height < 1:
            raise MazeBuilderException("Width and Height must be superior to 1")
        self._maze.set_board([[Cell(i, j, False) for i in range(width)] for j in range(height)])
        self._maze.set_start(randint(0, width-1), randint(0, height-1))

    def build(self):
        """
        The maze is built according to the following principle: for each point a random neighbour is selected and stored.
        While all points have not been seen, we continue. When we arrive to a point having all its neighbours selected,
        we get back to the most recent point having unseen neighbours. The finish point is selected randomly among
        these points
        :return: Map all cells with their natural children in the maze
        """
        parcours = []
        possible_finishes = []
        current_cell = self._maze.get_start()
        self._maze.set_cell_value(current_cell.x, current_cell.y, True)
        start_time = time.time()
        parcours.append(current_cell)
        track = self._maze.get_track()
        while self._maze.get_status() != MazeStatus.READY:
            current_cell_neighbours = self._maze.get_cell_neighbours(current_cell.x, current_cell.y)
            if len(current_cell_neighbours) > 0:
                direction, selected_neighbour = choice(list(current_cell_neighbours.items()))
                self._maze.set_cell_value(selected_neighbour.x, selected_neighbour.y, True)
                possible_track_from_cell = track.get(current_cell, [])
                possible_track_from_cell.append(selected_neighbour)
                track[current_cell] = possible_track_from_cell
                current_cell.next.append(direction)
                current_cell = selected_neighbour
                parcours.append(current_cell)
            else:
                if parcours:
                    current_cell = parcours.pop()
                    possible_finishes.append(current_cell)
                    if not self._maze.get_finish():
                        self._maze.set_finish(current_cell.x, current_cell.y)
        if parcours and not self._maze.get_finish():
            pop_item = parcours.pop()
            possible_finishes.append(pop_item)
        selected_finish = choice(possible_finishes)
        self._maze.set_finish(selected_finish.x, selected_finish.y)
        print("Maze generated in --- %s seconds ---" % (time.time() - start_time))
        self._maze.set_track(track)
        self._maze.display_with_graph()
        return track
