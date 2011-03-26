import pygame, sys, os, random, math, copy
from pygame.locals import *

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
COLORKEY = (255,0,255)

KEY_UP = pygame.K_UP
KEY_DOWN = pygame.K_DOWN
KEY_LEFT = pygame.K_LEFT
KEY_RIGHT = pygame.K_RIGHT
KEY_FLIP = pygame.K_SPACE

PLAYER_RADIUS = 13
PLAYER_ATTRACTRADIUS = 60
PLAYER_FORCE = 100
PLAYER_MAXSPEED = 200
PLAYER_ACCELERATION = 400

MAX_PARTICLES = 10
MAT_COLOR = (255,0,0)
ANTI_COLOR = (0,255,0)
PARTICLE_RADIUS = 10
PARTICLE_MAXSPEED = 20
PARTICLE_ATTRACTRADIUS = 20
PARTICLE_FORCE = 10
PARTICLE_SPAWNRATE = 5

MAX_ENEMIES = 5
ENEMY_COLOR = (100, 20, 250)
ENEMY_RADIUS = 5
ENEMY_SPAWNRATE = 5

EXPLOSION_MAXTIME = 2
EXPLOSION_GROWTHRATE = 30
EXPLOSION_COLOR = (255,82,30)

class Particle:
    def __init__(self, radius, maxSpeed, matter, attractRadius, force, color):
        """
        radius = radius of particle
        maxSpeed = maximum speed of particle
        matter = True if matter, False if antimatter
        attractRadius = Radius at which will attract another polarity particle 
        color = Color to draw particle """
        self.radius = radius
        self.maxSpeed = maxSpeed # NOT IMPLMENTED
        self.matter = matter
        self.position = [0,0]
        self.speed = [0,0]
        self.attractRadius = attractRadius
        self.force = force;
        self.color = color
    
    def update(self, sec):
        """
        sec = Time since last update in seconds """
        self.position[0] += self.speed[0] * sec # Move along x axis
        self.position[1] += self.speed[1] * sec # Move along y axis
        if(self.position[0] + self.radius > WINDOW_WIDTH or 
           self.position[0] - self.radius < 0 or 
           self.position[1] + self.radius > WINDOW_HEIGHT or
           self.position[1] - self.radius < 0): # We are out of bounds, go back
            self.bounce()
            
    
    def draw(self, screen):
        """
        screen = Screen to draw onto """
        
        #pygame.draw.circle(screen, (0,255,255), self.position, self.attractRadius) # Draw attract radius (debug)
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
    
    def collide(self, part2, updateSelf=True):
        part2.speed = self.bounce(part2.speed)
    
    def attract(self, part2, updateSelf=True):
        xdist = self.position[0] - part2.position[0]
        ydist = self.position[1] - part2.position[1]
        dist = (xdist ** 2 + ydist ** 2) ** 0.5
        force1 = self.force / dist # Strength of force moving part1
        force2 = part2.force / dist # Strength of force moving part2
        newPos = [part2.position[0] + (xdist / 2), part2.position[1] + (ydist / 2)] # Point to move towards
        # Now find the normalised unit vector between the points and this one
        vector1 = [(newPos[0] - self.position[0]) / dist, (newPos[1] - self.position[1]) / dist]
        vector2 = [(newPos[0] - part2.position[0]) / dist, (newPos[1] - part2.position[1]) / dist]
        # Modify speed for each particle
        if updateSelf:
            self.speed[0] += vector1[0] * force1
            self.speed[1] += vector1[1] * force1
        part2.speed[0] += vector2[0] * force2
        part2.speed[1] += vector2[1] * force2

    def bounce(self, speed=None):
        """
        If a speed is supplied, it does a more compelx calculation 
        Returns None if no speed supplied or the modified speed if it is supplied """
        self.speed[0] *= -1
        self.speed[1] *= -1
        if speed is not None:
            avgx = (math.fabs(self.speed[0]) + math.fabs(speed[0])) / 2 # Average x and y velocities
            avgy = (math.fabs(self.speed[1]) + math.fabs(speed[1])) / 2
            self.speed[0] = math.copysign(avgx, self.speed[0])
            self.speed[1] = math.copysign(avgy, self.speed[1])
            speed[0] = math.copysign(avgx, speed[0] * -1)
            speed[1] = math.copysign(avgy, speed[1] * -1)
        
        return speed
            
            
        
