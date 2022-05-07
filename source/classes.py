import pygame
from variables import myFont, black
from variables import file, config
import os.path
pygame.init()

class Knob:
    def __init__(self, number):
        self.state = 1 #.................................................Vertical, all knobs begin in the vertical position
        self.img = pygame.image.load('spinOutRealisticKnob.png')#('knob.png') #.......................Loads into memory knob image

        self.img = pygame.transform.scale(self.img, (148,148))
        
        self.w = 148 #...................................................Image width
        self.h = 148 #...................................................Image Height
        self.x = number*(self.w) #.......................................X position of knob based on order created (first knob created at x pos 0)
        self.y = 0 #.....................................................Y pos is always along the top of the screen at y pos 0
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h) #........Creates rectange at (x,y) with width (w) & height (h)
        self.index = 4-number #..........................................First knob created at x pos 0 is actually knob index 4 since python is zero-index, and we are using right to left logic (x = 0 is left side of screen)

    def switchState(self):
        if self.state == 1: #Switch from 1 to 0
            self.state = 0
            
        elif self.state == 0: #Switch from 0 to 1
            self.state = 1

    def rotate(self, restart=False): #Rotate knob image
        if restart == False:
            val = 1
        elif restart == True:
            val = -1
            
        if (self.state == 0):
            self.img = pygame.transform.rotate(self.img, 90*val) #If want to restart the game and the knob is horizontal, rotate CCW instead of the usual CW
        elif self.state == 1:
            self.img = pygame.transform.rotate(self.img, -90)
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
        if os.path.exists("config.ini") == False:
            newFile = open("config.ini", "w")
            newFile.close()

            file = 'config.ini'
            config.read( file )

            config.add_section('options')
            config.set('options', 'Teacher / Student', 'False')

            with open(file, 'a') as configfile:
                config.write(configfile)

        self.val = config['options']['Teacher / Student'] #Teacher/student mode, shows terminal output for easier recursion analysis
        if self.val == "False":
            self.TchrMd = False
        elif self.val == "True":
            self.TchrMd = True

        self.dispAnswer = False #Shows the steps to solving the game in the terminal
        self.shown = False

        self.prevStates = [] #Saves the previous knob states from each move

    def showAnswer(self):
        if ((self.dispAnswer == True) and (self.shown == False)):
            self.shown = True
            print(answer)
        
    def terminalOutput(self, allKnobs):
        if (self.TchrMd == True):
            temp = []
            
            for knob in allKnobs:
                temp.append(knob.state)
                
            temp.reverse()

            print(*temp) #The asterisk means print just prints as a list what is in temp
            self.prevStates.insert(0,temp) #Place at beggining, previous state (so that the previous move is index 1, two moves ago is index 2

    def prevMoves(self, index = None):
        #This is for retreiving previous knob states
        if index != None:
            if len(self.prevStates) > 1:
                return self.prevStates[index]
            else:
                return self.prevStates[0] #Maintain current state

    def popPrevMoves(self, index):
        if len(self.prevStates) > 1:
            self.prevStates.pop(index)

    def chngOption(self, label):
        if (label == "Teacher / Student"):
            if (self.TchrMd == False):
                self.TchrMd = True
                config.set('options', 'Teacher / Student', 'True')
                print("Teacher / Student Mode activated \n")
                
        elif (label == "Game Only"):
            if (self.TchrMd == True):
                self.TchrMd = False
                config.set('options', 'Teacher / Student', 'False')
                print("Game Only Mode activated \n")
                
        with open(file, 'w') as configfile:
                    config.write( configfile )
