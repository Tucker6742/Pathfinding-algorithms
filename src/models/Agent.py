import random
class Agent:
    def __init__(self, x, y):
        #when init, x and y are the starting position of the maze
        self.__x = x
        self.__y = y
        self.__previous_direction = None

    def getCoordinates(self):
        return (self.__x, self.__y)

    def remember(self, previous_direction):
        self.__previous_direction = previous_direction

    def possibleMoves(self, maze):
        possible_moves = ["n","e","w","s"]
        if self.__previous_direction == "n":
            try:
                possible_moves.remove("s")
            except:
                pass
        if self.__previous_direction == "s":
            try:
                possible_moves.remove("n")
            except:
                pass
        if self.__previous_direction == "e":
            try:
                possible_moves.remove("w")
            except:
                pass
        if self.__previous_direction == "w":
            try:
                possible_moves.remove("e")
            except:
                pass
        if self.__x == 1:
            try:
                possible_moves.remove("w")
            except:
                pass
        if self.__x == maze.getWidth() - 2:
            try:
                possible_moves.remove("e")
            except:
                pass
        if self.__y == 1:
            try:
                possible_moves.remove("n")
            except:
                pass
        if self.__y == maze.getHeight() - 2:
            try:
                possible_moves.remove("s")
            except:
                pass
        return possible_moves

    def move(self, maze):
        cells = maze.getMaze()
        direction = random.sample(self.possibleMoves(maze), k = 1)[0]
        if direction == "n":
            self.__y -= 1
        if direction == "e":
            self.__x += 1
        if direction == "s":
            self.__y += 1
        if direction == "w":
            self.__x -= 1
        self.remember(direction)
