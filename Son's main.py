import tkinter as tk
from src.models.Maze import Maze
from src.algorithms.Astar import A_star_search
from src.algorithms.gbfs import greedy_best_first_search
from src.algorithms.Dfs import dfs
from src.algorithms.Dijkstra import Dijkstra
window = tk.Tk()
window.geometry('1040x780+200+100')
window.resizable(False, False)
maze_frame = tk.Frame(window, bg = "#fff")
maze_frame.place(x = 25, y = 125, width = 990, height = 630)
maze = Maze()
for coordinate_y in range(maze.height):
    for coordinate_x in range(maze.width):
        cell = tk.Frame(maze_frame, bg = "#000000", bd = 0, relief=tk.SOLID)
        if maze.cells[coordinate_y][coordinate_x].x == maze.starting_point[1] and maze.cells[coordinate_y][coordinate_x].y == maze.starting_point[0]:
            cell.configure(bg = "#ED1C24")
        if maze.cells[coordinate_y][coordinate_x].x == maze.ending_point[1] and maze.cells[coordinate_y][coordinate_x].y == maze.ending_point[0]:
            cell.configure(bg = "#ED1C24")
        cell.place(x = maze.cells[coordinate_y][coordinate_x].x*30, y = maze.cells[coordinate_y][coordinate_x].y*30, width = 30, height = 30)
#maze.randomizeMaze()
maze.randomizeMazeDepthFirst()
for widget in maze_frame.winfo_children():
    widget.destroy()
for coordinate_y in range(maze.height):
    for coordinate_x in range(maze.width):
        if maze.cells[coordinate_y][coordinate_x].status == 0:
            cell = tk.Frame(maze_frame, bg = "#ffffff", bd = 1, relief=tk.SOLID)
        elif maze.cells[coordinate_y][coordinate_x].status == 1:
            cell = tk.Frame(maze_frame, bg = "#000000", bd = 0, relief=tk.SOLID)
        if maze.cells[coordinate_y][coordinate_x].x == maze.starting_point[1] and maze.cells[coordinate_y][coordinate_x].y == maze.starting_point[0]:
            cell.configure(bg = "#ED1C24")
        if maze.cells[coordinate_y][coordinate_x].x == maze.ending_point[1] and maze.cells[coordinate_y][coordinate_x].y == maze.ending_point[0]:
            cell.configure(bg = "#ED1C24")
        cell.place(x = maze.cells[coordinate_y][coordinate_x].x*30, y = maze.cells[coordinate_y][coordinate_x].y*30, width = 30, height = 30)
#window.mainloop()
(y_start, x_start) = maze.starting_point
(y_end, x_end) = maze.ending_point

best_path, explored_path  = Dijkstra.dijkstra(maze, maze.cells[y_start][x_start], maze.cells[y_end][x_end])
print(best_path)

