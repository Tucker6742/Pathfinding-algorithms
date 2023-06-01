"""
Comsider maze as an 1D array of cells.
"""

from ..models.GoodCell import GoodCell as Cell 
from ..models.GoodMaze import GoodMaze as Maze



class My_Cell(Cell): 
    def __init__(self, 
                 x, 
                 y, 
                 status, 
                 visited, 
                 weight,
                 distance:float = float('inf')):
        """
        Add more element to Cell
        Parameters:
            distance: default infinity

        Consider each cell have infinite distance from start cell
        attributes:
        - distance : distance from neighbour cell to this cell (default infinity)
        
        method:
        - setDistance(distance): set distance
        - getDistance(): return distance
        """

        super().__init__(x, y, status, visited, weight)
        self.__distance = distance

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


class Dijkstra:
    """
    Dijkstra algorithm
    """
    def __init__(self):
        pass



    @staticmethod
    def dijkstra(maze : Maze, start : Cell, end : Cell) -> list[tuple]:
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
        for x in range(maze.getWidth()):
            for y in range(maze.getHeight()):
                maze.getMaze()[x][y] = My_Cell(x, 
                                               y, 
                                               maze.getCell(x, y).getStatus(),
                                               maze.getCell(x, y).isVisited(),
                                               maze.getCell(x, y).getWeight()
                                               )

        #Initialize distance of start to 0
        start.setDistance(0)
        start.setVisited(True) #Set start_cell to be visited

        #Initialize start_cells and path
        explored_path = []
        explored_path.append(start)
        start_cells = []
        start_cells.append(start)

        #Loop until all cells are visited
        while True:
            #Get distances to neighbors
            for cell in start_cells:
                for neighbor_cell in maze.getNeighbors(cell):
                    distance = cell.getDistance() + neighbor_cell.getWeight() #Get real distance to neighbor_cell
                    if neighbor_cell.isVisited() == False: #If neighbor_cell is not visited 
                        if neighbor_cell.getStatus() == 0: #If neighbor_cell is not wall
                            if neighbor_cell.getDistance() > distance: #Update distance
                                neighbor_cell.setDistance(distance)  
                                neighbor_cell.setParent(cell) #Connect this cell to start cell

            #If cell is end, break
            for cell in start_cells:
                if cell.getCoordinates() == end.getCoordinates():
                    """
                    Return path from start to end
                    """
                    path = []
                    end = cell
                    end.setVisited(True)
                    while end.isVisited() == True:
                        path.append(end)
                        if end.getParent().isVisited() == True:
                            end = end.getParent()
                        if end == start:
                            break
                    path.append(start)
                    path.reverse()
                    return explored_path, path

            #Clear all start_cells
            start_cells.clear() 
            
            #Decide next cell to start
            min_dist = float('inf')
            for x in range(maze.getWidth()):
                for y in range(maze.getHeight()):
                    #Find min distance in unvisited cells
                    cell = maze.getCell(x, y)
                    if cell.isVisited() == False and cell.getStatus() == 0 \
                        and min_dist > cell.getDistance():
                        min_dist = cell.getDistance()
            
            #Find all cells with min distance
            for x in range(maze.getWidth()):
                for y in range(maze.getHeight()):
                    cell = maze.getCell(x, y)
                    if cell.isVisited() == False and cell.getStatus() == 0 \
                        and cell.getDistance() == min_dist:
                        start_cells.append(cell)#Append chosen cell to new start
                        cell.setVisited(True)
                        explored_path.append(cell)
                    
            

                
        

            


        
        

