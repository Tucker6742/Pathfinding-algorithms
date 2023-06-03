from tkinter import BUTT
import pygame
from pygame.locals import *
from .Button import Button

from src.models.GoodCell import GoodCell as Cell
from src.models.GoodMaze import GoodMaze as Maze
#from src.Visualize.DropDown import DropDown
from src.algorithms.Astar import A_star_search
from src.algorithms.Dijkstra import Dijkstra
from src.algorithms.BFS_Search import BFS_Search
from src.algorithms.Dfs import dfs
from src.algorithms.gbfs import greedy_best_first_search





#Set clock
clock = pygame.time.Clock()



def startDrawMaze(draw_maze, draw_maze_event):
    if draw_maze == True:
        pygame.time.set_timer(draw_maze_event, 10)
    else:
        pygame.time.set_timer(draw_maze_event, 0)

def drawMaze(screen, maze, path, cell_size):
    width, height = pygame.display.get_surface().get_size()
    (x, y) = path.getCoordinates()
    cell = pygame.Rect(x*cell_size + (width - maze.getWidth()*cell_size)/2, y*cell_size + (height - maze.getHeight()*cell_size)/2, cell_size, cell_size)

    pygame.draw.rect(screen, 'white', cell)

    if (x, y) == maze.getStart() or (x, y) == maze.getEnd():
        pygame.draw.rect(screen, 'red', cell)

    pygame.display.update(cell)


def startSolve(draw_solve, draw_event):
    if draw_solve == True:
        pygame.time.set_timer(draw_event, 10)
    else:
        pygame.time.set_timer(draw_event, 0)

def drawExplored(screen, maze, path, cell_size):
    width, height = pygame.display.get_surface().get_size()
    (x, y) = path.getCoordinates()
    cell = pygame.Rect(x*cell_size + (width - maze.getWidth()*cell_size)/2, y*cell_size + (height - maze.getHeight()*cell_size)/2, cell_size, cell_size)

    pygame.draw.rect(screen, 'blue', cell)
    if (x, y) == maze.getStart() or (x, y) == maze.getEnd():
        pygame.draw.rect(screen, 'red', cell)
    pygame.display.update(cell)

def drawSolve(screen, maze, path, cell_size):
    width, height = pygame.display.get_surface().get_size()
    (x, y) = path.getCoordinates()
    cell = pygame.Rect(x*cell_size + (width - maze.getWidth()*cell_size)/2, y*cell_size + (height - maze.getHeight()*cell_size)/2, cell_size, cell_size)

    pygame.draw.rect(screen, 'green', cell)
    if (x, y) == maze.getStart() or (x, y) == maze.getEnd():
        pygame.draw.rect(screen, 'red', cell)
    pygame.display.update(cell)


def getMazeInfo():
    maze = Maze(55, 31)
    maze.randomizeMazeDepthFirst(maze.getStart())
    walls = maze.walls
    paths = maze.paths
    
    paths.sort(key = lambda x: x.getRank())

    return maze, paths, walls

