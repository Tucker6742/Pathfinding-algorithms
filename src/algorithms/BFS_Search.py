from queue import Queue
from ..models.GoodCell import GoodCell
from ..models.GoodMaze import GoodMaze

class BFS_Search:
    def search(maze: GoodMaze):
        start: GoodCell = GoodCell(maze.getStart()[0], maze.getStart()[1])
        end: GoodCell = GoodCell(maze.getEnd()[0], maze.getEnd()[1])
        
        queue = Queue()
        queue.put(start)
        visited = set()
        visited.add(start.getCoordinates())
        parent = {}
        found = False

        while not queue.empty():
            current = queue.get()

            if current.getCoordinates() == end.getCoordinates():
                found = True
                break

            for neighbor in BFS_Search.get_neighbors(maze, current):
                if neighbor.getCoordinates() not in visited:
                    queue.put(neighbor)
                    visited.add(neighbor.getCoordinates())
                    parent[neighbor] = current

        if found:
            print("Found path by BFS")
            return BFS_Search.reconstruct_path(maze,end), list(visited)
        else:
            return None, list(visited)

    @staticmethod
    def get_neighbors(maze: GoodMaze, cell: GoodCell):
        neighbors = []
        (x, y) = cell.getCoordinates()

        if x < maze.getWidth() - 1 and maze.getCell(x + 1, y).getStatus() == 0:
            # right
            neighbors.append(maze.getCell(x + 1, y))
        if y > 0 and maze.getCell(x, y - 1).getStatus() == 0:
            # up
            neighbors.append(maze.getCell(x, y - 1))
        if y < maze.getHeight() - 1 and maze.getCell(x, y + 1).getStatus() == 0:
            # down
            neighbors.append(maze.getCell(x, y + 1))
        if x > 0 and maze.getCell(x - 1, y).getStatus() == 0:
            # left
            neighbors.append(maze.getCell(x - 1, y))

        return neighbors

    @staticmethod
    def reconstruct_path(maze: GoodMaze, cell: GoodCell):
        path = []
        while cell.getParent() is not None:
            path.append(cell.getCoordinates())
            cell = cell.getParent()
        path.append(maze.getStart())
        path.reverse()
        return path


