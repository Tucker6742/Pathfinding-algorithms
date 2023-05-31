from ..models import Cell
from ..models import Maze


class A_star_search:
    def search(maze: Maze.Maze):
        start: Cell = maze.starting_point
        end: Cell = maze.ending_point
        queue: dict[Cell.Cell:int] = {}
        queue[start] = 0
        visited: list[Cell.Cell] = []

        while queue:
            current = queue.popitem()
            visited.append(current)
            if current == end:
                return "Found!"

            for neighbor in A_star_search.get_neighbors(maze, current):
                if neighbor not in queue:
                    queue[neighbor] = 0

    @staticmethod
    def sorted_dict(dict: dict[Cell.Cell:int]):
        return dict(sorted(dict.items(), key=lambda item: item[1], reverse='True'))

    @staticmethod
    def get_neighbors(maze: Maze.Maze, cell: Cell.Cell):
        neighbors: list[Cell.Cell] = []
        x = cell.x
        y = cell.y
        if x > 0:
            neighbors.append(maze.cells[y][x-1])
        if x < maze.width - 1:
            neighbors.append(maze.cells[y][x+1])
        if y > 0:
            neighbors.append(maze.cells[y-1][x])
        if y < maze.height - 1:
            neighbors.append(maze.cells[y+1][x])
        return neighbors