class Player(Particle):
    def __init__(self, radius, sprite, attractRadius, force, maxSpeed, acceleration):
        Particle.__init__(self, radius, maxSpeed, True, attractRadius, force, (0,255,255))
        self.acceleration = acceleration
        self.position = [200,200]
        self.direction = [0,0]
        self.radius = radius
        self.sprite = sprite
    
    def draw(self, screen):
        """ Draws the player.
        screen: Surface to draw on """
        pygame.draw.circle(screen, self.color, self.position, self.attractRadius) # Draw attract radius
        x, y = self.position
        x -= self.radius
        y -= self.radius
        screen.blit(self.sprite, (x,y))
        
    def update(self, sec):
        """
        Updates player position etc
        sec: Time in seconds since last update """
        self.position[0] += self.speed[0] * sec
        self.position[1] += self.speed[1] * sec
        
        self.speed[0] += self.direction[0] * (self.acceleration * sec) # Update speed with acceleration
        self.speed[1] += self.direction[1] * (self.acceleration * sec) # TODO: Needs friction
        
        if self.speed[0] > self.maxSpeed: # Make sure speed is within limit
            self.speed[0] = self.maxSpeed
        if self.speed[0] < self.maxSpeed * -1:
            self.speed[0] = self.maxSpeed * -1
            
        if self.speed[1] > self.maxSpeed:
            self.speed[1] = self.maxSpeed
        if self.speed[1] < self.maxSpeed * -1:
            self.speed[1] = self.maxSpeed * -1
        
        if(self.position[0] + self.radius > WINDOW_WIDTH or 
           self.position[0] - self.radius < 0 or 
           self.position[1] + self.radius > WINDOW_HEIGHT or
           self.position[1] - self.radius < 0): # We are out of bounds, go back
            self.speed[0] *= -1
            self.speed[1] *= -1 # TODO: Direction does different things in Player and Particle, could fix this
        
        
    def flipPolarity(self):
        """
        Flips between matter and antimatter """
        self.matter = not self.matter # TODO: Change colour here too
    
