from queue import Queue
from src.models.Cell import Cell
from src.models.Maze import Maze
class BFS_Search:
    def search(maze: Maze):
        start: Cell = Cell(maze.starting_point[1], maze.starting_point[0])
        end: Cell = Cell(maze.ending_point[1], maze.ending_point[0])

        queue = Queue()
        queue.put(start)
        visited = set()
        visited.add(start)

        parent = {}
        parent[start] = None

        while not queue.empty():
            current = queue.get()

            if current.coordinate() == end.coordinate():
                print("Found path")
                return BFS_Search.reconstruct_path(maze, current), visited
            for neighbor in BFS_Search.get_neighbors(maze, current):
                if neighbor not in visited:
                    queue.put(neighbor)
                    visited.add(neighbor)
                    parent[neighbor] = current

        return None, visited

    @staticmethod
    def get_neighbors(maze: Maze, cell: Cell):
        neighbors = []
        x = cell.x
        y = cell.y

        if x < maze.width - 1:
            # right
            if maze.cells[y][x + 1].status == 0:
                neighbors.append(maze.cells[y][x + 1])
        if y > 0:
            # up
            if maze.cells[y - 1][x].status == 0:
                neighbors.append(maze.cells[y - 1][x])
        if y < maze.height - 1:
            # down
            if maze.cells[y + 1][x].status == 0:
                neighbors.append(maze.cells[y + 1][x])
        if x > 0:
            # left
            if maze.cells[y][x - 1].status == 0:
                neighbors.append(maze.cells[y][x - 1])

        return neighbors

    @staticmethod
    def reconstruct_path(maze: Maze, current: Cell):
        path = []
        while current.parent:
            path.append(current)
            current = current.parent
        path.append(Cell(maze.starting_point[1], maze.starting_point[0]))
        path.reverse()
        return path