def main():

    #Create maze
    maze = Maze()
    #maze.randomizeMazeDepthFirst(maze.getStart())
    #maze.setStart(1, 1)
    #maze.setEnd(31, 19)
    #maze.randomizeMaze()


    #Set up the drawing window
    width = 1280 
    height = 720
    


    


    pygame.init()

    button_list = []

    #Create stop button
    stop_button = Button(40, 40, 80, 60, color = '#b5d9eb', text = 'Stop', font_size = 32)
    button_list.append(stop_button)

    #Create randomaze button
    randomaze_button = Button(200, 40, 120, 60, color = '#b5d9eb', text = 'Randomaze', font_size = 32)
    button_list.append(randomaze_button)

    #Create menu button------------------------------------------------------------------------------
    menu_button = Button(40, 120, 90, 40,color = '#5be364', text = 'Menu', font_size = 32)
    button_list.append(menu_button)

    menu_list = ['A*', 'Dijkstra', 'BFS', 'DFS', 'Greedy']
    menu_item_color = '#f4f5e9'
    #Create Astar button
    astar_button = Button(40, 160, 120, 60, color = menu_item_color, text = 'A*', text_color = 'black', font_size = 32)
    button_list.append(astar_button)
    #Create Dijkstra button
    dijkstra_button = Button(40, 220, 120, 60, color = menu_item_color, text = 'Dijkstra', text_color = 'black', font_size = 32)
    button_list.append(dijkstra_button)
    #Create BFS button
    bfs_button = Button(40, 280, 120, 60, color = menu_item_color, text = 'BFS', text_color = 'black', font_size = 32)
    button_list.append(bfs_button)
    #Create DFS button
    dfs_button = Button(40, 340, 120, 60, color = menu_item_color, text = 'DFS', text_color = 'black', font_size = 32)
    button_list.append(dfs_button)
    #Create Greedy button
    greedy_button = Button(40, 400, 120, 60, color = menu_item_color, text = 'Greedy', text_color = 'black', font_size = 32)
    button_list.append(greedy_button)
    #------------------------------------------------------------------------------------------------
    
    

    
    # Variable to keep our game loop running
    gameOn = True
    draw_maze = False
    draw_maze_surface = True
    draw_solve = False
    solve = False
    solve_astar = False
    solve_dijkstra = False
    solve_bfs = False
    solve_dfs = False
    solve_greedy = False
    
    

    #Create event to draw maze
    draw_maze_event = pygame.USEREVENT + 1

    #Create event to draw solution
    draw_dijkstra_event = pygame.USEREVENT + 2
    draw_astar_event = pygame.USEREVENT + 3
    draw_bfs_event = pygame.USEREVENT + 4
    draw_dfs_event = pygame.USEREVENT + 5
    draw_greedy_event = pygame.USEREVENT + 6

    #Init screen
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Pathfinding Visualizer')
    screen.fill('#dceef7')

    # Our game loop
    while gameOn:

        #Get paths and walls
        if draw_maze_surface == True:
            maze, paths, walls = getMazeInfo()
            cell_size = 33/maze.getWidth() * 20
            maze_surf = pygame.Surface((maze.getWidth()*cell_size, maze.getHeight()*cell_size))
            maze_surf.fill('black')
            screen.blit(maze_surf, ((width - maze.getWidth()*cell_size)/2, (height - maze.getHeight()*cell_size)/2))
            draw_maze_surface = False

            solve = True
            

        #Get solve
        if solve == True:
            if solve_astar == True:
                #A*
                best_path_astar, explored_path_astar = A_star_search.search(maze)
                solve_astar = False
            elif solve_dijkstra == True:
                #Dijkstra
                (x_start, y_start) = maze.getStart()
                (x_end, y_end) = maze.getEnd()
                best_path_dijkstra, explored_path_dijkstra  = Dijkstra.dijkstra(maze, maze.getCell(x_start, y_start), maze.getCell(x_end, y_end))
                solve_dijkstra = False
            elif solve_bfs == True:
                #Bfs
                best_path_bfs, explored_path_bfs = BFS_Search.search(maze)
                solve_bfs = False
            elif solve_dfs == True:
                #Dfs
                best_path_dfs, explored_path_dfs = dfs(maze)
                solve_dfs = False
            elif solve_greedy == True:
                #Greedy
                best_path_greedy, explored_path_greedy = greedy_best_first_search.search(maze)
                solve_greedy = False


            solve = False


        mouse_x, mouse_y = pygame.mouse.get_pos()
        event_list = pygame.event.get()
        # for loop through the event queue
        for event in event_list:
            # Check for QUIT event
            if event.type == QUIT:
                pygame.quit()

            # Check for MOUSEBUTTONDOWN event
            elif event.type == MOUSEBUTTONDOWN:
                for button in button_list:
                    if button.rect.collidepoint((mouse_x, mouse_y)):
                        if button.text == 'Randomaze':
                            draw_maze = True
                            pygame.event.clear()
                            startDrawMaze(draw_maze, draw_maze_event)
                        elif button.text == 'A*':
                            solve_astar = True
                            draw_solve = True
                            pygame.event.clear()
                            startSolve(draw_solve, draw_astar_event)
                        elif button.text == 'Dijkstra':
                            solve_dijkstra = True
                            draw_solve = True
                            pygame.event.clear()
                            startSolve(draw_solve, draw_dijkstra_event)
                        elif button.text == 'BFS':
                            solve_bfs = True
                            draw_solve = True
                            pygame.event.clear()
                            startSolve(draw_solve, draw_bfs_event)
                        elif button.text == 'DFS':
                            solve_dfs = True
                            draw_solve = True
                            pygame.event.clear()
                            startSolve(draw_solve, draw_dfs_event)
                        elif button.text == 'Greedy':
                            solve_greed = True
                            draw_solve = True
                            pygame.event.clear()
                            startSolve(draw_solve, draw_greedy_event)

            #If press Stop button
            elif event.type == MOUSEBUTTONUP:
                for button in button_list:
                    if button.rect.collidepoint((mouse_x, mouse_y)):
                        if button.text == 'Stop':
                            draw_maze = False
                            draw_maze_surface = True
                            draw_solve = False
                            solve = True
                            
                            pygame.event.clear()
                            startDrawMaze(draw_maze, draw_maze_event)
                            

            

            #Draw maze
            elif event.type == draw_maze_event:
                if len(paths) > 0:
                    drawMaze(screen, maze, paths.pop(0), cell_size)
                else:
                    draw_maze = False
                    startDrawMaze(draw_maze, draw_maze_event)

            #Draw solution
            elif event.type == draw_dijkstra_event:
                
                if len(explored_path_dijkstra) > 0:
                    drawExplored(screen, maze, explored_path_dijkstra.pop(0), cell_size)
                else:
                    if len(best_path_dijkstra) > 0:
                        drawSolve(screen, maze, best_path_dijkstra.pop(0), cell_size)
                    else:
                        draw_solve = False
                        startSolve(draw_solve, draw_dijkstra_event)
            elif event.type == draw_astar_event:
                if len(explored_path_astar) > 0:
                    drawExplored(screen, maze, explored_path_astar.pop(0), cell_size)
                else:
                    if len(best_path_astar) > 0:
                        drawSolve(screen, maze, best_path_astar.pop(0), cell_size)
                    else:
                        draw_solve = False
                        startSolve(draw_solve, draw_astar_event)
                
            
             


        #Draw buttons
        
        for button in button_list:
            font = pygame.font.Font(button.font, button.font_size)
            button_text = font.render(button.text, True, button.text_color)
            text_rect = button_text.get_rect(center = button.rect.center) #center the text
            
            if button.text == 'Stop':
                if button.rect.left <= mouse_x <= button.rect.right and button.rect.top <= mouse_y <= button.rect.bottom:
                    pygame.draw.rect(screen, 'red', button.rect)
                else:
                    pygame.draw.rect(screen, button.color, button.rect)

            if button.text == 'Menu':
                if button.rect.left <= mouse_x <= button.rect.right and button.rect.top <= mouse_y <= button.rect.bottom:
                    pygame.draw.rect(screen, '#78e37f', button.rect)
                else:
                    pygame.draw.rect(screen, button.color, button.rect)

            if button.text in menu_list:
                if button.rect.left <= mouse_x <= button.rect.right and button.rect.top <= mouse_y <= button.rect.bottom:
                    pygame.draw.rect(screen, '#fafafa', button.rect)
                else:
                    pygame.draw.rect(screen, button.color, button.rect)

            screen.blit(button_text, text_rect) 


       


        




        pygame.display.flip()