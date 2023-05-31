"""
Comsider maze as an 1D array of cells.
"""

import Cell.Cell #Assume there is a class called Cell
import Maze.Maze #Assume there is a class called Maze
from Dijkstra import Dijkstra


class DijkstraCell(Cell): #Inherit from Cell and add more attributes
    def __init__(self, 
                 x:int, 
                 y:int, 
                 state:int,
                 visited:bool = False, 
                 weight:int = 1,
                 distance:float = float('inf')):
        """
        Add more element to Cell
        Parameters:
            x: int
            y: int
            state: int (0:normal, 1:obstacle)
            visited: bool
            weight: int (default 1)
            distance: infinity


        Consider each cell as an object:
        attributes:
        - x: x coordinate
        - y: y coordinate
        - distance : distance from neighbour cell to this cell (default infinity)
        - state : state of cell (0: normal, 1: obstacle) 
        - visited: visited or not (default False)
        - previous: previous cell (default None)
        

        method:
        - setDistance(distance): set distance
        - setState(state): set state
        - getCoordinates(): return (x, y)
        - getDistance(): return distance
        - getWeight(): return weight
        - getState(): return state
        - getNeighbors(): return list of neighbors (list of cells with coordinates: 
                                        (x+1, y), 
                                        (x, y+1), 
                                        (x-1, y),
                                        (x, y-1),  
                                        )))
        - setVisited(state): set visited
        - isVisited(): return visited
        - setPrevious(previous): set previous
        - getPrevious(): return previous
        """

        super().__init__(x, y)
        self.__state = state
        self.__distance = distance
        self.__visited = visited
        self.__weight = weight
        self.__previous = None
        self.__visitlist = []

    def getCoordinates(self) -> tuple:
        """
        Return coordinate of cell
        """
        return (self._x, self._y)

    def getState(self) -> int:
        """
        Return state of cell
        """
        return self.__state

    def setDistance(self, distance) -> None:
        """
        Set distance of cell
        """
        self.__distance = distance

    def getDistance(self) -> int:
        """
        Return distance of cell
        """
        return self.__distance

    def getWeight(self) -> int:
        """
        Return weight of cell
        """
        return self.__weight

    def setVisited(self, state)->None:
        self.__visited = state

    def isVisited(self) -> bool:
        """
        Return visited of cell
        """ 
        return self.__visited

    def setVisitlist(self, visit_cell):
        self.__visitlist.append(visit_cell)

    def getVisitlist(self):
        return self.__visitlist

    def getNeighbors(self, maze_width, maze_height) -> list[tuple]:
        """
        Return coordinates of neighbors of this cell
        """
        neighbors = []

        if self.__x == 0: #Left edge
            if self.__y == 0: #Bottom left corner
                neighbors.append((self._x + 1, self._y))
                neighbors.append((self._x, self._y + 1))
            elif self.__y == maze_height - 1: #Top left corner
                neighbors.append((self._x, self._y - 1))
                neighbors.append((self._x + 1, self._y))
            else:
                neighbors.append((self._x, self._y - 1))
                neighbors.append((self._x + 1, self._y))
                neighbors.append((self._x, self._y + 1))

        elif self.__x == maze_width - 1: #Right edge
            if self.__y == 0: #Bottom right corner
                neighbors.append((self._x - 1, self._y))
                neighbors.append((self._x, self._y + 1))
            elif self.__y == maze_height - 1: #Top right corner
                neighbors.append((self._x, self._y - 1))
                neighbors.append((self._x - 1, self._y))
            else:
                neighbors.append((self._x, self._y - 1))
                neighbors.append((self._x - 1, self._y))
                neighbors.append((self._x, self._y + 1))
        
        else:
            if self.__y == 0: #Bottom edge
                neighbors.append((self._x + 1, self._y))
                neighbors.append((self._x - 1, self._y))
                neighbors.append((self._x, self._y + 1))
            elif self.__y == maze_height - 1: #Top edge
                neighbors.append((self._x + 1, self._y))
                neighbors.append((self._x - 1, self._y))
                neighbors.append((self._x, self._y - 1))
            else:
                neighbors.append((self._x + 1, self._y))
                neighbors.append((self._x - 1, self._y))
                neighbors.append((self._x, self._y + 1))
                neighbors.append((self._x, self._y - 1))

        return neighbors

    def setPrevious(self, previous_cell_coordinate) -> None:
        """
        Set previous cell
        """
        previous_cell = DijkstraCell.getCell(previous_cell_coordinate[0], 
                                             previous_cell_coordinate[1], 
                                             Maze.getMaze())
        self.__previous = previous_cell

    def getPrevious(self):
        """
        Return previous cell
        """
        return self.__previous

    @staticmethod
    def getCell(x:int, y:int, maze:list):
        for cell in maze:
            if cell.getCoordinates() == (x, y):
                dijkstra_cell = DijkstraCell(x = x, y = y, state = cell.getState(), distance = cell.getDistance())
                return dijkstra_cell


