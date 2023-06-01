import pygame
from pygame.locals import *


from ..models.GoodCell import GoodCell as Cell
from ..models.GoodMaze import GoodMaze as Maze
from ..algorithms import *


pygame.init()
 
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Pathfinding Visualizer')

# Variable to keep our game loop running
gameOn = True
 
# Our game loop
while gameOn:
    # for loop through the event queue
    for event in pygame.event.get():
         
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
             
            # If the Backspace key has been pressed set
            # running to false to exit the main loop
            if event.key == K_BACKSPACE:
                gameOn = False
                 
        # Check for QUIT event
        elif event.type == QUIT:
            pygame.quit()

    # Define where the squares will appear on the screen
    # Use blit to draw them on the screen surface
    screen.blit(square1.surf, (40, 40))
    screen.blit(square2.surf, (40, 530))
    screen.blit(square3.surf, (730, 40))
    screen.blit(square4.surf, (730, 530))
 
    # Update the display using flip
    pygame.display.flip()