from ..models.Cell import Cell
from ..models.Maze import Maze


class A_star_search:
    def search(maze: Maze):
        start: Cell = maze.starting_point
        end: Cell = maze.ending_point

        # queue: (g, h, f)
        # g: distance from start
        # h: heuristic to end
        # f: g + h
        queue: dict[Cell:tuple[int, int, int]] = {}
        queue[start] = (0, A_star_search.heuristic(start, end),
                        A_star_search.heuristic(start, end))
        visited: list[Cell] = []

        while queue:
            current = queue.popitem()
            visited.append(current)
            if current == end:
                return A_star_search.reconstruct_path(maze, current)

            for neighbor in A_star_search.get_neighbors(maze, current):
                g = A_star_search.heuristic(start, neighbor)
                h = A_star_search.heuristic(neighbor, end)
                f = g + h
                if neighbor not in list(queue.keys()):
                    neighbor.setParent(current)
                    queue[neighbor] = (g, h, f)
                elif queue[neighbor][2] < f:
                    queue[neighbor] = (g, h, f)
            queue = A_star_search.sorted_dict(queue)
        return None

    @staticmethod
    def sorted_dict(dict: dict[Cell.Cell:int]):
        return dict(sorted(dict.items(), key=lambda item: (item[2], item[1]), reverse='True'))

    @staticmethod
    def get_neighbors(maze: Maze, cell: Cell):
        neighbors: list[Cell] = []
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

    @staticmethod
    def heuristic(cell: Cell, end: Cell):
        return abs(cell.x - end.x) + abs(cell.y - end.y)

    @staticmethod
    def reconstruct_path(maze: Maze, current: Cell):
        path = []
        while current.parent:
            path.append(current)
            current = current.parent
        path.append(maze.starting_point)
        path.reverse()
        return path
