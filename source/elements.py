from classes import *
from variables import mint

strtBtns = []  #Holds start screen buttons (sets number of knobs in game)
mainBtns = [] #Holds main buttons such as reset or restart
ttlBtns = []  #Holds title screen buttons
rlsBtns = []  #Holds rule screen buttons
optBtns = []  #Holds options screen buttons
againBtns = []#Holds "play again?" screen buttons

#label = "Example Name" pos = (x,y) size = (w,h) color = (r,g,b)
strtBtns.append(button("3 Knobs", (91.25, 49), (125, 125), mint))
strtBtns.append(button("4 Knobs", (307.5, 49), (125, 125), mint))
strtBtns.append(button("5 Knobs", (523.75, 49), (125, 125), mint))

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
againBtns.append(button("Play Again", (100, (223/3)), (540, 25), mint))
againBtns.append(button("Quit", (100, (371/3)), (540, 25), mint))

optBtns.append(button("Title Screen", (25, 25), (100, 25), mint))
optBtns.append(button("Teacher / Student", (100, (223/3)), (540, 25), mint))
optBtns.append(button("Game Only", (100, (371/3)), (540, 25), mint))
optBtns.append(button("Quit", (615, 173), (100, 25), mint))
