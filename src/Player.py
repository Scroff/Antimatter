class Player:
    def __init__(self, radius, sprite):
        self.position = (50,50)
        self.radius = radius
        self.matter = True # True if player is matter, False if he is antimatter
        self.sprite = sprite

    
    def draw(self, screen):
        """ Draws the player.
        screen: Surface to draw on """
        screen.blit(self.sprite, self.position)
        
    def update(self, ms):
        """
        Updates player position etc
        ms: Time in milliseconds since last update """
        
    def flipPolarity(self):
        """
        Flips between matter and antimatter """
        self.matter = not self.matter
        # TODO: Change colour here too