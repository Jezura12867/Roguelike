# Importing pygame
import pygame

# Imports randint and the Map class
from random import randint
from map import Map


class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        self.enemy_dict = {}  

    def spawn(self, rooms_dict, room_pos):

        TILE_SIZE = 32
        self.enemy_dict = {}
        enemy_count_range = 2, 5

        room_coordinates = Map().main(rooms_dict, room_pos)[0][0]

        spawn_locations = []

        # Checks every tile
        for row_num, row in enumerate(room_coordinates):
            for collum_num, cell in enumerate(row):
                # If cell is a enemy spawn point
                if cell == "S":
                    spawn_locations.append((row_num * TILE_SIZE, collum_num * TILE_SIZE))


        # How many enemies will spawn in this room
        enemies_to_spawn_count = randint(enemy_count_range[0], enemy_count_range[1])

        for i in range(enemies_to_spawn_count):

            # Selects random spawn location
            temporary_spawn_location = spawn_locations[randint(0, len(spawn_locations) - 1)]

            # Two enemies can't have same spawn spot
            spawn_locations.remove(temporary_spawn_location)

            self.enemy_dict.update({i: pygame.rect.Rect((temporary_spawn_location[1], temporary_spawn_location[0], 55, 55))})

        return self.enemy_dict   


    def for_this_clone(self, enemy_dict, screen, id, bullet, bullet_spawned, enemies_to_kill):

        # Defines current clone
        clone_hitbox = enemy_dict.get(id)

        # Only execute if enemy is still alive
        if clone_hitbox == None:
            return bullet_spawned, enemies_to_kill

        # If collides with bullet, die
        if pygame.Rect.colliderect(bullet, clone_hitbox) and bullet_spawned:
            bullet_spawned = False
            enemies_to_kill.append(id)

        # Clone rendering
        pygame.draw.rect(screen, (0, 255, 0, 255), clone_hitbox)

        return bullet_spawned, enemies_to_kill


    def correct_dict_order(self, enemy_dict, pos_popped):

        swap_occured = False

        enemy = None

        # For every enemy
        for enemy_id in range(len(enemy_dict)):
            enemy = enemy_dict.get(enemy_id)

            if enemy != None:

                enemy_key = [enemy_key for enemy_key, val in enemy_dict.items() if val == enemy][0]

                # If key is further in list than an enemy that just died, bring its key's value down
                if enemy_key > pos_popped:
                    swap_occured = True
                    enemy_dict[enemy_key - 1] = enemy_dict.pop(enemy_key)
        
        # Prevents a bug where there's an enemy in the list, but cannot be seen or interacted with in game
        if len(enemy_dict) > 0:
            enemy_key = max(enemy_dict)

            if enemy != None and swap_occured:
                enemy_dict[enemy_key - 1] = enemy_dict.pop(enemy_key)

            else:
                enemy_dict[len(enemy_dict)] = enemy_dict.pop(enemy_key)

        
        return enemy_dict


    def run(self, screen, enemy_dict, bullet, bullet_spawned):

        enemy_id_count = 0

        enemy_id_count = len(enemy_dict)

        enemies_to_kill = []


        # For every enemy
        for i in range(enemy_id_count):
            bullet_spawned, enemies_to_kill = Enemy().for_this_clone(enemy_dict, screen, i, bullet, bullet_spawned, enemies_to_kill)

        # Makes sure that if there was nothing popped, it doesn't swap anything 
        pos_popped = 127

        # Kills enemies
        for enemy in enemies_to_kill:
            pos_popped = enemy
            enemy_dict.pop(enemy)

        # Corrects the dict order
        enemy_dict = Enemy().correct_dict_order(enemy_dict, pos_popped)

        return bullet_spawned, enemy_dict
