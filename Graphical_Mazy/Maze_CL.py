#!/usr/bin/python3 -tt

#Maze Generator

import sys, pygame, os
from pygame.locals import *
from Maze_class import halls
#import pdb
import random
from random import randrange, randint

#Globals
#base maze 0 elemets

col = 0
row = 0
startx = 1
starty = 1
black = (  0,   0,   0)
white = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
blocksz = ()
maze1 = halls()    #Init object maze1 global


def draw_maze(screen, maze1, blocksz, col, row):
# display u\2588 block char
# directions for NORTH, EAST, SOUTH, WEST
    yellow = (255, 255, 0)
    solvesz = (blocksz[0]/2, blocksz[1]/2)
    solveoffset = (solvesz[0]/2, solvesz[1]/2)
    #boarder around the maze
    pygame.draw.rect(screen, white, [0, 0, blocksz[0] * (row * 2 + 2), blocksz[1]])
    pygame.draw.rect(screen, white, [0, 0, blocksz[0], blocksz[1] * (col * 2 + 2)])
    pygame.draw.rect(screen, white, [0, blocksz[1] * (col * 2), blocksz[0] * (row * 2 + 1), blocksz[1] * (col * 2 + 2)])
    pygame.draw.rect(screen, white, [blocksz[0] * (row * 2), 0, blocksz[0] * (row * 2 + 1), blocksz[1] * (col * 2 + 1)])
    #Draw the cells
    for y in range(row):
        yy = (row - 1) - y
        for x in range(col):      # [ [(T, T, T, T) ...][() () () () () ][][][][]  ]
            if (x + 1) < col and (y + 1) < row:  #Central Blocks
                centerblk = (((x * 2 + 1)*blocksz[0]) + blocksz[0],((y * 2 + 1)*blocksz[1]) + blocksz[1])
                pygame.draw.rect(screen, white, [centerblk[0], centerblk[1], blocksz[0]+1, blocksz[1]+1])
            if maze1.data[x][y][1] == False and (x + 1) < col:  #If there is a EAST blocked
                eastgate = (((x * 2 + 2) * blocksz[0]),((yy * 2 + 1) * blocksz[1]))
                pygame.draw.rect(screen, white, [eastgate[0], eastgate[1], blocksz[0]+1, blocksz[1]+1])
            if maze1.data[x][y][2] == False and (yy + 1) < row:  #If there is a SOUTH blocked
                southgate = (((x * 2 + 1) * blocksz[0]),((yy * 2 + 2) * blocksz[1]))
                pygame.draw.rect(screen, white, [southgate[0], southgate[1], blocksz[0]+1, blocksz[1]+1])
            if maze1.data[x][yy][4]:
                #if solver path then draw path in yellow
                solveoffset = (((x * 2 + 1) * blocksz[0]) + (solvesz[0] / 2), ((y * 2 + 1) * blocksz[1]) + (solvesz[1] / 2))
                pygame.draw.rect(screen, yellow, [solveoffset[0], solveoffset[1], solvesz[0], solvesz[1]])


def makemaze(col, row):
    global maze1
    startx = random.randint(0, col - 1)
    starty = random.randint(0, row - 1)
    #initial maze all cells clossed
    maze1.seal_halls(col, row)
    maze1.build_maze(startx, starty, col, row)
    maze1.solve(0, 0, col, row)


#standard out for main function
def main():
    #global width, height, maze, startx, starty
    random.seed()
    size = (800, 600)
    if len(sys.argv) == 3:
        colwidth = int(str(sys.argv[1]))
        rowheight = int(str(sys.argv[2]))
        if (colwidth < 2 or colwidth > 40) or (rowheight < 2 or rowheight > 40):
            print("Both values need to greater than 1 and less then 40.\n")
            sys.exit(1)
    else:
        print("Enter two numbers for width and height.\n")
        sys.exit(1)

    #initalize screen
    pygame.init()
    backscreen = pygame.display.set_mode(size,HWSURFACE|DOUBLEBUF|RESIZABLE)
    #set current size of the display as the starting size
    backscreen.fill(black)
    backscreen.blit(backscreen, (0,0))

    #inital maze
    makemaze(colwidth, rowheight)

    #inital rect size for the maze elements
    blocksz = ((size[0] / (colwidth * 2)), (size[1] / (rowheight * 2)))

    # Graphical output of maze and inital display
    draw_maze(backscreen, maze1, blocksz, colwidth, rowheight)
    pygame.display.flip()

    #Do main loop untill quit event
    while True:
        mouse = cursor = space = False
        pygame.event.pump()
        #event = pygame.event.wait()
        #get input
        pygame.display.flip()
        for event in pygame.event.get():
            print("Event: ", event)
            if event.type == pygame.QUIT \
                or (event.type == KEYDOWN and event.key == K_ESCAPE) \
                or (event.type == KEYDOWN and event.key == K_q):
                    sys.exit()
            elif event.type == VIDEORESIZE:
                size = event.size
                backscreen = pygame.display.set_mode(size, HWSURFACE | DOUBLEBUF | RESIZABLE)
                draw_maze(backscreen, maze1, blocksz, colwidth, rowheight)
            elif (event.type == KEYDOWN):
                if (event.key == K_SPACE):
                    space = True
                # if cursor key is pressed
                elif (event.key == K_UP):
                    if (colwidth < 40): colwidth += 1
                    if (rowheight < 40): rowheight += 1
                    cursor = True
                elif (event.key == K_DOWN):
                    if (colwidth > 3):colwidth -= 1
                    if (rowheight > 3): rowheight -= 1
                    cursor = True
                # if either cursor key or space pressed
                if space or cursor:
                    #print("screen, col-row :", size, colwidth, rowheight)
                    # change formating on maze to new
                    blocksz = ((size[0] / (colwidth * 2)), (size[1] / (rowheight * 2)))
                    backscreen.fill(black)
                    makemaze(colwidth, rowheight)
                    # Graphical output of maze
                    draw_maze(backscreen, maze1, blocksz, colwidth, rowheight)
                    cursor = space = False




# This is the standard boiler plate call for main
if __name__=='__main__':
        main()