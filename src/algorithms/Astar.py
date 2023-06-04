from ..models.GoodCell import GoodCell
from ..models.GoodMaze import GoodMaze


class A_star_search:
    def search(maze: GoodMaze):
        start: GoodCell = GoodCell(
            maze.getStart()[0], maze.getStart()[1])
        end: GoodCell = GoodCell(maze.getEnd()[0], maze.getEnd()[1])
        # print(start.coordinate(), end.coordinate())
        # queue: (g, h, f)
        # g: distance from start
        # h: heuristic to end
        # f: g + h
        # with open("astar.txt", "w") as file:
        queue: dict[GoodCell:tuple[int, int, int]] = {}
        queue[start] = (0, A_star_search.heuristic(start, end),
                        A_star_search.heuristic(start, end))
        visited: list[GoodCell] = []
        while queue:
            current: GoodCell = queue.popitem()[0]
            visited.append(current)
            if current.getCoordinates() == end.getCoordinates():
                #print("Found path")
                return A_star_search.reconstruct_path(maze, current), visited

            for neighbor in A_star_search.get_neighbors(maze, current):
                if neighbor.getCoordinates() in map(GoodCell.getCoordinates, visited):
                    continue
                if neighbor.getCoordinates() not in list(map(lambda x: x.getCoordinates, queue.keys())):
                    neighbor.setParent(current)
                    new_node = True

                g = current.getRank() + 1
                h = A_star_search.heuristic(neighbor, end)
                f = g + h

                if new_node or queue[neighbor][2] > f:
                    neighbor.setRank(g)
                    queue[neighbor] = (g, h, f)
                    new_node = False
            queue = A_star_search.sorted_dict(queue)
        return None, visited

    @staticmethod
    def sorted_dict(dict_point: dict[GoodCell:int]):
        return dict(sorted(list(dict_point.items()), key=lambda item: (item[1][2], item[1][1]), reverse=True))

    @staticmethod
    def get_neighbors(maze: GoodMaze, cell: GoodCell):
        neighbors: list[GoodCell] = []
        x = cell.getCoordinates()[0]
        y = cell.getCoordinates()[1]
        if x <= maze.getWidth() - 2:
            # right
            if maze.getMaze()[x+1][y].getStatus() == 0:
                neighbors.append(maze.getMaze()[x+1][y])
        if y > 0:
            # down
            if maze.getMaze()[x][y-1].getStatus() == 0:
                neighbors.append(maze.getMaze()[x][y-1])
        if y <= maze.getHeight() - 2:
            # up
            if maze.getMaze()[x][y+1].getStatus() == 0:
                neighbors.append(maze.getMaze()[x][y+1])
        if x > 0:
            # left
            if maze.getMaze()[x-1][y].getStatus() == 0:
                neighbors.append(maze.getMaze()[x-1][y])
        return neighbors

    @staticmethod
    def heuristic(cell: GoodCell, end: GoodCell):
        return abs(cell.getCoordinates()[0] - end.getCoordinates()[0]) + abs(cell.getCoordinates()[1] - end.getCoordinates()[1])

    @staticmethod
    def reconstruct_path(maze: GoodMaze, current: GoodCell):
        path = []
        while current.getParent():
            path.append(current)
            current = current.getParent()
        path.append(GoodCell(maze.getStart()[0], maze.getStart()[1]))
        path.reverse()
        return path