class ParticleManager:
    def __init__(self, maxParticles, matColor, antiColor, radius, maxSpeed, attractRadius, force, player, spawnRate, explosionMan):
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
        self.explosionMan = explosionMan
        
        self.aliveList = [] # List of particles currently alive
        self.deadList = [] # List of all particles currently dead
        self.lastSpawn = 0.0 # Time since last spawn

        for i in range(maxParticles): # All particles start off dead so add them to dead list
            matter = True # (i % 2 == 0) # Half matter, half antimatter
            if matter:
                color = matColor
            else:
                color = antiColor
            part = Particle(radius, maxSpeed, matter, attractRadius, force, color)
            self.deadList.append(part)
            
    def spawnParticle(self):
        """ 
        Spawns a particle if we aren't at the max limit. Particle is spawned at a random location
        outside the range of any other particles or player and has no momentum
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
            part.speed = [0,0]
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
            oldPos = copy.deepcopy(part1.position)
            part1.update(sec)
            for j in range(i+1, len(self.aliveList)): # Check all the ones after this particle for collision
                part2 = self.aliveList[j]
                collide = part1.checkCollision(part2.position, part2.radius, part2.attractRadius)
                if collide == 1: # Full on collision
                    if part1.matter == part2.matter: # Same stuff so just bounce
                        part1.collide(part2)
                        part1.position = oldPos
                    else: # Uh oh... things are gonna blow up here
                        toDie.append(i) # Marked for death
                        toDie.append(j) # TODO: Implement explosions
                        pos1 = self.aliveList[i].position
                        pos2 = self.aliveList[j].position # Make explosion halfway between both
                        epos = [pos1[0] - ((pos1[0] - pos2[0]) / 2), pos1[1] - ((pos1[1] - pos2[1]) / 2)]
                        explosionMan.addExplosion(epos)
                elif collide == 0 and part1.matter is not part2.matter: # Attract range and attractive (pretty little particles)
                    part1.attract(part2)
            
            collide = part1.checkCollision(player.position, player.radius, player.attractRadius) # Check proximity to player
            if collide == 1: # TODO: Need to check player collisions
                player.collide(part1, False)
            if collide == 0:
                player.attract(part1, False)
        # Each time we remove one from alive, the counter drops
        toDie.sort() # So if we sort it first, we can use an offset of i
        for i in range(len(toDie)):
            self.deadList.append(self.aliveList[toDie[i] - i])
            del self.aliveList[toDie[i] - i]
        # Now that we have tried to kill our particles, lets see if we can ressurect a few
        if len(self.deadList) > 0:
            self.lastSpawn += sec
            if self.lastSpawn > self.spawnRate:
                self.spawnParticle()
                self.lastSpawn = 0.0
    
    def draw(self, screen):
        for alive in self.aliveList:
            alive.draw(screen)

class Ememy(Particle):
    def __init__(self, radius, color):
        Particle.__init__(self, radius, 0, True, 0, 0, color)
        
class EnemyManager(ParticleManager):
    def __init__(self, maxEnemies, color, radius, spawnRate, explosionMan):
        """
        Pretty much just a modified ParticleManager with some values set to 0 """
        ParticleManager.__init__(self, maxEnemies, color, color, radius, 0, 0, 0, player, spawnRate, explosionMan)
       
    def update(self, sec):
        i = 0
        offset = 0
        limit = len(self.aliveList)
        while i < limit: # Loop through alive enemies to see if any are getting blown up
            e = self.aliveList[i - offset]
            die = explosionMan.checkCollision(e.position, e.radius)
            if die: # Bogey down
                self.deadList.append(e)
                del self.aliveList[i - offset]
                offset += 1
            i += 1
        
        if len(self.deadList) > 0: # Bring the little beggers back
            self.lastSpawn += sec
            if self.lastSpawn > self.spawnRate:
                self.spawnParticle()
                self.lastSpawn = 0

class Explosion:
    def __init__(self, maxTime, growthRate, color, position):
        self.maxTime = maxTime # Time in seconds to stay alive
        self.growthRate = growthRate # Rate to grow per second
        self.color = color
        self.position = position
        self.radius = 0.0 # Start with 0 radius
        self.aliveTime = 0.0 # Only just born
    
    def update(self, sec):
        """
        Returns True if still alive, False if time is up """
        self.aliveTime += sec
        if self.aliveTime >= self.maxTime:
            return False
        self.radius += self.growthRate * sec
        return True
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)
        
class ExplosionManager:
    def __init__(self, maxTime, growthRate, color):
        self.active = [] # All active explosions (none to start)
        self.maxTime = maxTime
        self.growthRate = growthRate
        self.color = color
        
    def addExplosion(self, position):
        expl = Explosion(self.maxTime, self.growthRate, self.color, position)
        self.active.append(expl) # TODO: Maybe best to keep a record of dead explosions and use them instead of creating new every time
    
    def update(self, sec):
        i = 0
        offset = 0 # number removed, have to offset list by
        size = len(self.active) # Don't use for loop because we need index and offset
        while i < size:
            alive = self.active[i - offset].update(sec)
            if not alive:
                del self.active[i - offset]
                offset += 1
            i += 1
    
    def draw(self, screen):
        for exp in self.active:
            exp.draw(screen)
    
    def checkCollision(self, pos, radius):
        """ Checks to see if any explosions are within this range 
        Returns True if there is a collision, False if not """
        for exp in self.active:
            x1, y1 = exp.position
            x2, y2 = pos
            dist = ((x1 - x2) ** 2 + (y2 - y1) ** 2) ** 0.5
            if dist < radius + exp.radius:
                return True
        return False
            
def input(events): # Handles input
    moveDir = player.direction # Direction to move player based on input
    for event in events:
        if event.type == QUIT: # Quit event
            sys.exit(0)
        
        if event.type == KEYDOWN:
            if event.key == KEY_UP:
                moveDir[1] -= 1
            elif event.key == KEY_DOWN:
                moveDir[1] += 1
            elif event.key == KEY_LEFT:
                moveDir[0] -= 1
            elif event.key == KEY_RIGHT:
                moveDir[0] += 1
        
        elif event.type == KEYUP:
            if event.key == KEY_UP:
                moveDir[1] += 1
            elif event.key == KEY_DOWN:
                moveDir[1] -= 1
            elif event.key == KEY_LEFT:
                moveDir[0] += 1
            elif event.key == KEY_RIGHT:
                moveDir[0] -= 1

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
explosionMan = ExplosionManager(EXPLOSION_MAXTIME, EXPLOSION_GROWTHRATE, EXPLOSION_COLOR)
player = Player(PLAYER_RADIUS , playerSprite, PLAYER_ATTRACTRADIUS, PLAYER_FORCE, PLAYER_MAXSPEED, PLAYER_ACCELERATION)
particleMan = ParticleManager(MAX_PARTICLES, MAT_COLOR, ANTI_COLOR, PARTICLE_RADIUS, PARTICLE_MAXSPEED, PARTICLE_ATTRACTRADIUS, PARTICLE_FORCE, player, PARTICLE_SPAWNRATE, explosionMan)
particleMan.spawnAll()
enemyMan = EnemyManager(MAX_ENEMIES, ENEMY_COLOR, ENEMY_RADIUS, ENEMY_SPAWNRATE, explosionMan)
enemyMan.spawnAll()

clock = pygame.time.Clock()

while 1: # main loop
    input(pygame.event.get()) # Get input
    ms = clock.tick_busy_loop() # Time since last update in ms
    secs = ms / 1000.0 # Time in seconds
    player.update(secs)
    particleMan.update(secs)
    explosionMan.update(secs)
    enemyMan.update(secs)
    
    screen.fill((0,0,0))
    
    explosionMan.draw(screen)
    player.draw(screen)
    enemyMan.draw(screen)
    particleMan.draw(screen)

    pygame.display.flip() # Update changes to screen