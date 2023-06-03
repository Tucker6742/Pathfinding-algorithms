from collections import OrderedDict
from ..models.GoodCell import GoodCell
from ..models.GoodMaze import GoodMaze
class BFS_Search:
    def search(maze: GoodMaze):
        start: GoodCell = GoodCell(maze.getStart()[0], maze.getStart()[1])
        end: GoodCell = GoodCell(maze.getEnd()[0], maze.getEnd()[1])
        queue: dict[GoodCell:tuple[int, int, int]] = OrderedDict()
        queue[start] = (0, 0, 0)  
        visited: list[GoodCell] = []
        visited.append(start)
        found = False

        while queue:
            current: GoodCell = next(iter(queue))
            del queue[current]

            if current.getCoordinates() == end.getCoordinates():
                found = True
                break

            for neighbor in BFS_Search.get_neighbors(maze, current):
                if neighbor not in visited:
                    queue[neighbor] = (0, 0, 0)  
                    visited.append(neighbor)
                    neighbor.setParent(current)

        if found:
            print("Found path by BFS")
            visited_sorted = sorted(list(map(GoodCell.getCoordinates, visited)))
            return BFS_Search.reconstruct_path(maze, current), visited_sorted
        else:
            visited_sorted = sorted(list(map(GoodCell.getCoordinates, visited)))
            return None, visited_sorted

    @staticmethod
    def get_neighbors(maze: GoodMaze, cell: GoodCell):
        neighbors: list[GoodCell] = []
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
