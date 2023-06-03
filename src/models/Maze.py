import random
from .Cell import Cell

class Maze:
    def __init__(self):
        self.width = 33
        self.height = 21
        self.cells = [[0]*self.width for i in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                self.cells[y][x] = Cell(x,y)
        #2D arrays are [heigt][width], so [0, 0] are actually [y, x]
        self.starting_point = [1, 1]
        self.ending_point = [19, 31]

    def setEnvironment(self):
        for y in range(1, self.height-1):
            for x in range(1, self.width-1):
                if self.cells[y-1][x].status == 1:
                    self.cells[y][x].environment['N'] = 1
                if self.cells[y+1][x].status == 1:
                    self.cells[y][x].environment['S'] = 1
                if self.cells[y][x-1].status == 1:
                    self.cells[y][x].environment['W'] = 1
                if self.cells[y][x+1].status == 1:
                    self.cells[y][x].environment['E'] = 1
    
    def changeStartingPoint(self,x,y):
        self.starting_point = [y, x]

    def changeEndingPoint(self,x,y):
        self.ending_point = [y, x]

    def randomizeMaze(self):
        self.createPath()
        self.batchChangeStatus()
        self.setEnvironment()

    def deletePath(self, starting_rank, ending_rank):
        for y in range(self.height):
            for x in range(self.width):
                if self.cells[y][x].rank > starting_rank and self.cells[y][x].rank <= ending_rank:
                    self.cells[y][x].changeRank(0)

    def createPath(self):
        class agent:
            def __init__(self, x, y):
                #when init, x and y are the starting position of the maze
                self.x = x
                self.y = y
                self.previous_direction = None

            def remember(self, previous_direction):
                self.previous_direction = previous_direction

            def possibleMoves(self, maze):
                possible_moves = ["n","e","w","s"]
                if self.previous_direction == "n":
                    try:
                        possible_moves.remove("s")
                    except:
                        pass
                if self.previous_direction == "s":
                    try:
                        possible_moves.remove("n")
                    except:
                        pass
                if self.previous_direction == "e":
                    try:
                        possible_moves.remove("w")
                    except:
                        pass
                if self.previous_direction == "w":
                    try:
                        possible_moves.remove("e")
                    except:
                        pass
                if self.x == 1:
                    try:
                        possible_moves.remove("w")
                    except:
                        pass
                if self.x == maze.width - 2:
                    try:
                        possible_moves.remove("e")
                    except:
                        pass
                if self.y == 1:
                    try:
                        possible_moves.remove("n")
                    except:
                        pass
                if self.y == maze.height - 2:
                    try:
                        possible_moves.remove("s")
                    except:
                        pass
                return possible_moves

            def move(self, maze):
                cells = maze.cells
                direction = random.sample(self.possibleMoves(maze), k = 1)[0]
                if direction == "n":
                    self.y -= 1
                if direction == "e":
                    self.x += 1
                if direction == "s":
                    self.y += 1
                if direction == "w":
                    self.x -= 1
                self.remember(direction)
        
        a = agent(self.starting_point[1], self.starting_point[0])
        self.cells[self.starting_point[1]][self.starting_point[0]].changeRank(1)
        rank_counter = 1
        while (True):
            a.move(self)
            if self.cells[a.y][a.x].rank == 0:
                rank_counter += 1
                self.cells[a.y][a.x].changeRank(rank_counter)
                if a.x == self.ending_point[1] and a.y == self.ending_point[0]:
                    break
                continue
            else:
                self.deletePath(self.cells[a.y][a.x].rank, rank_counter)
                rank_counter = self.cells[a.y][a.x].rank
                continue

    def batchChangeStatus(self):
        for y in range(self.height):
            for x in range(self.width):
                if x == 0 or y == 0 or x == (self.width - 1) or y == (self.height - 1):
                    self.cells[y][x].changeStatus(1)
                    continue
                if self.cells[y][x].rank == 0:
                    self.cells[y][x].changeStatus(2)
                    continue
                else:
                    self.cells[y][x].changeStatus(0)
                    self.cells[y][x].changeRank(0)

    def randomizeMazeDepthFirst(self):
        def getVisitableCells(maze, coordinate):
            cells = maze.cells
            [x,y] = coordinate
            visitable_cells = []
            if x - 2 >= 0 and cells[y][x-2].visited == 0:
                visitable_cells.append([x-2,y])
            if y - 2 >= 0 and cells[y-2][x].visited == 0:
                visitable_cells.append([x,y-2])
            if x + 2 < maze.width and cells[y][x+2].visited == 0:
                visitable_cells.append([x+2,y])
            if y + 2 < maze.height and cells[y+2][x].visited == 0:
                visitable_cells.append([x,y+2])
            return visitable_cells

        def createRandomPath(maze, current_coordinate):
            cells = maze.cells
            while True:
                visitable_cells = getVisitableCells(maze, current_coordinate)
                if not visitable_cells:
                    if backtrack(maze, current_coordinate, maze.starting_point) == 0:
                        return
                else:
                    child_coordinate = random.sample(visitable_cells,1)[0]
                    cells[child_coordinate[1]][child_coordinate[0]].visited = 1
                    cells[int((child_coordinate[1] + current_coordinate[1])/2)][int((child_coordinate[0]+current_coordinate[0])/2)].changeStatus(0)
                    cells[child_coordinate[1]][child_coordinate[0]].setParent(cells[current_coordinate[1]][current_coordinate[0]])
                    current_coordinate = child_coordinate

        def backtrack(maze, current_coordinate, starting_point):
            while True:
                visitable_cells = getVisitableCells(maze, current_coordinate)
                if not visitable_cells:
                    current_coordinate = [maze.cells[current_coordinate[1]][current_coordinate[0]].parent.x,maze.cells[current_coordinate[1]][current_coordinate[0]].parent.y]
                    if current_coordinate[1] == starting_point[1] and current_coordinate[0] == starting_point[0]:
                        return 0
                else:
                    createRandomPath(maze, current_coordinate)
            
        for y in range(self.height):
            for x in range(self.width):
                if x % 2 == 1 and y % 2 == 1:
                    self.cells[y][x].changeStatus(0)
                else:
                    self.cells[y][x].changeStatus(1)

        current_coordinate = [self.starting_point[0], self.starting_point[1]]
        self.cells[self.starting_point[1]][self.starting_point[0]].visited = 1
        createRandomPath(self, current_coordinate)
        self.setEnvironment()

    def westCell(maze, Cell):
        currentX, currentY = Cell.getCoordinates()
        searchingX = currentX - 1
        searchingY = currentY
        cell = maze.cells[searchingY][searchingX]
        return cell

    def southCell(maze, Cell):
        currentX, currentY = Cell.getCoordinates()
        searchingX = currentX 
        searchingY = currentY + 1
        cell = maze.cells[searchingY][searchingX]
        return cell
        
    def eastCell(maze, Cell):
        currentX, currentY = Cell.getCoordinates()
        searchingX = currentX + 1
        searchingY = currentY
        cell = maze.cells[searchingY][searchingX]
        return cell 
     
    def northCell(maze, Cell):
        currentX, currentY = Cell.getCoordinates()
        searchingX = currentX
        searchingY = currentY - 1
        cell = maze.cells[searchingY][searchingX]
        return cell
        
                


        
