# Importing
import pygame
from sprites import Cube, Entrance, Enemy
from map import Rooms
from random import randint

class Tiles:

    def __init__(self) -> None:

        super.__init__

        self.tiles = pygame.sprite.Group()
        self.exits = pygame.sprite.Group()
        self.tile_size = 64

    def render(self, screen, rooms_dict, room):

        # Defines what the room type is based on coords
        rooms_vars = Rooms().main(rooms_dict, room)


        # Idk, if there's a better way to do this, if yes, I'll change thos
        map = rooms_vars[0][0]
        enemy_spawn_random_int = rooms_vars[0][1]
        rooms_dict = rooms_vars[1]
        room = rooms_vars[2]


        # Renders room
        for row, blank in enumerate(map):
            for collum, cell in enumerate(blank):
                if cell == "X":
                    x = collum * self.tile_size
                    y = row * self.tile_size

                    tile = Cube((x, y), self.tile_size)
                    self.tiles.add(tile)
                
                if cell == "E":
                    x = collum * self.tile_size
                    y = row * self.tile_size

                    tile = Entrance((x, y), self.tile_size)
                    self.exits.add(tile)
                
                if cell == "S" and (collum - row) % enemy_spawn_random_int == 0:
                        x = collum * self.tile_size
                        y = row * self.tile_size

                        tile = Enemy((x, y), self.tile_size)
                        self.exits.add(tile)



        self.tiles.draw(screen)
        self.exits.draw(screen)

        return rooms_dict
        
    
    def collision(self, player_hitbox, rooms_dict, room):

        # Defines what the room type is based on coords
        map_vars = Rooms().main(rooms_dict, room)

        map = map_vars[0][0]
        room = map_vars[1]

        collided_objects = []


        # Checks every tile that is a wall
        for row, blank in enumerate(map):
            for collum, cell in enumerate(blank):

                # If cell is a wall
                if cell == "X":
                    x = collum * self.tile_size
                    y = row * self.tile_size

                    tile = Cube((x, y), self.tile_size)

                    if  pygame.Rect.colliderect(player_hitbox, tile.rect):
                        collided_objects.append("Wall")
                    
                # If cell is an entrance
                if cell == "E":
                    x = collum * self.tile_size
                    y = row * self.tile_size

                    tile = Entrance((x, y), self.tile_size)

                    if pygame.Rect.colliderect(player_hitbox, tile.rect):
                        collided_objects.append("Entrance")
        

        # [I'm surprised that this isn't heavily nested]
        # Returns type of collision
        if collided_objects == []:
            return False
        

        # Code prioritises entrances over walls in terms of collision
        if "Entrance" in collided_objects:
            return "Entrance"
        
        return "Wall"

