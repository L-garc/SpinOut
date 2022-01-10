import pygame
from configparser import ConfigParser
pygame.init()

file = 'config.ini'
config = ConfigParser()
config.read( file )

#Cannot use one object and later change the font or size, must create new object for new font or font size
myFont = pygame.font.SysFont("calibri", 15)
largerFont = pygame.font.SysFont("calibri", 24)
scoreFont = pygame.font.SysFont("calibri", 20)

ds_width = 148*5 # Picked because each knob image is 148 x 148 images
ds_height = 148 + 75 # "+ 75" is for the space below the knobs for the buttons

#Defines colors based on combinations of rgb values
white = (255, 255, 255)
black = (0, 0, 0)
mint = (62, 180, 137)

#All moves required to solve a 5 knob game
answer = """
The least required moves are:

1 1 1 1 1
1 1 1 1 0
1 1 0 1 0
1 1 0 1 1
1 1 0 0 1
1 1 0 0 0
0 1 0 0 0
0 1 0 0 1
0 1 0 1 1
0 1 0 1 0
0 1 1 1 0
0 1 1 1 1
0 1 1 0 1
0 1 1 0 0
0 0 1 0 0
0 0 1 0 1
0 0 1 1 1
0 0 1 1 0
0 0 0 1 0
0 0 0 1 1
0 0 0 0 1
0 0 0 0 0

This is 21 Moves
         """
