import pygame
from random import randint
from map import Map


class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        self.enemy_dict = {}  

    def spawn(self, rooms_dict, room_pos):

        tile_size = 32
        self.enemy_dict = {}
        enemy_count_range = 2, 5

        room = Map().main(rooms_dict, room_pos)[0][0]

        spawn_locations = []

        # Checks every tile
        for row_num, blank in enumerate(room):
            for collum_num, cell in enumerate(blank):

                # If cell is a enemy spawn point
                if cell == "S":
                    spawn_locations.append((row_num * tile_size, collum_num * tile_size))

        # How many enemies will spawn in this room
        enemies_to_spawn_count = randint(enemy_count_range[0], enemy_count_range[1])


        for i in range(enemies_to_spawn_count):

            # Selects random spawn location
            temp_spawn_location = spawn_locations[randint(0, len(spawn_locations) - 1)]

            # Two enemies can't have same spawn spot
            spawn_locations.remove(temp_spawn_location)

            self.enemy_dict.update({i: pygame.rect.Rect((temp_spawn_location[1], temp_spawn_location[0], 55, 55))})

        return self.enemy_dict   


    def for_this_clone(self, enemy_dict, screen, id):

        # Defines current clone
        hitbox = enemy_dict.get(id)

        # Clone rendering
        pygame.draw.rect(screen, (0, 255, 0, 255), hitbox)
  

    def run(self, screen, enemy_dict):

        enemy_id_count = 0

        enemy_id_count = len(enemy_dict)

        for i in range(enemy_id_count):
            Enemy().for_this_clone(enemy_dict, screen, i)

        return enemy_dict

