'''
Spin Out: Digitized
Author: Luis A. Garcia

rules:
to turn a knob the knob to the immediate right must be a 1 (vertical) and every knob right of that must be 0 (horizontal)

1.1 - Added win condition
1.2 - Added functioning buttons
1.3 - Added Title Screen
1.4 - Added Rules page, modded some functions
1.5 - Title Screen Logo, Fixed bug where after winning you'd go to title screen or rules screen
1.6 - Added Play Again screen, invalid move indicator, Option to output to terminal for teachers/professors
'''

import pygame
import math
import time
pygame.init()

#Cannot use one object and later change the font or size, must create new object for new font or font size
myFont = pygame.font.SysFont("calibri", 15)
largerFont = pygame.font.SysFont("calibri", 24)
scoreFont = pygame.font.SysFont("calibri", 20)

#Variable Definitions
ds_width = 148*5 # Picked because each knob image is 148 x 148 images
ds_height = 148 + 75 # "+ 75" is for the space below the knobs for the buttons

white = (255, 255, 255)
black = (0, 0, 0)
mint = (62, 180, 137)

#Setup display window
ds = pygame.display.set_mode((ds_width, ds_height))
pygame.display.set_caption('Spin It!')

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

    def disp(self):
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
        
    def terminalOutput(self):
        if (self.TchrMd == True):
            print(allKnobs[4].state, allKnobs[3].state ,allKnobs[2].state, allKnobs[1].state, allKnobs[0].state)

    def chngOption(self, label):
        if (label == "Teacher / Student"):
            if (self.TchrMd == False):
                self.TchrMd = True
                
        elif (label == "Game Only"):
            if (self.TchrMd == True):
                self.TchrMd = False

def checkKnobs(index): #Checks whether turning a knob would violate the rules
    check1 = False #Checks if the knob to the right is vertical or not --- False = not turning knob 0, True = turning knob 0
    check2 = True #Checks if every knob after check1 is horizontal or not --- False = some knob to the right is vertical (1)
    check3 = False #Checks if we're changing the 1st knob or not (by passes checks 1 and 2)
    val = False #Takes all three checks into consideration before letting a knob turn or not

    if (index == 0):
        check3 = True

    if allKnobs[index-1].state == 1: #Check if the knob to the right is 1 (vertical)
        check1 = True
    
    for i in range(index-2,-1,-1): #Iterate through knobs
        if allKnobs[i].state != 0:
            check2 = False
            break

    if((check1 and check2) or check3):
        val = True


    return val

def checkBtns(pos, lis):
    val = None
    for btn in lis:
        if btn.rect.collidepoint(pos):
            val = btn.label    

    return val

def dispKnobs():
    num = len(allKnobs)
    for index in range(0 ,num):
        ds.blit(allKnobs[index].img, (allKnobs[index].x, allKnobs[index].y))

def dispBtns(lis):
    num = len(lis)
    for index in range(0, num):
        lis[index].disp()
        
def checkClick(pos):
    val = None
    num = len(allKnobs)
    for index in range(num, -1, -1):
        if allKnobs[index-1].rect.collidepoint(pos):
            val = index-1
            break
    return val

def checkWin():
    val = True
    for knob in allKnobs:
        if knob.state == 1:
            val = False
    return val
            
            
def EndScreen():
    endscrn = pygame.image.load('EndScreen.png')
    ds.blit(endscrn,(0,0))
    pygame.display.flip()
    time.sleep(3)

def rlsScreen(): #Rules Screen
    goal = "Your goal is to turn every knob such that they are all horizontal"
    rule1 = "1) To turn a knob, the one to the immediate right must be vertical"
    rule2 = "2) Every knob to the right after that must be horizontal"
    dispGoal = largerFont.render(goal, 1, black) #(Str, Anti-ailiasing, color)
    dispRule1 = myFont.render(rule1, 1, black) #(Str, Anti-ailiasing, color)
    dispRule2 = myFont.render(rule2, 1, black) #(Str, Anti-ailiasing, color)

    done = False
    while (not done):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    label = checkBtns(event.pos, rlsBtns)
                    if (label == "Play"):
                        done = True
                    try:
                        btnActions(label) 
                    except TypeError:
                        pass
                    finally:
                        done = True
            
        ds.fill(white)
        dispBtns(rlsBtns)
        
        ds.blit(dispGoal, ((ds_width/2 - dispGoal.get_width()/2),25))
        ds.blit(dispRule1, (ds_width/2 - dispRule1.get_width()/2, dispGoal.get_height() + 50))
        ds.blit(dispRule2, (ds_width/2 - dispRule2.get_width()/2, dispRule1.get_height() + 75))
        
        pygame.display.flip()

def titleScreen():
    introLogo = pygame.image.load('IntroLogo.png')
    
    play = False
    while (not play):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = True
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    label = checkBtns(event.pos, ttlBtns)
                    try:
                        btnActions(label) 
                    except TypeError:
                        pass
                    finally:
                        play = True
                        continue
            
        ds.fill(white)
        dispBtns(ttlBtns)
        ds.blit(introLogo,(0,0))
        pygame.display.flip()

