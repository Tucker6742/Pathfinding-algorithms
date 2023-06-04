# import the pygame module
import pygame
 
# import pygame.locals for easier
# access to key coordinates
from pygame.locals import *


class Button():
    def __init__(self,
                 topleft_x, 
                 topleft_y,
                 width,
                 height,
                 color = 'white',
                 text = '',
                 text_color = 'white',
                 font = r'.\src\Font\Lexend\static\Lexend-Light.ttf',
                 font_size = 32):

        
        self.topleft_x = topleft_x
        self.topleft_y = topleft_y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = font
        self.font_size = font_size
        self.rect = pygame.Rect(self.topleft_x, self.topleft_y, self.width, self.height)




 

