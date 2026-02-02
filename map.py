# Importing
import pygame
from sprites import Cube, Entrance
from rooms import Rooms

class Tiles:

    def __init__(self) -> None:

        super.__init__

        self.tiles = pygame.sprite.Group()
        self.exits = pygame.sprite.Group()
        self.tile_size = 64

    def render(self, screen, rooms_dict):

        rooms_vars = Rooms().main(rooms_dict)

        map = rooms_vars[0]
        rooms_dict = rooms_vars[1]

        print(map)

        for row, blank in enumerate(map):
            for collum, cell in enumerate(blank):
                if cell == "X":
                    x = collum * self.tile_size / 1.3 + 2
                    y = row * self.tile_size / 1.325

                    tile = Cube((x, y), self.tile_size)
                    self.tiles.add(tile)
                
                if cell == "E":
                    x = collum * self.tile_size / 1.3 + 2
                    y = row * self.tile_size / 1.325

                    tile = Entrance((x, y), self.tile_size + 2)
                    self.exits.add(tile)

        self.tiles.draw(screen)
        self.exits.draw(screen)

        return rooms_dict
        
    
    def collision(self, player_hitbox, rooms_dict):
        map, rooms_dict = Rooms().main(rooms_dict)

        collided_objects = []

        for row, blank in enumerate(map):
            for collum, cell in enumerate(blank):
                if cell == "X":
                    x = collum * self.tile_size / 1.3 + 2
                    y = row * self.tile_size / 1.325

                    tile = Cube((x, y), self.tile_size)

                    if  pygame.Rect.colliderect(player_hitbox, tile.rect):
                        collided_objects.append("Wall")
                    
                if cell == "E":
                    x = collum * self.tile_size / 1.3 + 2
                    y = row * self.tile_size / 1.325

                    tile = Entrance((x, y), self.tile_size + 2)

                    if  pygame.Rect.colliderect(player_hitbox, tile.rect):
                        collided_objects.append("Entrance")
                
        if collided_objects == []:
            return False
        
        if "Entrance" in collided_objects:
            return "Entrance"
        
        return "Wall"

