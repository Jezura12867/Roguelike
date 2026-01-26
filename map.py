# Importing
import pygame
from sprites import Cube

class Tiles:

    def __init__(self) -> None:

        super.__init__

        self.tiles = pygame.sprite.Group()
        self.tile_size = 64

        self.map = [
            "XXXXXXXXXXXXX   XXXXXXXXXXXXXXX",
            "X                             X",
            "X     X                       X",
            "X                             X",
            "X                             X",
            "X                             X",
            "X                             X",
            "                               ",
            "                 XX            ",
            "                 XX            ",
            "X                             X",
            "X                             X",
            "X                             X",
            "X                             X",
            "X                             X",
            "X                             X",
            "X                             X",
            "XXXXXXXXXXXXX   XXXXXXXXXXXXXXX",
        ]

    def render(self, screen, player_hitbox):
        for row, blank in enumerate(self.map):
            for collum, cell in enumerate(blank):
                if cell == "X":
                    x = collum * self.tile_size / 1.3 + 2
                    y = row * self.tile_size / 1.325

                    tile = Cube((x, y), self.tile_size)
                    self.tiles.add(tile)

        self.tiles.draw(screen)
        
    
    def collision(self, player_hitbox):

        for row, blank in enumerate(self.map):
            for collum, cell in enumerate(blank):
                if cell == "X":
                    x = collum * self.tile_size / 1.3 + 2
                    y = row * self.tile_size / 1.325

                    tile = Cube((x, y), self.tile_size)

                    if  pygame.Rect.colliderect(player_hitbox, tile.rect):
                        return True

        return False
    
    def run(self, screen, player_hitbox):
        Tiles.render(self, screen, player_hitbox)

