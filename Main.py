import tkinter as tk
from src.models.GoodMaze import GoodMaze as Maze
from src.models.GoodCell import GoodCell as Cell
from src.algorithms.Astar import A_star_search
from src.algorithms.gbfs import greedy_best_first_search
from src.algorithms.BFS_Search import BFS_Search
from src.algorithms.Dijkstra import Dijkstra
from src.algorithms.Dfs import dfs
import time



#Init window
window = tk.Tk()
window.geometry('1040x780+200+100')
window.resizable(False, False)
window.title("Maze Solver")
maze_frame = tk.Frame(window, bg = "#fff")
maze_frame.place(x = 25, y = 125, width = 990, height = 630)

#Init maze using random maze generator
maze = Maze()
for x in range(maze.getWidth()):
    for y in range(maze.getHeight()):
        cell = tk.Frame(maze_frame, bg = "#000000", bd = 0, relief=tk.SOLID)
        if maze.getCell(x, y).getCoordinates() == maze.getStart():
            cell.configure(bg = "#ED1C24")
        if maze.getCell(x, y).getCoordinates() == maze.getEnd():
            cell.configure(bg = "#ED1C24")
        cell.place(x = x*30, y = y*30, width = 30, height = 30)
#maze.randomizeMaze()
maze.randomizeMazeDepthFirst(maze.getStart())
maze.setEnvironment()
for widget in maze_frame.winfo_children():
    widget.destroy()

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

window.mainloop()

start = time.time()
path,visited_sorted = A_star_search.search(maze)
end = time.time()
print(f'A*: {end - start} milisec')

start = time.time()
path,visited_sorted = greedy_best_first_search.search(maze)
end = time.time()
print(f'GBFS: {end - start} milisec')

start = time.time()
path,visited_sorted = dfs(maze)
end = time.time()
print(f'DFS: {end - start} milisec')


(x_start, y_start) = maze.getStart()
(x_end, y_end) = maze.getEnd()
start = time.time()
best_path, explored_path  = Dijkstra.dijkstra(maze, maze.getCell(x_start, y_start), maze.getCell(x_end, y_end))
end = time.time()
print(f'dijkstra: {end - start} milisec')

start = time.time()
path,visited_sorted = BFS_Search.search(maze)
end = time.time()
print(f'BFS: {end - start} milisec')



