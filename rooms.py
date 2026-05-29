# Importing pygame
import pygame

# Importing from other scripts
from static_sprites import Cube, Entrance
from map import Map

class Rooms:

    def __init__(self):

        self.tiles = pygame.sprite.Group()
        self.exits = pygame.sprite.Group()
        self.TILE_SIZE = 32


    def render(self, screen, rooms_dict, room):

        # Defines what the room type is based on coords
        rooms_vars = Map().main(rooms_dict, room)

        (map, unused_var), rooms_dict, room = rooms_vars


        # Renders room
        for row, blank in enumerate(map):
            for collum, cell in enumerate(blank):

                # IF it's a wall
                if cell == "X":
                    x = collum * self.TILE_SIZE
                    y = row * self.TILE_SIZE

                    tile = Cube((x, y), self.TILE_SIZE)
                    self.tiles.add(tile)
                
                # If it's an entrance/exit
                elif cell == "E":
                    x = collum * self.TILE_SIZE
                    y = row * self.TILE_SIZE

                    tile = Entrance((x, y), self.TILE_SIZE)
                    self.exits.add(tile)
                

        # Draws everything
        self.tiles.draw(screen)
        self.exits.draw(screen)

        return rooms_dict
        
    def individual_tile_detection(self, collum, row, cell, collide_object):

        # If cell is a wall
        if cell == "X":
            x = collum * self.TILE_SIZE
            y = row * self.TILE_SIZE

            tile = Cube((x, y), self.TILE_SIZE)

            if pygame.Rect.colliderect(collide_object, tile.rect):
                return "Wall"
            
        # If cell is an entrance
        if cell == "E":
            x = collum * self.TILE_SIZE
            y = row * self.TILE_SIZE

            tile = Entrance((x, y), self.TILE_SIZE)

            if pygame.Rect.colliderect(collide_object, tile.rect):
                return "Entrance"
            

    def collision(self, collide_object, rooms_dict, room, enemy_dict, is_enemy):

        # Defines what the z type is based on coords
        map_vars = Map().main(rooms_dict, room)

        map = map_vars[0][0]
        room = map_vars[1]

        collided_objects = []

        closest_cell = round(pygame.Vector2(collide_object.x, collide_object.y) / 1536 * 47, 0)

        closest_cell = pygame.Vector2(int(closest_cell.x), int(closest_cell.y))

        if enemy_dict != None and is_enemy == False:
            for id in enemy_dict:
                enemy_hitbox = enemy_dict.get(id)

                if pygame.rect.Rect.colliderect(enemy_hitbox, collide_object):
                    collided_objects.append("Wall")


        # Checks every tile that is a wall

        for row in range(3):

            # Defines the row count and row contents
            row_count = row + closest_cell.y
            row_count = int(row_count)
            row_contents = map[row_count]

            for collum in range(3):
                
                # Defines the collum count and collum contents
                collum_count = collum + closest_cell.x
                collum_count = int(collum_count)
                cell = row_contents[collum_count]

                tile_colliding = Rooms().individual_tile_detection(collum_count, row_count, cell, collide_object)

                if tile_colliding != None:
                    collided_objects.append(tile_colliding)
        

        # [I'm surprised that this isn't that heavily nested]
        # Returns type of collision
        if collided_objects == []:
            return False
        

        # Code prioritises entrances over walls in terms of collision
        if "Entrance" in collided_objects:
            return "Entrance"
        
        return "Wall"

