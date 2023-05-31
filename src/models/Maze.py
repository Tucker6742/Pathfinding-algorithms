import random
from .Cell import Cell
random.seed(1)

class Maze:
    def __init__(self):
        self.width = 33
        self.height = 21
        self.cells = [[0]*self.width for i in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                self.cells[y][x] = Cell(x,y)
        #2D arrays are [heigt][width], so [0, 0] are actually [y, x]
        self.starting_point = [0, 0]
        self.ending_point = [19, 31]
    
    def changeStartingPoint(self,x,y):
        self.starting_point = [y, x]

    def changeEndingPoint(self,x,y):
        self.ending_point = [y, x]

    def randomizeMaze(self):
        self.createPath()
        self.batchChangeStatus()

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
                if self.x == 0:
                    try:
                        possible_moves.remove("w")
                    except:
                        pass
                if self.x == maze.width - 1:
                    try:
                        possible_moves.remove("e")
                    except:
                        pass
                if self.y == 0:
                    try:
                        possible_moves.remove("n")
                    except:
                        pass
                if self.y == maze.height - 1:
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
                # print(a.x,a.y)
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
                if self.cells[y][x].rank == 0:
                    self.cells[y][x].changeStatus(2)
                    continue
                else:
                    self.cells[y][x].changeStatus(0)
                    self.cells[y][x].changeRank(0)

    def randomizeMazeDepthFirst(self):
        def getVisitableCells(cells, x, y):
            visitable_cells = []
            try:
                if not cells[y-2][x-2].visited:
                    visitable_cells.append(cells[y-2][x-2])
            except:
                pass
            try:
                if not cells[y+2][x-2].visited:
                    visitable_cells.append(cells[y+2][x-2])
            except:
                pass
            try:
                if not cells[y-2][x+2].visited:
                    visitable_cells.append(cells[y-2][x+2])
            except:
                pass
            try:
                if  not cells[y+2][x+2].visited:
                    visitable_cells.append(cells[y+2][x+2])
            except:
                pass
        for y in range(self.height):
            for x in range(self).width:
                if x % 2 == 1 and y % 2 == 1:
                    self.cells[y][x].changeStatus(0)
                else:
                    self.cells[y][x].changeStatus(1)
        starting_cell = self.cells[self.starting_point[y]][self.starting_point[x]]
        
                


        