def optScreen():
    
    play = False
    while (not play):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = True
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    label = checkBtns(event.pos, optBtns)
                    try:
                        btnActions(label) 
                    except TypeError:
                        pass
                    finally:
                        if (label == "Title Screen"):
                            play = True
            
        ds.fill(white)
        dispBtns(optBtns)
        pygame.display.flip()

def playAgainScreen():
    restart()

    play = False
    while (not play):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = True
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    label = checkBtns(event.pos, againBtns)
                    try:
                        btnActions(label) 
                    except TypeError:
                        pass
                    finally:
                        play = True
            
        ds.fill(white)
        dispBtns(againBtns)
        pygame.display.flip()

def btnActions(label):
    global Solved

    if (label == "Reset"):
        resetKnobs()
    elif (label == "Restart"):
        restart()
    elif (label == "Rules"):
        rlsScreen()
    elif (label == "Play"):
        mainGame()
    elif (label == "Options"):
        optScreen()
    elif (label == "Title Screen"):
        titleScreen()
    elif (label == "Quit"):
        EndScreen()
    elif (label == "Teacher / Student" or "Game Only"):
        options.chngOption(label)
    else:
        pass
            
def resetKnobs():
    for knob in allKnobs:
        if knob.state == 0:
            knob.rotate()
            knob.state = 1

def restart():
    global score
    for knob in allKnobs:
        if knob.state == 0:
            knob.rotate()
            knob.state = 1
    score = 0

def mainGame():
    global score
    invalidMove = pygame.image.load('InvalidMoveIndicatorOverLay.png')
    youWin = pygame.image.load('YouWin.png')
    Solved = False

    while (not Solved):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    index = checkClick(event.pos) #Tuple (x,y) for knobs
                    label = checkBtns(event.pos, mainBtns) #For buttons in main game
                    try:
                        btnActions(label)
                        if checkKnobs(index) == True:
                            score += 1
                            
                            #Changes the requested knob
                            allKnobs[index].switchState()
                            #Rotates knob image
                            allKnobs[index].rotate()
                            #While loop will finish and not repeat
                            Solved = checkWin()

                            options.terminalOutput()
                            if Solved == True:
                                ds.blit(youWin,(0,0))
                                pygame.display.flip()
                                time.sleep(3)
                                playAgainScreen()
                                
                        elif checkKnobs(index) == False:
                            ds.blit(invalidMove,(0,0))
                            pygame.display.flip()
                            time.sleep(.5)
                    except TypeError: #Clicking a space with no buttons or knobs raises TypeError
                        pass          #This catches that error and ignores it
                    finally:
                        if (label == "Quit"):
                            Solved = True

                
        ds.fill(white)
        
        #Display knobs & buttons
        dispKnobs()
        dispBtns(mainBtns)

        diScore = scoreFont.render(str(score), 1, black) #(Str, Anti-ailiasing, color)
        ds.blit(diScore,(0,0))#(223 - diScore.get_width(),0))

        #Displays all changes made between the screen being filled and now
        pygame.display.flip()
#============================================================================================================================

numKnobs = 5

allKnobs = [] #Holds all knobs in this list
mainBtns = [] #Holds main buttons such as reset or restart
ttlBtns = []  #Holds title screen buttons
rlsBtns = []  #Holds rule screen buttons
optBtns = []  #Holds options screen buttons
againBtns = []#Holds "play again?" screen buttons

#label = "Example Name" pos = (x,y) size = (w,h) color = (r,g,b)
mainBtns.append(button("Reset", (25, 173), (205, 25), mint))
mainBtns.append(button("Restart", (255, 173), (205, 25), mint))
mainBtns.append(button("Quit", (485, 173), (205, 25), mint))

ttlBtns.append(button("Play", (25, 173), (153.75, 25), mint))
ttlBtns.append(button("Rules", (203.75, 173), (153.75, 25), mint))
ttlBtns.append(button("Options", (382.5, 173), (153.75, 25), mint))
ttlBtns.append(button("Quit", (561.25, 173), (153.75, 25), mint))

rlsBtns.append(button("Play", (25, 173), (332.5, 25), mint))
rlsBtns.append(button("Quit", (382.5, 173), (332.5, 25), mint))

againBtns.append(button("Title Screen", (25, 25), (100, 25), mint))
againBtns.append(button("Play", (100, (223/3)), (540, 25), mint))
againBtns.append(button("Quit", (100, (371/3)), (540, 25), mint))

optBtns.append(button("Title Screen", (25, 25), (100, 25), mint))
optBtns.append(button("Teacher / Student", (100, (223/3)), (540, 25), mint))
optBtns.append(button("Game Only", (100, (371/3)), (540, 25), mint))
optBtns.append(button("Quit", (615, 173), (100, 25), mint))

options = Options()

for number in range(0,numKnobs):
    allKnobs.append( Knob(number) ) #Creates the knob objects with correct x position

allKnobs.reverse() #Reverses list since we're using right to left logic (images and checks)

options.showAnswer()
options.terminalOutput() #Prints the first stage i.e. 1 1 1 1 1

score = 0

titleScreen()

#Close the program   
pygame.quit()
