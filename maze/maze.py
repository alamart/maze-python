from enum import Enum
import time


class MazeStatus(Enum):
    INIT = "Initialized"
    GENERATING = "Generating"
    READY = "Ready"
    SOLVING = "Solving"
    SOLVED = "Solved"


class MazeDirection(Enum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"


class Cell:
    """Class representing a cell in the maze. It has a value used to generate the maze. Every cell has up to 4
    neighbours it is connected to in four directions"""
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.next = []

    def __repr__(self):
        return 'Cell(%s, %s) with value %s' % (str(self.x), str(self.y), str(self.value))


class Maze:

    def __init__(self):
        self._board = []
        self._start = None
        self._finish = None
        self._track = {}

    def set_board(self, board):
        self._board = board

    def set_start(self, x, y):
        self._start = self._board[y][x]

    def set_finish(self, x, y):
        self._finish = self._board[y][x]

    def set_track(self, track):
        self._track = track

    def get_track(self):
        return self._track

    def get_start(self):
        return self._start

    def get_finish(self):
        return self._finish

    def get_board(self):
        return self._board

    def get_status(self):
        for line in self._board:
            if self._track:
                if not all(cell.value for cell in line):
                    return MazeStatus.GENERATING
            else:
                return MazeStatus.INIT
        return MazeStatus.READY

    def get_cell(self, x, y):
        return self._board[y][x]

    def set_cell_value(self, x, y, value):
        self._board[y][x].value = value

    def get_cell_neighbours(self, x, y):
        height = len(self._board)
        if height > 0:
            width = len(self._board[0])
        else:
            width = 0
        if height == 0 or width == 0:
            return {}
        cell = self.get_cell(x, y)
        neighbours = {}
        if cell.x != 0 and not self._board[cell.y][cell.x - 1].value:
            neighbours[MazeDirection.WEST] = self._board[cell.y][cell.x - 1]
        if cell.x != width - 1 and not self._board[cell.y][cell.x + 1].value:
            neighbours[MazeDirection.EAST] = self._board[cell.y][cell.x + 1]
        if cell.y != 0 and not self._board[cell.y - 1][cell.x].value:
            neighbours[MazeDirection.NORTH] = self._board[cell.y - 1][cell.x]
        if cell.y != height - 1 and not self._board[cell.y + 1][cell.x].value:
            neighbours[MazeDirection.SOUTH] = self._board[cell.y + 1][cell.x]
        return neighbours

    def display_with_graph(self, path_to_highlight=[]):
        graph = []
        first_last_lane = ["###" for i in range(len(self._board[0])*2-1)]
        graph.append(first_last_lane)
        for cell_lane in self._board:
            lane_track = []
            lane_separator = []
            for cell in cell_lane:
                if cell == self._start:
                    lane_track.append(" S ")
                elif cell == self._finish:
                    lane_track.append(" F ")
                elif cell in path_to_highlight:
                    lane_track.append(" X ")
                else:
                    lane_track.append("   ")
                if cell_lane.index(cell) < len(cell_lane) - 1:
                    if MazeDirection.EAST in cell.next:
                        lane_track.append("   ")
                    elif MazeDirection.WEST in self.get_cell(cell.x + 1, cell.y).next:
                        lane_track.append("   ")
                    else:
                        lane_track.append(" | ")
                if self._board.index(cell_lane) < len(self._board) - 1:
                    if MazeDirection.SOUTH in cell.next:
                        lane_separator.append("   ")
                    elif MazeDirection.NORTH in self.get_cell(cell.x, cell.y+1).next:
                        lane_separator.append("   ")
                    else:
                        lane_separator.append("---")
                    if cell_lane.index(cell) < len(cell_lane) - 1:
                        lane_separator.append("---")
            graph.append(lane_track)
            if lane_separator:
                graph.append(lane_separator)
        graph.append(first_last_lane)
        for lane in graph:
            print("#", end="")
            print(''.join(lane), end="")
            print("#")

    def solve(self):
        start_time = time.time()
        track = self.get_track()
        start = self.get_start()
        finish = self.get_finish()
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
        print(f'Shortest path to finish : {len(final)} steps. See the result below')
        self.display_with_graph(path_to_highlight=final)
        return final
