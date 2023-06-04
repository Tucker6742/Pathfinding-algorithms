from concurrent.futures import thread
from tracemalloc import start
import pygame
import sys
from pygame.locals import *
from .Button import Button
from multiprocessing.pool import ThreadPool
import time as Time

from src.models.GoodCell import GoodCell as Cell
from src.models.GoodMaze import GoodMaze
from src.models.Maze import Maze
#from src.Visualize.DropDown import DropDown
from src.algorithms.Astar import A_star_search
from src.algorithms.Dijkstra import Dijkstra
from src.algorithms.BFS_Search import BFS_Search
from src.algorithms.Dfs import dfs
from src.algorithms.gbfs import greedy_best_first_search





#Set clock
clock = pygame.time.Clock()

def startDraw(draw_type, draw, draw_event):
    if draw == True:
        if draw_type == 'maze':
            pygame.time.set_timer(draw_event, 5)
        elif draw_type == 'solve' or draw_type == 'menu':
            pygame.time.set_timer(draw_event, 10)
    else:
        if draw_type == 'menu':
            pygame.time.set_timer(draw_event, 1)
        else:
            pygame.time.set_timer(draw_event, 0)
    

def drawMaze(screen, maze, path, cell_size):
    (x, y) = path.getCoordinates()
    cell = pygame.Rect(x*cell_size[0] + 25, y*cell_size[1] + 52, cell_size[0], cell_size[1])

    pygame.draw.rect(screen, 'white', cell)

    if (x, y) == maze.getStart() or (x, y) == maze.getEnd():
        pygame.draw.rect(screen, 'red', cell)

    pygame.display.update(cell)


def startSolve(maze, algo, solve_list):
    if algo not in solve_list.keys():
        start_time = Time.time()
        if algo == 'A*':
            #A*
            best_path, explored_path = A_star_search.search(maze)
        elif algo == 'Dijkstra':
            #Dijkstra
            (x_start, y_start) = maze.getStart()
            (x_end, y_end) = maze.getEnd()
            best_path, explored_path  = Dijkstra.dijkstra(maze, maze.getCell(x_start, y_start), maze.getCell(x_end, y_end))
        elif algo == 'BFS':
            #BFS
            best_path, explored_path = BFS_Search.search(maze)
        elif algo == 'DFS':
            #try:
                #DFS
                best_path, explored_path = dfs(maze)
            #except:
            #    print('Error')
        elif algo == 'Greedy':
            #GBFS
            best_path, explored_path = greedy_best_first_search.search(maze)
        time = round((Time.time() - start_time)*1000, 2)
        solve_list[algo] = [best_path, explored_path, time]
    else:
        best_path = solve_list[algo][0]
        explored_path = solve_list[algo][1]
    startDraw('solve', True, pygame.USEREVENT + 2)
    return solve_list, algo

def drawExplored(screen, maze, path, color, cell_size):
    (x, y) = path.getCoordinates()
    cell = pygame.Rect(x*cell_size[0] + 25, y*cell_size[1] + 52, cell_size[0], cell_size[1])

    pygame.draw.rect(screen, color, cell)
    if (x, y) == maze.getStart() or (x, y) == maze.getEnd():
        pygame.draw.rect(screen, 'red', cell)
    pygame.display.update(cell)

def drawSolve(screen, maze, path, color, cell_size):
    (x, y) = path.getCoordinates()
    cell = pygame.Rect(x*cell_size[0] + 25, y*cell_size[1] + 52, cell_size[0], cell_size[1])

    pygame.draw.rect(screen, color, cell)
    if (x, y) == maze.getStart() or (x, y) == maze.getEnd():
        pygame.draw.rect(screen, 'red', cell)
    pygame.display.update(cell)


def drawButton(screen, button, menu_list):
    font = pygame.font.Font(button.font, button.font_size)
    button_text = font.render(button.text, True, button.text_color)
    text_rect = button_text.get_rect(center = button.rect.center) #center the text
    if button.text in menu_list or button.text == 'Solve maze':
        pygame.draw.rect(screen, button.color, button.rect, 3)
    else:
        pygame.draw.rect(screen, button.color, button.rect)
    screen.blit(button_text, text_rect)

def drawScrollUp(screen, menu_button):
    pygame.draw.rect(screen, '#e8f8fa', menu_button.rect)
    pygame.display.update(menu_button)


