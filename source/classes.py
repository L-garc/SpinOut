import pygame
from variables import myFont, black
pygame.init()

class Knob:
    def __init__(self, number):
        self.state = 1 #.................................................Vertical, all knobs begin in the vertical position
        self.img = pygame.image.load('knob.png') #.......................Loads into memory knob image
        self.w = 148 #...................................................Image width
        self.h = 148 #...................................................Image Height
        self.x = number*(self.w) #.......................................X position of knob based on order created (first knob created at x pos 0)
        self.y = 0 #.....................................................Y pos is always along the top of the screen at y pos 0
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h) #........Creates rectange at (x,y) with width (w) & height (h)
        self.index = 4-number #..........................................First knob created at x pos 0 is actually knob index 4 since python is zero-index, and we are using right to left logic (x = 0 is left side of screen)

        #print("knob index ", self.index, " created at x = ", self.x)#....Checks if the correct index is assosciated with the correct knob object (left most = 4, right most = 0)

    def switchState(self):
        if self.state == 1: #Switch from 1 to 0
            self.state = 0
            
        elif self.state == 0: #Switch from 0 to 1
            self.state = 1

    def rotate(self): #Rotate knob image
        self.img = pygame.transform.rotate(self.img, 90)

class button:
    def __init__(self, label, pos, size, color): #label = "Example Name" pos = (x,y) size = (w,h) color = (r,g,b)
        self.label = label
        self.x, self.y = pos
        self.w, self.h = size
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.dispLabel = myFont.render(label, 1, black) #(Str, True, color) no idea what the true is for

    def disp(self, ds):
        pygame.draw.rect(ds, self.color, self.rect)

        self.dlRect = self.dispLabel.get_rect()
        self.center = ((self.x + self.w/2)-self.dlRect.w/2,(self.y + self.h/2)-self.dlRect.h/2) #Center's Text to button center (text (x,y) is defined at top left corner)
        ds.blit(self.dispLabel, self.center)

class Options:
    def __init__(self):
        self.TchrMd = True #Teacher/student mode, shows terminal output for easier recursion analysis
        self.dispAnswer = False #Shows the steps to solving the game in the terminal
        self.shown = False

    def showAnswer(self):
        if ((self.dispAnswer == True) and (self.shown == False)):
            self.shown = True
            print(answer)
        
    def terminalOutput(self, allKnobs):
        if (self.TchrMd == True):
            print(allKnobs[4].state, allKnobs[3].state ,allKnobs[2].state, allKnobs[1].state, allKnobs[0].state)

    def chngOption(self, label):
        if (label == "Teacher / Student"):
            if (self.TchrMd == False):
                self.TchrMd = True
                
        elif (label == "Game Only"):
            if (self.TchrMd == True):
                self.TchrMd = False
