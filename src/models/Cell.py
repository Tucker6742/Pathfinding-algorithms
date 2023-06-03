import random
class Cell:
    #x, y are coordinates of the cell
    #status at 1 represents a wall, 0 represents a non-wall
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = None
        self.rank = 0
        self.visited = 0
        self.parent = None
        self.cost = 0
        self.environment = {
            'E': 0,
            'S': 0,
            'N': 0,
            'W': 0
        }
        self.ispath = 0
        self.passpath = 0

    def changeStatus(self, status):
        if status == 0 or status == 1:
            self.status = status
        elif status == 2:
            self.status = random.randint(0,1)

    def changeRank(self, rank):
        self.rank = rank

    def setParent(self, parent_cell):
        self.parent = parent_cell

    def __repr__(self):
        return f"Cell({self.y}, {self.x})"
    
    # @staticmethod
    def coordinate(self):
        return (self.y, self.x)

    def getCoordinates(self):
        return (self.x, self.y)
    
    