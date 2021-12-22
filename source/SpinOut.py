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
1.7 - Organized code into seperate files
'''

import pygame
import math
import time
import variables
import elements
import classes #We can do this because the classes module contains only the necessary for this application
pygame.init()

#Setup display window
ds = pygame.display.set_mode((variables.ds_width, variables.ds_height))
pygame.display.set_caption('Spin It!')

def checkKnobs(index): #Checks whether turning a knob would violate the rules
    check1 = False #Checks if the knob to the right is vertical or not --- False = not turning knob 0, True = turning knob 0
    check2 = True #Checks if every knob after check1 is horizontal or not --- False = some knob to the right is vertical (1)
    check3 = False #Checks if we're changing the 1st knob or not (by passes checks 1 and 2)
    val = False #Takes all three checks into consideration before letting a knob turn or not

    if (index == 0):
        check3 = True

    if elements.allKnobs[index-1].state == 1: #Check if the knob to the right is 1 (vertical)
        check1 = True
    
    for i in range(index-2,-1,-1): #Iterate through knobs
        if elements.allKnobs[i].state != 0:
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
    num = len(elements.allKnobs)
    for index in range(0 ,num):
        ds.blit(elements.allKnobs[index].img, (elements.allKnobs[index].x, elements.allKnobs[index].y))

def dispBtns(lis):
    num = len(lis)
    for index in range(0, num):
        lis[index].disp(ds)
        
def checkClick(pos):
    val = None
    num = len(elements.allKnobs)
    for index in range(num, -1, -1):
        if elements.allKnobs[index-1].rect.collidepoint(pos):
            val = index-1
            break
    return val

def checkWin():
    val = True
    for knob in elements.allKnobs:
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
    dispGoal = variables.largerFont.render(goal, 1, variables.black) #(Str, Anti-ailiasing, color)
    dispRule1 = variables.myFont.render(rule1, 1, variables.black) #(Str, Anti-ailiasing, color)
    dispRule2 = variables.myFont.render(rule2, 1, variables.black) #(Str, Anti-ailiasing, color)

    done = False
    while (not done):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    label = checkBtns(event.pos, elements.rlsBtns)
                    if (label == "Play"):
                        done = True
                    try:
                        btnActions(label) 
                    except TypeError:
                        pass
                    finally:
                        done = True
            
        ds.fill(variables.white)
        dispBtns(elements.rlsBtns)
        
        ds.blit(dispGoal, ((variables.ds_width/2 - dispGoal.get_width()/2),25))
        ds.blit(dispRule1, (variables.ds_width/2 - dispRule1.get_width()/2, dispGoal.get_height() + 50))
        ds.blit(dispRule2, (variables.ds_width/2 - dispRule2.get_width()/2, dispRule1.get_height() + 75))
        
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
                    label = checkBtns(event.pos, elements.ttlBtns)
                    try:
                        btnActions(label) 
                    except TypeError:
                        pass
                    finally:
                        play = True
                        continue
            
        ds.fill(variables.white)
        dispBtns(elements.ttlBtns)
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
                    label = checkBtns(event.pos, elements.optBtns)
                    try:
                        btnActions(label) 
                    except TypeError:
                        pass
                    finally:
                        if (label == "Title Screen"):
                            play = True
            
        ds.fill(variables.white)
        dispBtns(elements.optBtns)
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
                    label = checkBtns(event.pos, elements.againBtns)
                    try:
                        btnActions(label) 
                    except TypeError:
                        pass
                    finally:
                        play = True
            
        ds.fill(variables.white)
        dispBtns(elements.againBtns)
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
    for knob in elements.allKnobs:
        if knob.state == 0:
            knob.rotate()
            knob.state = 1

def restart():
    global score
    for knob in elements.allKnobs:
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
                    label = checkBtns(event.pos, elements.mainBtns) #For buttons in main game
                    try:
                        btnActions(label)
                        if checkKnobs(index) == True:
                            score += 1
                            
                            #Changes the requested knob
                            elements.allKnobs[index].switchState()
                            #Rotates knob image
                            elements.allKnobs[index].rotate()
                            #While loop will finish and not repeat
                            Solved = checkWin()

                            options.terminalOutput(elements.allKnobs)
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

                
        ds.fill(variables.white)
        
        #Display knobs & buttons
        dispKnobs()
        dispBtns(elements.mainBtns)

        diScore = variables.scoreFont.render(str(score), 1, variables.black) #(Str, Anti-ailiasing, color)
        ds.blit(diScore,(0,0))#(223 - diScore.get_width(),0))

        #Displays all changes made between the screen being filled and now
        pygame.display.flip()
#============================================================================================================================

numKnobs = 5

options = classes.Options()

for number in range(0,numKnobs):
    elements.allKnobs.append( classes.Knob(number) ) #Creates the knob objects with correct x position

elements.allKnobs.reverse() #Reverses list since we're using right to left logic (images and checks)

options.showAnswer()
options.terminalOutput(elements.allKnobs) #Prints the first stage i.e. 1 1 1 1 1

score = 0

titleScreen()

#Close the program   
pygame.quit()
