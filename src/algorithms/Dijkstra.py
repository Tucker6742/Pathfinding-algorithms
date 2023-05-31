"""
Comsider maze as an 1D array of cells.
"""

from ..models.Cell import Cell #Assume there is a class called Cell
from ..models.Maze import Maze #Assume there is a class called Maze
from Dijkstra import Dijkstra


class My_Cell: 
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

        self.__x = x
        self.__y = y
        self.__state = state
        self.__distance = distance
        self.__visited = visited
        self.__weight = weight
        self.__previous = None

    def getCoordinates(self) -> tuple:
        """
        Return coordinate of cell
        """
        return (self.__x, self.__y)

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

    def getNeighbors(self, maze:Maze) -> list[tuple]:
        """
        Return neighbors of this cell
        """
        maze = Maze()
        neighbors = []
        for y in maze.height:
            for x in maze.width:
                if x == 0: #Left edge
                    if y == 0: #Bottom left corner
                        neighbors.append(My_Cell(x + 1, y, maze[y][x].status))
                        neighbors.append(My_Cell(x, y + 1, maze[y][x].status))
                    elif y == maze.height - 1: #Top left corner
                        neighbors.append(My_Cell(x, y - 1, maze[y][x].status))
                        neighbors.append(My_Cell(x + 1, y, maze[y][x].status))
                    else:
                        neighbors.append(My_Cell(x, y - 1, maze[y][x].status))
                        neighbors.append(My_Cell(x + 1, y, maze[y][x].status))
                        neighbors.append(My_Cell(x, y + 1, maze[y][x].status))

                elif x == maze.width - 1: #Right edge
                    if y == 0: #Bottom right corner
                        neighbors.append(My_Cell(x - 1, y, maze[y][x].status))
                        neighbors.append(My_Cell(x, y + 1, maze[y][x].status))
                    elif y == maze.height - 1: #Top right corner
                        neighbors.append(My_Cell(x, y - 1, maze[y][x].status))
                        neighbors.append(My_Cell(x - 1, y, maze[y][x].status))
                    else:
                        neighbors.append(My_Cell(x, y - 1, maze[y][x].status))
                        neighbors.append(My_Cell(x - 1, y, maze[y][x].status))
                        neighbors.append(My_Cell(x, y + 1, maze[y][x].status))
        
                else:
                    if y == 0: #Bottom edge
                        neighbors.append(My_Cell(x + 1, y, maze[y][x].status))
                        neighbors.append(My_Cell(x - 1, y, maze[y][x].status))
                        neighbors.append(My_Cell(x, y + 1, maze[y][x].status))
                    elif y == maze.height - 1: #Top edge
                        neighbors.append(My_Cell(x + 1, y, maze[y][x].status))
                        neighbors.append(My_Cell(x - 1, y, maze[y][x].status))
                        neighbors.append(My_Cell(x, y - 1, maze[y][x].status))
                    else:
                        neighbors.append(My_Cell(x + 1, y, maze[y][x].status))
                        neighbors.append(My_Cell(x - 1, y, maze[y][x].status))
                        neighbors.append(My_Cell(x, y + 1, maze[y][x].status))
                        neighbors.append(My_Cell(x, y - 1, maze[y][x].status))

        return neighbors

    def setPrevious(self, previous_cell) -> None:
        """
        Set previous cell
        """
        self.__previous = previous_cell

    def getPrevious(self):
        """
        Return previous cell
        """
        return self.__previous



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
        path.reverse()
        print(path)
        return path

    def dijkstra(maze : list, start : Cell, end : Cell) -> list[tuple]:
        """
        Finding shortest path from start to end using Dijkstra algorithm.
        Parameters:
            maze: 1D array of cells
            start: (x, y)
            end: (x, y)

        All cells except start are set distance of infinity.
        Weight will be added to distance of each cell when visit that cell.
        """

        #Convert to my maze and my cells
        bruh_maze = Maze()
        maze = []
        for y in bruh_maze.height:
            for x in bruh_maze.width:
                maze.append(My_Cell(x, y, maze[y][x].status))

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
                for neighbor_node in node.getNeighbors(maze_width, maze_height):
                    distance = node.getDistance() + neighbor_node.getWeight() #Get real distance to neighbor_node
                    if neighbor_node.isVisited() == False: #If neighbor_node is not visited 
                        if neighbor_node.getState() == 0: #If neighbor_node is not wall
                            if neighbor_node.getDistance() > distance: #Update distance
                                neighbor_node.setDistance(distance)  
                                neighbor_node.setPrevious(node) #Connect this node to start node

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
            #print(f'start: {start.getCoordinates()}')
            #print(f'end: {end.getCoordinates()}')
            #for start_node in start_nodes:
            #    print(f'start_nodes: {start_node.getCoordinates()}')
            for start_node in start_nodes:
                if start_node == end:
                    return Dijkstra.getPath(start, end)

                
        

            


        
        

