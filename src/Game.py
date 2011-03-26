import pygame, sys, os, random, math
from pygame.locals import *

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
COLORKEY = (255,0,255)

class Particle:
    def __init__(self, radius, maxSpeed, matter, attractRadius, force, color):
        """
        radius = radius of particle
        maxSpeed = maximum speed of particle
        matter = True if matter, False if antimatter
        attractRadius = Radius at which will attract another polarity particle 
        color = Color to draw particle """
        self.radius = radius
        self.maxSpeed = maxSpeed
        self.matter = matter
        self.position = [0,0]
        self.direction = [0,0]
        self.attractRadius = attractRadius
        self.force = force;
        self.color = color
    
    def update(self, sec):
        """
        sec = Time since last update in seconds """
        self.position[0] += self.direction[0] * sec # Move along x axis
        self.position[1] += self.direction[1] * sec # Move along y axis
    
    def draw(self, screen):
        """
        screen = Screen to draw onto """
        
        pygame.draw.circle(screen, (0,255,255), self.position, self.attractRadius) # Draw attract radius (debug)
        pygame.draw.circle(screen, self.color, self.position, self.radius)
        
    def checkCollision(self, pos, radius, attractRadius):
        """
        Checks for collision within radius and attractRadius
        returns 1 for radius collision, 0 for attractRadius collision, -1 for no collision
        """
        xdist = self.position[0] - pos[0]
        ydist = self.position[1] - pos[1]
        dist = (xdist ** 2 + ydist ** 2) ** 0.5
        if dist <= (radius + self.radius):
            return 1
        if dist <= (attractRadius + self.attractRadius):
            return 0
        return -1
    
    def collide(self, part2):
        return 0 # TODO: Implement
    
    def attract(self, part2):
        xdist = self.position[0] - part2.position[0]
        ydist = self.position[1] - part2.position[1]
        dist = (xdist ** 2 + ydist ** 2) ** 0.5
        force1 = self.force / dist # Strength of force moving part1
        force2 = part2.force / dist # Strength of force moving part2
        newPos = [part2.position[0] + (xdist / 2), part2.position[1] + (ydist / 2)] # Point to move towards
        # New find the normalised unit vector between the points and this one
        vector1 = [(newPos[0] - self.position[0]) / dist, (newPos[1] - self.position[1]) / dist]
        vector2 = [(newPos[0] - part2.position[0]) / dist, (newPos[1] - part2.position[1]) / dist]
        # Modify direction for each particle
        self.direction[0] += vector1[0] * force1
        self.direction[1] += vector1[1] * force1
        part2.direction[0] += vector2[0] * force2
        part2.direction[1] += vector2[1] * force2
    
class Player(Particle):
    def __init__(self, radius, sprite, attractRadius, force, maxSpeed):
        Particle.__init__(self, radius, maxSpeed, True, attractRadius, force, (0,255,255))
        self.position = [50,50]
        self.direction = [0,0]
        self.radius = radius
        self.sprite = sprite
    
    def draw(self, screen):
        """ Draws the player.
        screen: Surface to draw on """
        pygame.draw.circle(screen, self.color, self.position, self.attractRadius) # Draw attract radius
        screen.blit(self.sprite, self.position)
        
    def update(self, sec):
        """
        Updates player position etc
        sec: Time in seconds since last update """
        mpos = pygame.mouse.get_pos()
        self.position[0] = mpos[0]
        self.position[1] = mpos[1]
        
    def flipPolarity(self):
        """
        Flips between matter and antimatter """
        self.matter = not self.matter # TODO: Change colour here too
        
class ParticleManager:
    def __init__(self, maxParticles, matColor, antiColor, radius, maxSpeed, attractRadius, force, player, spawnRate):
        """
        maxParticles =  Maximum number of particles that can spawn
        matColor = Color of matter
        antiColor = Color of antimatter
        radius = Radius for each particle
        maxSpeed = Max speed for each particle
        attractRadius = attractRadius for each particle
        force = attraction force of particles
        player = reference to the player
        spawnRate = Rate at which particles spawn automatically
        """
        self.maxParticles = maxParticles
        self.matColor = matColor
        self.antiColor = antiColor
        self.player = player
        self.spawnRate = spawnRate
        
        self.aliveList = [] # List of particles currently alive
        self.deadList = [] # List of all particles currently dead
        self.lastSpawn = 0.0 # Time since last spawn

        for i in range(maxParticles): # All particles start off dead so add them to dead list
            matter = (i % 2 == 0) # Half matter, half antimatter
            if matter:
                color = matColor
            else:
                color = antiColor
            part = Particle(radius, maxSpeed, matter, attractRadius, force, color)
            self.deadList.append(part)
            
    def spawnParticle(self):
        """ 
        Spawns a particle if we aren't at the max limit. Particle is spawned at a random location
        outside the range of any other particles or player
        """
        if len(self.deadList) > 0:
            part = self.deadList.pop() # There are dead available so get a body to raise
            top = part.radius + 1 # Highest it can spawn
            left = part.radius + 1 # Most left it can spawn
            right = WINDOW_WIDTH - part.radius  - 1 # Most right it can spawn
            bot = WINDOW_HEIGHT - part.radius - 1 # Lowest it can spawn
            spawnable = False # Will set to true when it is ok to spawn here
            
            while not spawnable:
                pos = [random.randint(left, right), random.randint(top, bot)] # Get a random location
                spawnable = True # Be optimistic
                
                collide = player.checkCollision(pos, part.radius, part.attractRadius)
                if collide >= 0:
                    spawnable = False # Too close to player
                    continue # Don't bother checking against other part, just roll again
                
                for alive in self.aliveList:
                    collide = alive.checkCollision(pos, part.radius, part.attractRadius)
                    if collide >= 0:
                        spawnable = False
                        break # We are in range of another particle so don't spawn here
                
            part.position = pos;
            self.aliveList.append(part)

    def spawnAll(self):
        """
        Turns all dead particles into living ones """
        for i in range(len(self.deadList)):
            self.spawnParticle()
    
    def update(self, sec):
        toDie = [] # List of particles which have to die when we finish
        for i in range(len(self.aliveList)):
            part1 = self.aliveList[i]
            for j in range(i+1, len(self.aliveList)): # Check all the ones after this particle for collision
                part2 = self.aliveList[j]
                collide = part1.checkCollision(part2.position, part2.radius, part2.attractRadius)
                if collide == 1: # Full on collision
                    part1.collide(part2)
                elif collide == 0: # Attract range
                    part1.attract(part2)
            
            collide = part1.checkCollision(player.position, player.radius, player.attractRadius) # Check proximity to player
            if collide == 1:
                player.collide(part1)
            if collide == 0:
                player.attract(part1)
            part1.update(sec)
                
    def draw(self, screen):
        for alive in self.aliveList:
            alive.draw(screen)
        
def input(events): # Handles input
    for event in events:
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
player = Player(10, playerSprite, 60, 10, 10)
particleMan = ParticleManager(1, (255,0,0), (0,255,0), 20, 20, 50, 10, player, 5)
particleMan.spawnAll()
clock = pygame.time.Clock()

while 1: # main loop
    input(pygame.event.get()) # Get input
    ms = clock.tick_busy_loop() # Time since last update in ms
    secs = ms / 1000.0 # Time in seconds
    player.update(secs)
    particleMan.update(secs)
    
    particleMan.draw(screen)
    player.draw(screen)
    pygame.display.flip() # Update changes to screen