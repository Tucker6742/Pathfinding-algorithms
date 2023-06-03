import random
from .GoodCell import GoodCell as Cell
from .Agent import Agent


class GoodMaze:
    """
    Represent a maze
    Parameters:
        width: int
    height: int
    start: tuple (x, y)
    end: tuple (x, y)

    Attributes:
        __width: int
        __height: int
        __cells: list[list[Cell]]
        __start: tuple (x, y)
        __end: tuple (x, y)

    Methods:
        setStart(x, y) -> None
        setEnd(x, y) -> None
        getMaze() -> list[list[Cell]]
        getNeighbors(cell) -> list[tuple]
        other for random maze generation
    """
    def __init__(self, width = 33, height = 21):
        self.__width = width
        self.__height = height
        self.__cells = [[0]*self.__height for i in range(self.__width)]

        for x in range(self.__width):
            for y in range(self.__height):
                self.__cells[x][y] = Cell(x, y)

        self.__start = (1, 1)
        self.__end = (31, 19)
        self.walls = []
        self.paths = []
        self.rank = 0
    
    def setEnvironment(self):
        for x in range(1, self.__width-1):
            for y in range(1, self.__height-1):
                if self.__cells[x][y-1].getStatus() == 1:
                    self.__cells[x][y].environment['N'] = 1
                if self.__cells[x][y+1].getStatus() == 1:
                    self.__cells[x][y].environment['S'] = 1
                if self.__cells[x-1][y].getStatus() == 1:
                    self.__cells[x][y].environment['W'] = 1
                if self.__cells[x+1][y].getStatus() == 1:
                    self.__cells[x][y].environment['E'] = 1

    
    def setStart(self, x, y):
        self.__start = (x, y)

    def setEnd(self, x, y):
        self.__end = (x, y)

    def getStart(self):
        return self.__start

    def getEnd(self):
        return self.__end

    def getHeight(self):
        return self.__height

    def getWidth(self):
        return self.__width

    def getCell(self, x_coordinate, y_coordinate) -> Cell:
        return self.__cells[x_coordinate][y_coordinate]

    def getMaze(self):
        return self.__cells

    def getNeighbors(self, cell: Cell) -> list[tuple]:
        """
        Return neighbors of this cell
        """
        neighbors = []
        (x, y) = cell.getCoordinates()
        if x < self.__width - 2:
            if self.__cells[x+1][y].getStatus() == 0:
                neighbors.append(self.__cells[x+1][y])

        if x > 0:
            if self.__cells[x-1][y].getStatus() == 0:
                neighbors.append(self.__cells[x-1][y])

        if y < self.__height - 2:
            if self.__cells[x][y+1].getStatus() == 0:
                neighbors.append(self.__cells[x][y+1])

        if y > 0:
            if self.__cells[x][y-1].getStatus() == 0:
                neighbors.append(self.__cells[x][y-1])

        return neighbors

    def randomizeMaze(self):
        self.createPath()
        self.batchChangeStatus()
        self.setEnvironment()

    def deletePath(self, starting_rank, ending_rank):
        for x in range(self.__width):
            for y in range(self.__height):
                if self.__cells[x][y].getRank() > starting_rank and self.__cells[x][y].getRank() <= ending_rank:
                    # print(f'This cell {(x, y)} has rank:{self.__cells[x][y].getRank()} need to be changed')
                    self.__cells[x][y].setRank(0)
                    self.walls.append(self.__cells[x][y])

    def createPath(self):
        a = Agent(self.__start[0], self.__start[1])
        self.__cells[self.__start[0]][self.__start[1]].setRank(1)
        rank_counter = 1
        while True:
            a.move(self)
            # print(f'a:{a.getCoordinates()}, rank a before:{self.__cells[a.getCoordinates()[0]][a.getCoordinates()[1]].getRank()}')
            if self.__cells[a.getCoordinates()[0]][a.getCoordinates()[1]].getRank() == 0:
                rank_counter += 1
                
                self.__cells[a.getCoordinates()[0]][a.getCoordinates()[1]].setRank(rank_counter)
                
                #print(f'rank a after:{self.__cells[a.getCoordinates()[0]][a.getCoordinates()[1]].getRank()}')
                #print(f'a:{a.getCoordinates()},  end:{self.__end}')
                if a.getCoordinates() == self.__end:
                    for i in range(1, rank_counter):
                        for x in range(self.__width):
                            for y in range(self.__height):
                                if self.__cells[x][y].getRank() == i:
                                   self.paths.append(self.__cells[x][y])
                    #print('Found')
                    break
                continue
            else:
                self.deletePath(self.__cells[a.getCoordinates()[
                                0]][a.getCoordinates()[1]].getRank(), rank_counter)
                rank_counter = self.__cells[a.getCoordinates()[0]][a.getCoordinates()[
                    1]].getRank()
                continue

    def batchChangeStatus(self):
        for x in range(self.__width):
            for y in range(self.__height):
                if x == 0 or y == 0 or x == (self.__width - 1) or y == (self.__height - 1):
                    self.__cells[x][y].setStatus(1)
                    continue
                if self.__cells[x][y].getRank() == 0:
                    self.__cells[x][y].setStatus(2)
                    continue
                else:
                    self.__cells[x][y].setStatus(0)
                    self.__cells[x][y].setRank(0)

    def randomizeMazeDepthFirst(self, current_coordinate, init=False, create_path=True):

        # Initialize the maze
        if init == False:
            for x in range(self.__width):
                for y in range(self.__height):
                    if x % 2 == 1 and y % 2 == 1:  # Set all cells not edge to be normal
                        self.__cells[x][y].setStatus(0)
                        self.__cells[x][y].setRank(0)
                        self.paths.append(self.__cells[x][y])
                            #self.paths.append(self.__cells[x][y])
                    else:
                        self.__cells[x][y].setStatus(1)
                    
                        
            self.__cells[self.__start[0]][self.__start[1]].setVisited(True)
            init = True
            self.randomizeMazeDepthFirst(self.__start, init, create_path)

        # If create_path is True, create a path from start to end
        if create_path == True:
            cells = self.__cells
            (x, y) = current_coordinate
            # Get all visitable cells
            visitable_cells = []
            if x - 2 >= 0 and cells[x-2][y].isVisited() == False:
                visitable_cells.append((x-2, y))
            if y - 2 >= 0 and cells[x][y-2].isVisited() == False:
                visitable_cells.append((x, y-2))
            if x + 2 < self.__width and cells[x+2][y].isVisited() == False:
                visitable_cells.append((x+2, y))
            if y + 2 < self.__height and cells[x][y+2].isVisited() == False:
                visitable_cells.append((x, y+2))

            # If there are no visitable cells, backtracking
            if not visitable_cells:
                # If the current cell is the start cell, return
                if current_coordinate == self.__start:
                    return
                # Backtrack to the parent cell
                current_coordinate = cells[x][y].getParent().getCoordinates()
                self.randomizeMazeDepthFirst(
                    current_coordinate, init, create_path)

            # If there are visitable cells, randomly choose one and create a path
            else:
                child_coordinate = random.sample(visitable_cells, 1)[0]
                (x_child, y_child) = child_coordinate
                # Visit the child cell and set the wall between the child cell and the current cell to be normal cell
                cells[x_child][y_child].setVisited(True)
                cells[int((x_child + x)/2)][int((y_child+y)/2)].setStatus(0)

                self.rank += 1
                cells[int((x_child + x)/2)][int((y_child+y)/2)].setRank(self.rank)
                cells[x_child][y_child].setRank(self.rank + 1)
                self.paths.append(cells[int((x_child + x)/2)][int((y_child+y)/2)])
                self.paths.append(cells[x_child][y_child])
                #Set the parent of the child cell to be the current cell
                cells[x_child][y_child].setParent(cells[x][y])
                # Set the current cell to be the child cell
                current_coordinate = child_coordinate
                self.randomizeMazeDepthFirst(current_coordinate, init, create_path)
        #self.setEnvironment()
    
    def westCell(maze, Cell):
        currentX, currentY = Cell.getCoordinates()
        searchingX = currentX - 1
        searchingY = currentY
        cell = maze.getCell(searchingX, searchingY)
        return cell

    def southCell(maze, Cell):
        currentX, currentY = Cell.getCoordinates()
        searchingX = currentX 
        searchingY = currentY + 1
        cell = maze.getCell(searchingX, searchingY)
        return cell
        
    def eastCell(maze, Cell):
        currentX, currentY = Cell.getCoordinates()
        searchingX = currentX + 1
        searchingY = currentY
        cell = maze.getCell(searchingX, searchingY)
        return cell 
     
    def northCell(maze, Cell):
        currentX, currentY = Cell.getCoordinates()
        searchingX = currentX
        searchingY = currentY - 1
        cell = maze.getCell(searchingX, searchingY)
        return cell

             

        
                


        

