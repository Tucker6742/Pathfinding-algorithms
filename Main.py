import tkinter as tk
from src.models.GoodMaze import GoodMaze as Maze
from src.models.GoodCell import GoodCell as Cell
from src.algorithm.Dijkstra import Dijkstra as Dj

#Init window
window = tk.Tk()
window.geometry('1040x780+200+100')
window.resizable(False, False)
window.title("Maze Solver")
maze_frame = tk.Frame(window, bg = "#fff")
maze_frame.place(x = 25, y = 125, width = 990, height = 630)

#Init maze
maze = Maze()
maze.randomizeMaze()
#maze.randomizeMazeDepthFirst(maze.getStart())

Frames = []

for x in range(maze.getWidth()):
    for y in range(maze.getHeight()):
        if maze.getCell(x, y).getStatus() == 0:
            cell = tk.Frame(maze_frame, bg = "#ffffff", bd = 0, relief=tk.SOLID)
        elif maze.getCell(x, y).getStatus() == 1:
            cell = tk.Frame(maze_frame, bg = "#000000", bd = 0, relief=tk.SOLID)
        if maze.getCell(x, y).getCoordinates() == maze.getStart():
            cell.configure(bg = "#ED1C24")
        if maze.getCell(x, y).getCoordinates() == maze.getEnd():
            cell.configure(bg = "#ED1C24")
        cell.place(x = x*30, y = y*30, width = 30, height = 30)
        Frames.append(cell)


#Test dijkstra
#Create subwindow
subwindow = tk.Toplevel(window)
subwindow.geometry('1040x780+200+100')
subwindow.resizable(False, False)
subwindow.title("Dijkstra")
maze_frame = tk.Frame(subwindow, bg = "#fff")
maze_frame.place(x = 25, y = 125, width = 990, height = 630)

path = Dj.dijkstra(maze.getMaze(), maze.getStart(), maze.getEnd())

for frame in Frames:
    if (frame.winfo_rootx()//30, frame.winfo_rooty()//30) == maze.getStart():
        frame.configure(bg = "#ED1C24")



window.mainloop()