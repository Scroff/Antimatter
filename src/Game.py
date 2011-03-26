import pygame, sys, os, Player
from pygame.locals import *

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
COLORKEY = (255,0,255)

def input(events): # Handles input
    for event in events:
        print event
        if event.type == QUIT: # Quit event
            sys.exit(0)

def loadImage(name, colorkey):
    """
    Loads an image from the res folder with the specified name and with the specified colorkey """
    
    fullname = os.path.join('res', name) # Create full name of file so it includes the res folder
    try:
        image = pygame.image.load(fullname) # Try and load the image
    except pygame.error, message:
        print "Cannot load image ", name
        raise SystemExit, message # If it can't load image, gtfo
    
    image = image.convert() # Set the image to the same format as dispaly so it is drawn quickly
    image.set_colorkey(colorkey, RLEACCEL)
    return image

pygame.init(); # initialise pygame
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
screen = pygame.display.get_surface()
updateRate = 50 # ms between updates
playerSprite = loadImage("player.bmp", COLORKEY)
player = Player.Player(10, playerSprite)
player.draw(screen)

while 1: # main loop
    input(pygame.event.get()) # Get input
    pygame.display.flip() # Update changes to screen