import random
class GoodCell: 
    def __init__(self, 
                 x:int, 
                 y:int, 
                 status:int = 0,
                 visited:bool = False, 
                 weight:int = 1
                 ):
        """
        Represent a cell in maze
        Parameters:
            x: int
            y: int
            status: int (0:normal, 1:obstacle) (default 0)
            visited: bool
            weight: int (default 1) (indicate how many steps to move to this cell)

        Attributes:
        - x: x coordinate
        - y: y coordinate
        - state : state of cell (0: normal, 1: obstacle)
        - visited: visited or not (default False)
        - weight: weight of cell (default 1)
        - rank: rank of cell (default 0)
        - parent: parent cell (default None)
        

        Method:
        - setRank(rank): set rank  Don't know what this is for but Son use it to create maze
        - setState(state): set state
        - getState(): return state
        - getCoordinates(): return (x, y)
        - getWeight(): return weight
        - setVisited(state): set visited
        - isVisited(): return visited
        - setParent(parent): set parent_cell
        - getParent(): return parent_cell
        """

        self.__x = x
        self.__y = y
        self.__status = status
        self.__visited = visited
        self.__weight = weight
        self.__parent = None
        self.__rank = 0

    def setRank(self, rank):
        """
        Set rank of cell
        """
        self.__rank = rank

    def getRank(self):
        """
        Return rank of cell
        """
        return self.__rank

    def getCoordinates(self) -> tuple:
        """
        Return coordinate of cell
        """
        return (self.__x, self.__y)

    def setStatus(self, status):
        """
        Set state of cell
        """
        if status == 0 or status == 1:
            self.__status = status
        elif status == 2:
            self.__status = random.randint(0, 1)
        

    def getStatus(self) -> int:
        """
        Return state of cell
        """
        return self.__status

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

    def setParent(self, parent_cell) -> None:
        """
        Set parent cell
        """
        self.__parent = parent_cell

    def getParent(self):
        """
        Return parent cell
        """
        return self.__parent

    def __str__(self):
        return f"({self.__x}, {self.__y})"

    def __repr__(self):
        return f"({self.__x}, {self.__y})"
