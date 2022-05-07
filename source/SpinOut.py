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
1.8 - Default to game only mode, toggleable to recursion/teacher/student mode
'''

import pygame
import math
import time
import variables
import elements
import classes
pygame.init()

#Setup display window
ds = pygame.display.set_mode((variables.ds_width, variables.ds_height))
pygame.display.set_caption('Spin It!')

allKnobs = [] #Having this defined in another module caused an issue where it could append but not clear the list

def createKnobs(numKnobs):
    if (len(allKnobs) > 0):
        globals()['allKnobs'] = []
        
    for number in range(0,numKnobs):
        allKnobs.append( classes.Knob(number) ) #Creates the knob objects with correct x position

    allKnobs.reverse() #Reverses list since we're using right to left logic (images and checks)

def checkKnobs(index): #Checks whether turning a knob would violate the rules
    check1 = False #Checks if the knob to the right is vertical or not --- False = not turning knob 0, True = turning knob 0
    check2 = True #Checks if every knob after check1 is horizontal or not --- False = some knob to the right is vertical (1)
    check3 = False #Checks if we're changing the 1st knob or not (by passes checks 1 and 2)
    val = False #Takes all three checks into consideration before letting a knob turn or not

    if (index == 0):
        check3 = True

    if allKnobs[index-1].state == 1: #Check if the knob to the right is 1 (vertical)
        check1 = True
    
    for i in range(index-2,-1,-1):
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
        lis[index].disp(ds)
        
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
                        if (label != None):
                            done = True
            
        ds.fill(variables.white)
        dispBtns(elements.rlsBtns)
        
        ds.blit(dispGoal, ((variables.ds_width/2 - dispGoal.get_width()/2),25))
        ds.blit(dispRule1, (variables.ds_width/2 - dispRule1.get_width()/2, dispGoal.get_height() + 50))
        ds.blit(dispRule2, (variables.ds_width/2 - dispRule2.get_width()/2, dispRule1.get_height() + 75))
        
        pygame.display.flip()

def titleScreen(): #After pressing quit anywhere you return here and the next line to run is except... which gets ignored
    introLogo = pygame.image.load('IntroLogo.png')  #this is why the title screen is visible for a short time before ending the program
    
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
                    except TypeError: #In testing a TypeError exception was never raised even when I expected there to be one
                        pass
                    finally:
                        if (label == "Quit"):
                            play = True
                            continue #This must be here for some reason or else the program will not close when you click "Quit"
            
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
                        if (label == "Title Screen" or "Quit"):
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
                        if (label != None): # Label should only ever be "not None" if you click a button
                            play = True
            
        ds.fill(variables.white)
        dispBtns(elements.againBtns)
        pygame.display.flip()

def strtScrn():
    play = False
    while (not play):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = True
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    label = checkBtns(event.pos, elements.strtBtns)
                    try:
                        btnActions(label) 
                    except TypeError:
                        pass
                    finally:
                        if (label != None):
                            play = True
            
        ds.fill(variables.white)
        dispBtns(elements.strtBtns)
        pygame.display.flip()

def btnActions(label):
    global Solved

    if (label == "Undo"):
        undo()
    elif (label == "Restart"):
        restart()
    elif (label == "Rules"):
        rlsScreen()
    elif (label == "Play"):
        mainGame()
    elif (label == "Play Again"):
        strtScrn()
        mainGame()
    elif (label == "3 Knobs"):
        createKnobs(3)
    elif (label == "4 Knobs"):
        createKnobs(4)
    elif (label == "5 Knobs"):
        createKnobs(5)
    elif (label == "Options"):
        optScreen()
    elif (label == "Title Screen"):
        titleScreen()
    elif (label == "Quit"):
        EndScreen()
        pygame.quit()
        quit()
    elif (label == "Teacher / Student" or "Game Only"):
        options.chngOption(label)
    else:
        pass
            
def resetKnobs():
    for knob in allKnobs:
        if knob.state == 0:
            knob.rotate(True)
            knob.state = 1

def restart():
    global score
    for knob in allKnobs:
        if knob.state == 0:
            knob.rotate(True) #Passing true means it will reset all knobs to vertical, (some may need to move CCW when they used to move CW)
            knob.state = 1
    score = 0
    
def undo():
    global score
    
    if score > 0: #If score is greater than zero (no negative scores)
        score -= 1 #Decrement score counter
    
    GameState = options.prevMoves(1)
    options.popPrevMoves(0) #Delete the current state, effectively means last move is now current move
    print("Game State = ", GameState)
    
    for i in range(0, len(GameState)):
        if allKnobs[i].state != GameState[i]: #If the current state of the knob is not the same as its prev state, rotate CW or CCW
            allKnobs[i].state = GameState[i] #Set the knob state to whatever the state was previously
            allKnobs[i].rotate() #Rotate image so that it matches what its state says it should look like
        

def mainGame():
    global score
    invalidMove = pygame.image.load('InvalidMoveIndicatorOverLay.png')
    youWin = pygame.image.load('YouWin.png')
    
    options.terminalOutput(allKnobs) #Prints initial state, where every knob state is 1
    
    Solved = False

    while (not Solved):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    undo()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    index = checkClick(event.pos) #Tuple (x,y) for knobs
                    label = checkBtns(event.pos, elements.mainBtns) #For buttons in main game
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

                            options.terminalOutput(allKnobs)
                            #options.prevMoves()
                            
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
        ds.blit(diScore,(0,0))

        #Displays all changes made between the screen being filled and now
        pygame.display.flip()
#============================================================================================================================

options = classes.Options() #Options() is a class defined in the class module

strtScrn()

options.showAnswer() #If the option for this is set to true, it will print the steps to solve a 5 knob game

score = 0

titleScreen()

#Close the program
pygame.quit()
