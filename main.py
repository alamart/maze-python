from maze.builder import MazeBuilderWithRandomStart
from maze.solver import MazeSolver


def main():
    maze_builder = MazeBuilderWithRandomStart()
    maze_builder.init_board(40, 30)
    maze_builder.build()
    maze_solver = MazeSolver(maze_builder)
    maze_solver.solve()


if __name__ == '__main__':
    main()
