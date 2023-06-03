import pygame
import sys
from pygame.locals import *
from .Button import Button

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



def startDrawMaze(draw_maze, draw_maze_event):
    if draw_maze == True:
        pygame.time.set_timer(draw_maze_event, 1)
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


def startSolve(maze, algo, solve_list):
    if algo not in solve_list.keys():
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
            #DFS
            best_path, explored_path = dfs(maze)
        elif algo == 'GBFS':
            #GBFS
            best_path, explored_path = greedy_best_first_search(maze)

        solve_list[algo] = [best_path, explored_path]
    else:
        best_path = solve_list[algo][0]
        explored_path = solve_list[algo][1]

    
    return best_path, explored_path

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
    maze = GoodMaze(55, 33)
    maze.randomizeMazeDepthFirst(maze.getStart())
    walls = maze.walls
    paths = maze.paths
    paths.sort(key = lambda x: x.getRank())
    return maze

def main():

    #Create maze
    #maze = GoodMaze()
    #maze.randomizeMazeDepthFirst(maze.getStart())
    #maze.setStart(1, 1)
    #maze.setEnd(31, 19)
    #maze.randomizeMaze()


    #Set up the drawing window
    width = 1730
    height = 973
    
    pygame.init()

    button_list = []

    #Create exit button
    stop_button = Button(40, 40, 80, 60, color = 'blue', text = 'Stop', text_color = 'black', font_size = 32)
    button_list.append(stop_button)

    #Create randomaze button
    randomaze_button = Button(455, 25, 270, 30, color = 'yellow', text = 'Randomize maze', text_color = 'black', font_size = 32)
    button_list.append(randomaze_button)

    #Create menu button------------------------------------------------------------------------------
    menu_button = Button(745, 25, 270, 30,color = 'yellow', text = 'Solve maze', font_size = 32)
    button_list.append(menu_button)

    menu_list = ['A*', 'Dijkstra', 'BFS', 'DFS', 'Greedy']
    menu_item_color = 'yellow'
    #Create Astar button
    astar_button = Button(745, 55, 270, 30, color = menu_item_color, text = 'A*', text_color = 'black', font_size = 32)
    button_list.append(astar_button)
    #Create Dijkstra button
    dijkstra_button = Button(745, 85, 270, 30, color = menu_item_color, text = 'Dijkstra', text_color = 'black', font_size = 32)
    button_list.append(dijkstra_button)
    #Create BFS button
    bfs_button = Button(745, 115, 270, 30, color = menu_item_color, text = 'BFS', text_color = 'black', font_size = 32)
    button_list.append(bfs_button)
    #Create DFS button
    dfs_button = Button(745, 145, 270, 30, color = menu_item_color, text = 'DFS', text_color = 'black', font_size = 32)
    button_list.append(dfs_button)
    #Create Greedy button
    greedy_button = Button(745, 175, 270, 30, color = menu_item_color, text = 'Greedy', text_color = 'black', font_size = 32)
    button_list.append(greedy_button)
    #------------------------------------------------------------------------------------------------
    
    

    
    # Variable to keep our game loop running
    gameOn = True
    draw_maze = False
    draw_maze_surface = True
    solve_list = {}
    
    

    #Create event to draw maze
    draw_maze_event = pygame.USEREVENT + 1

    #Create event to draw solution
    draw_solve_event = pygame.USEREVENT + 2

    #Box grow 
    box_grow_event = pygame.USEREVENT + 3

    #Init screen
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Pathfinding Visualizer')
    screen.fill('white')

    # Our game loop
    while gameOn:

        #Get paths and walls
        if draw_maze_surface == True:
            maze = getMazeInfo()
            paths = maze.paths.copy()
            best_path = []
            explored_path = []
            cell_size = 33/maze.getWidth() * 20
            maze_surf = pygame.Surface((maze.getWidth()*cell_size, maze.getHeight()*cell_size))
            maze_surf.fill('black')
            screen.blit(maze_surf, ((width - maze.getWidth()*cell_size)/2, (height - maze.getHeight()*cell_size)/2))
            draw_maze_surface = False


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
                for button in button_list:
                    if button.rect.collidepoint((mouse_x, mouse_y)):
                        pygame.event.post(pygame.event.Event(box_grow_event))
                        if button.text == 'Stop':
                            draw_maze = False
                            draw_maze_surface = True
                            pygame.event.clear()
                            startDrawMaze(draw_maze, draw_maze_event)

                        elif button.text == 'Randomize maze':
                            draw_maze = True
                            startDrawMaze(draw_maze, draw_maze_event)
                            
                        elif button.text == 'A*':
                            paths = maze.paths.copy()
                            for path in paths:
                                drawMaze(screen, maze, path, cell_size)
                            best_path, explored_path = startSolve(maze, button.text, solve_list)
                            pygame.event.clear(draw_solve_event)
                            pygame.time.set_timer(draw_solve_event, 10)
                        elif button.text == 'Dijkstra':
                            paths = maze.paths.copy()
                            for path in paths:
                                drawMaze(screen, maze, path, cell_size)
                            best_path, explored_path = startSolve(maze, button.text, solve_list)
                            pygame.event.clear(draw_solve_event)
                            pygame.time.set_timer(draw_solve_event, 10)
                        elif button.text == 'BFS':
                            paths = maze.paths.copy()
                            for path in paths:
                                drawMaze(screen, maze, path, cell_size)
                            best_path, explored_path = startSolve(maze, button.text, solve_list)
                            pygame.event.clear(draw_solve_event)
                            pygame.time.set_timer(draw_solve_event, 10)
                        elif button.text == 'DFS':
                            paths = maze.paths.copy()
                            for path in paths:
                                drawMaze(screen, maze, path, cell_size)
                            best_path, explored_path = startSolve(maze, button.text, solve_list)
                            pygame.event.clear(draw_solve_event)
                            pygame.time.set_timer(draw_solve_event, 10)
                        elif button.text == 'Greedy':
                            paths = maze.paths.copy()
                            for path in paths:
                                drawMaze(screen, maze, path, cell_size)
                            best_path, explored_path = startSolve(maze, button.text, solve_list)
                            pygame.event.clear(draw_solve_event)
                            pygame.time.set_timer(draw_solve_event, 10)

                      
                            

            #Draw maze
            elif event.type == draw_maze_event:
                #paths = maze.paths.copy()
                if len(paths) > 0:
                    drawMaze(screen, maze, paths.pop(0), cell_size)
                else:
                    pygame.event.clear()

            #Draw solution
            elif event.type == draw_solve_event:
                if len(explored_path) > 0:
                    drawExplored(screen, maze, explored_path.pop(0), cell_size)
                else:
                    if len(best_path) > 0:
                        drawSolve(screen, maze, best_path.pop(0), cell_size)
                    else:
                        pygame.event.clear()

            #Box grow
            elif event.type == box_grow_event:
                for button in button_list:
                    if grow:
                        button.rect.inflate_ip(5, 5)
                        grow = button.rect.width < button.width * 5
                    else:
                        button.rect.inflate_ip(-5, -5)
                        grow = button.rect.width > button.width

        #Draw buttons
        
        for button in button_list:
            font = pygame.font.Font(button.font, button.font_size)
            button_text = font.render(button.text, True, button.text_color)
            text_rect = button_text.get_rect(center = button.rect.center) #center the text
            pygame.draw.rect(screen, button.color, button.rect)
            screen.blit(button_text, text_rect) 


        pygame.display.flip()