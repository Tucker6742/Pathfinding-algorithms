from ..models.Cell import Cell
from ..models.Maze import Maze


class A_star_search:
    def search(maze: Maze):
        start: Cell = Cell(maze.starting_point[0], maze.starting_point[1])
        end: Cell = Cell(maze.ending_point[0], maze.ending_point[1])

        # queue: (g, h, f)
        # g: distance from start
        # h: heuristic to end
        # f: g + h
        with open("astar.txt", "w") as file:
            queue: dict[Cell:tuple[int, int, int]] = {}
            queue[start] = (0, A_star_search.heuristic(start, end),
                            A_star_search.heuristic(start, end))
            visited: list[Cell] = []

            while queue:
                current = queue.popitem()[0]
                file.write(
                    f"{current.parent}->{current}:{A_star_search.heuristic(current, end)}\n")
                file.write(f"{visited=}\n\n")
                visited.append(current)
                if current == end:
                    return A_star_search.reconstruct_path(maze, current)

                for neighbor in A_star_search.get_neighbors(maze, current):
                    if neighbor.coordinate() in map(Cell.coordinate, visited):
                        continue
                    if neighbor.coordinate() not in list(map(lambda x: x.coordinate, queue.keys())):
                        neighbor.setParent(current)
                        g = (neighbor.parent.cost + 1)
                        h = A_star_search.heuristic(neighbor, end)
                        f = g + h
                        queue[neighbor] = (g, h, f)
                    g = (neighbor.parent.cost + 1)
                    h = A_star_search.heuristic(neighbor, end)
                    f = g + h
                    if queue[neighbor][2] > f:
                        queue[neighbor] = (g, h, f)
                queue = A_star_search.sorted_dict(queue)
                file.write(f"{queue=}\n\n\n")
            return None, visited

    @staticmethod
    def sorted_dict(dict_point: dict[Cell:int]):
        return dict(sorted(list(dict_point.items()), key=lambda item: (item[1][2], item[1][1]), reverse=True))

    @staticmethod
    def get_neighbors(maze: Maze, cell: Cell):
        neighbors: list[Cell] = []
        x = cell.x
        y = cell.y
        if x < maze.width - 1:
            # right
            if maze.cells[y][x+1].status == 0:
                neighbors.append(maze.cells[y][x+1])
        if y > 0:
            # up
            if maze.cells[y-1][x].status == 0:
                neighbors.append(maze.cells[y-1][x])
        if y < maze.height - 1:
            # down
            if maze.cells[y+1][x].status == 0:
                neighbors.append(maze.cells[y+1][x])
        if x > 0:
            # left
            if maze.cells[y][x-1].status == 0:
                neighbors.append(maze.cells[y][x-1])
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