def drawRunningDot(screen, dot):
    solving = pygame.Rect(27, 25, 270, 25)
    solving_text = pygame.font.Font('./src/Font/Lexend/static/Lexend-Light.ttf', 22).render('Solving:', True, 'black')
    pygame.draw.rect(screen, '#e8f8fa', solving)
    screen.blit(solving_text, (27, 25))

    pygame.draw.rect(screen, 'black', dot)
    
    pygame.display.update(dot)



def getMazeInfo():
    #width and height of maze must be odd and width - height > 10
    maze = GoodMaze(55, 33)
    maze.setStart(13, 31)
    maze.setEnd(41, 11)
    maze.randomizeMazeDepthFirst(maze.getStart())
    maze.setEnvironment()
    walls = maze.walls
    paths = maze.paths
    paths.sort(key = lambda x: x.getRank())
    return maze

def main():

    
    
    pygame.init()

    button_list = []
    menu_button_list = []

    font_size = 22


    #Create randomaze button
    randomaze_button = Button(1045, 52, 210, 30, color = '#27aae1', text = 'Randomize maze', text_color = 'black', font_size = font_size)
    button_list.append(randomaze_button)

    #Create menu button------------------------------------------------------------------------------
    menu_button = Button(1045, 322, 210, 30,color = 'black', text = 'Solve maze', text_color = 'black', font_size = font_size)
    button_list.append(menu_button)

    menu_list = ['A*', 'Dijkstra', 'BFS', 'DFS', 'Greedy']
    menu_item_color = 'black'
    #Create Astar button
    astar_button = Button(1045, 352, 210, 30, color = menu_item_color, text = 'A*', text_color = 'black', font_size = font_size)
    menu_button_list.append(astar_button)
    #Create Dijkstra button
    dijkstra_button = Button(1045, 382, 210, 30, color = menu_item_color, text = 'Dijkstra', text_color = 'black', font_size = font_size)
    menu_button_list.append(dijkstra_button)
    #Create BFS button
    bfs_button = Button(1045, 412, 210, 30, color = menu_item_color, text = 'BFS', text_color = 'black', font_size = font_size)
    menu_button_list.append(bfs_button)
    #Create DFS button
    dfs_button = Button(1045, 442, 210, 30, color = menu_item_color, text = 'DFS', text_color = 'black', font_size = font_size)
    menu_button_list.append(dfs_button)
    #Create Greedy button
    greedy_button = Button(1045, 472, 210, 30, color = menu_item_color, text = 'Greedy', text_color = 'black', font_size = font_size)
    menu_button_list.append(greedy_button)
    menu_copy = menu_button_list.copy()
    #------------------------------------------------------------------------------------------------
    
    

    
    # Variable to keep our game loop running
    gameOn = True
    draw_maze = False
    draw_maze_surface = True
    draw_menu = False
    solve_list = {}
    best_count = 0
    explored_count = 0
    explored_color_cycle = ['#f8f5fa', '#bda1cc']
    best_color_cycle = ['#c0cccb', '#65c7c1']
    
    #Dot list
    running_1_dot_box = pygame.Rect(115, 40, 10, 10)
    running_2_dot_box = pygame.Rect(130, 40, 10, 10)
    running_3_dot_box = pygame.Rect(145, 40, 10, 10)
    dot_count = 0
    dot_list = [running_1_dot_box, running_2_dot_box, running_3_dot_box]

    #Create event to draw maze
    draw_maze_event = pygame.USEREVENT + 1

    #Create event to draw solution
    draw_solve_event = pygame.USEREVENT + 2

    #Create event to draw menu
    draw_menu_event = pygame.USEREVENT + 3

    #Create event to draw dot
    draw_dot_event = pygame.USEREVENT + 4

    #Init screen
    width = 1335
    height = 707
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Pathfinding Visualizer')
    screen.fill('#e8f8fa')

    #Draw buttons
    for button in button_list:
        drawButton(screen, button, menu_list)
    # Our game loop
    press = False
    while gameOn:



        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        event_list = pygame.event.get()
        # for loop through the event queue
        for event in event_list:
            # Check for QUIT event
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # Check for MOUSEBUTTONDOWN event
            
            elif event.type == MOUSEBUTTONDOWN:
                press = True
                if press == True:
                    for button in button_list:
                        if button.rect.collidepoint((mouse_x, mouse_y)):
                            if button.text == 'Randomize maze':
                                draw_maze = True
                                maze = getMazeInfo()
                                #maze.setEnvironment()
                                paths = maze.paths.copy()
                                best_path = []
                                explored_path = []
                                maze_surf = pygame.Surface((990, 630))
                                cell_width = maze_surf.get_width()//maze.getWidth()
                                cell_height = maze_surf.get_height()//maze.getHeight()
                                cell_size = cell_width, cell_height 
                                maze_surf.fill('black')
                                screen.blit(maze_surf, (25, 52))
                                startDraw('maze', draw_maze, draw_maze_event)
                                pygame.time.set_timer(draw_solve_event, 0)
                                pygame.time.set_timer(draw_dot_event, 0)
                                solve_list.clear()

                            elif button.text == 'Solve maze':
                                draw_menu = 1 - draw_menu
                                startDraw('menu', draw_menu, draw_menu_event)
                            
                    for button in menu_button_list:
                        if button.rect.collidepoint((mouse_x, mouse_y)):
                            done_box = pygame.Rect(1045, 660, 270, 30)
                            pygame.draw.rect(screen, '#e8f8fa', done_box)
                            pygame.display.update(done_box)
                            running_text = pygame.font.Font('./src/Font/Lexend/static/Lexend-Light.ttf', 22).render('Running: ' + button.text, True, 'black')
                            running_box = pygame.Rect(1045, 292, 270, 30)
                            pygame.draw.rect(screen, '#e8f8fa', running_box)
                            screen.blit(running_text, (1045, 292))
                            time_box = pygame.Rect(1030, 90, 270, 30)
                            pygame.draw.rect(screen, '#e8f8fa', time_box)
                            pygame.display.update((running_box, time_box))
                                
                            pygame.time.set_timer(draw_dot_event, 500)
                            paths = maze.paths.copy()
                            for path in paths:
                                drawMaze(screen, maze, path, cell_size)

                            solve = ThreadPool(processes=1)
                            solve_result = solve.apply_async(startSolve, (maze, button.text, solve_list))

                                
                            startDraw('maze', False, draw_maze_event)
                            
                            
                    press = False
                      
                            

            #Draw maze
            elif event.type == draw_maze_event:
                #paths = maze.paths.copy()
                if len(paths) > 0:
                    drawMaze(screen, maze, paths.pop(0), cell_size)
                else:
                    startDraw('maze', False, draw_maze_event)

            #Draw menu
            if event.type == draw_menu_event:
                if len(menu_copy) > 0:
                    if draw_menu == 1:
                        drawButton(screen, menu_copy.pop(0), menu_list)
                    elif draw_menu == 0:
                        drawScrollUp(screen, menu_copy.pop(-1))
                else:
                    menu_copy = menu_button_list.copy()
                    startDraw('solve', False, draw_menu_event)
                
                        

            #Draw solution
            if event.type == draw_solve_event:
                solve_list, algo = solve_result.get()
                best_path, explored_path, time = solve_list[algo]
                if explored_count < len(explored_path):
                    drawExplored(screen, maze, explored_path[explored_count], explored_color_cycle[0], cell_size)
                    if explored_count > 0:
                        drawExplored(screen, maze, explored_path[explored_count - 1], explored_color_cycle[1], cell_size)
                    explored_count += 1
                    
                else:
                    if len(best_path) > best_count:
                        drawSolve(screen, maze, best_path[best_count], best_color_cycle[0], cell_size)
                        if best_count > 0:
                            drawSolve(screen, maze, best_path[best_count-1], best_color_cycle[1], cell_size)
                        best_count += 1
                    else:
                        startDraw('solve', False, draw_solve_event)
                        pygame.time.set_timer(draw_dot_event, 0)

                        done_text = pygame.font.Font('./src/Font/Lexend/static/Lexend-Light.ttf', 22).render('Done!', True, 'black')
                        done_box = pygame.Rect(110, 25, 210, 25)
                        pygame.draw.rect(screen, '#e8f8fa', done_box)
                        screen.blit(done_text, (110, 25))

                        time_text = pygame.font.Font(r'./src/Font/Lexend/static/Lexend-Light.ttf', 22).render('Runtime: ' + str(time) + ' milisec', True, 'black')
                        time_box = pygame.Rect(1045, 660, 210, 30)
                        pygame.draw.rect(screen, '#e8f8fa', time_box)
                        screen.blit(time_text, (1045, 660))

                        pygame.display.update((done_box, time_box))
                        explored_count = 0
                        best_count = 0




            #Draw running dot
            if event.type == draw_dot_event:
                if dot_count == 3:
                    dot_count = 0
                drawRunningDot(screen, dot_list[dot_count])
                dot_count += 1
            

         


        pygame.display.flip()