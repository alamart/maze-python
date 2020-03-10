from abc import ABC, abstractmethod
import time

from maze.builder import Builder


class Solver(ABC):

    @property
    @abstractmethod
    def builder(self):
        pass

    @abstractmethod
    def solve(self):
        pass


class MazeSolver(Solver):
    """
    Solver getting the maze builder as input and finding the path from the starting point to the finish
    """

    def __init__(self, builder):
        self._builder = builder

    @property
    def builder(self) -> Builder:
        return self._builder

    def solve(self):
        """
        Getting the maze information, we determine the path from start to finish. The algorithm is based on
        a binary search trees algorithm. We look for the finish point among the children of a point. While it is not
        found, we recursively look for it in the children of the children, etc.
        :return: Points list to go to the finish from the starting point
        """
        start_time = time.time()
        track = self.builder.maze.get_track()
        start = self.builder.maze.get_start()
        finish = self.builder.maze.get_finish()
        parcours = []
        current_cell = start
        parcours.append([current_cell])
        final = []
        while not final:
            new_parcours = []
            for possible_parcours in parcours:
                last_visited = possible_parcours[-1]
                next_cells = track.get(last_visited, [])
                if finish in next_cells:
                    final = possible_parcours
                    break
                for next_cell in next_cells:
                    new_route = possible_parcours.copy()
                    new_route.append(next_cell)
                    new_parcours.append(new_route)
            parcours = new_parcours

        print("Maze solved in --- %s seconds ---" % (time.time() - start_time))
        print(f'Shortest path to finish : {len(final)} steps from {start} to {finish}. See the result below')
        self.builder.maze.display_with_graph(path_to_highlight=final)
        return final
