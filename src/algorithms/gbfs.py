from ..models.GoodCell import GoodCell
from ..models.GoodMaze import GoodMaze


class greedy_best_first_search:
    def search(maze: GoodMaze):
        start: GoodCell = GoodCell(maze.getStart()[0], maze.getStart()[1])
        end: GoodCell = GoodCell(maze.getEnd()[0], maze.getEnd()[1])
        # print(start.getCoordinates(), end.getCoordinates())
        # queue: (h)
        # h: heuristic to end
        queue: dict[GoodCell:tuple[int]] = {}
        queue[start] = greedy_best_first_search.heuristic(start, end)
        visited: list[GoodCell] = []

        while queue:
            current = queue.popitem()[0]
            visited.append(current)
            if current.getCoordinates() == end.getCoordinates():
                #print("Found path by greedy best first search")
                return greedy_best_first_search.reconstruct_path(maze, current), visited

            for neighbor in greedy_best_first_search.get_neighbors(maze, current):
                if neighbor.getCoordinates() in map(GoodCell.getCoordinates, visited):
                    continue
                if neighbor.getCoordinates() not in list(map(lambda x: x.getCoordinates(), queue.keys())):
                    neighbor.setParent(current)
                    new_node = True

                if new_node:
                    queue[neighbor] = greedy_best_first_search.heuristic(neighbor, end)
                    new_node = False

            queue = greedy_best_first_search.sorted_dict(queue)
        return None, visited
    
    @staticmethod
    def sorted_dict(dict_point: dict[GoodCell:int]):
        return dict(sorted(list(dict_point.items()), key=lambda item: item[1], reverse=True))
    
    @staticmethod
    def get_neighbors(maze: GoodMaze, cell: GoodCell):
        neighbors: list[GoodCell] = []
        (x, y) = cell.getCoordinates()
        if x < maze.getWidth() - 1:
            # right
            if maze.getCell(x+1, y).getStatus() == 0:
                neighbors.append(maze.getCell(x+1, y))
        if y > 0:   
            # up
            if maze.getCell(x, y-1).getStatus() == 0:
                neighbors.append(maze.getCell(x, y-1))
        if y < maze.getHeight() - 1:
            # down
            if maze.getCell(x, y+1).getStatus() == 0:
                neighbors.append(maze.getCell(x, y+1))
        if x > 0:
            # left
            if maze.getCell(x-1, y).getStatus() == 0:
                neighbors.append(maze.getCell(x-1, y))
        return neighbors
        
    
    
    @staticmethod
    def heuristic(cell: GoodCell, end: GoodCell):
        return abs(cell.getCoordinates()[0] - end.getCoordinates()[0]) + abs(cell.getCoordinates()[1] - end.getCoordinates()[1])
    
    @staticmethod
    def reconstruct_path(maze: GoodMaze, cell: GoodCell):
        path = []
        while cell.getParent() is not None:
            path.append(cell.getCoordinates())
            cell = cell.getParent()
        path.append(maze.getStart())
        path.reverse()
        return path