class Dijkstra:
    """
    Dijkstra algorithm
    """
    def __init__(self):
        pass


    @staticmethod
    def getPath(start : Cell, end : Cell) -> list[tuple]:
        """
        Return path from start to end
        """
        path = []
        print(end.isVisited())
        while end.isVisited() == True:
            print(end.getCoordinates())
            path.append(end.getCoordinates())
            end = end.getPrevious()
            
            if end == start:
                break
        path.append(start.getCoordinates())
        print(path)
        return path

    @staticmethod
    def dijkstra(maze : list, start : Cell, end : Cell) -> list[tuple]:
        """
        Finding shortest path from start to end using Dijkstra algorithm.
        Parameters:
            maze: 1D array of cells
            start: (x, y)
            end: (x, y)
        """

        #Get maze height and width
        position = []
        for cell in maze:
            position.append(cell.getCoordinates())

        maze_width = max(position)[0] + 1
        maze_height = max(position)[1] + 1

        #Initialize distance of start to 0
        start.setDistance(0)
        start.setVisited(True) #Set start_node to be visited


        #Initialize start_nodes and path
        path = []
        start_nodes = []
        start_nodes.append(start)


        #Loop until all nodes are visited
        count = 0
        while True:
            print(f'Loop : {count + 1}')
            #Get distances to neighbors
            for node in start_nodes:
                for neighbor in node.getNeighbors(maze_width, maze_height):
                    neighbor_node = Dijkstra.getCell(neighbor[0], neighbor[1], maze)
                    distance = node.getDistance() + neighbor_node.getWeight()
                    if neighbor_node.isVisited() == False and neighbor_node.getState() == 0\
                        and neighbor_node.getDistance() > distance:
                        neighbor_node.setDistance(node.getDistance() + neighbor_node.getWeight())
                        neighbor_node.setPrevious(node.getCoordinates())

            #Clear all start_nodes
            start_nodes.clear() 
            
            #Decide next node to start
            min_dist = float('inf')

            #Find min distance in unvisited nodes
            for node in maze:
                if node.isVisited() == False and neighbor_node.getState() == 0 \
                    and min_dist > node.getDistance():
                    min_dist = node.getDistance()

            #Find all nodes with min distance
            for node in maze:
                if node.isVisited() == False and neighbor_node.getState() == 0 \
                    and node.getDistance() == min_dist:
                    start_nodes.append(node)
                    node.setVisited(True)

            #If start_node is end, break
            print(f'start: {start.getCoordinates()}')
            print(f'end: {end.getCoordinates()}')
            for start_node in start_nodes:
                print(f'start_nodes: {start_node.getCoordinates()}')
            for start_node in start_nodes:
                if start_node == end:
                    return Dijkstra.getPath(start, end)

                
        

            


        
        

