# Importing pygame
import pygame

# Imports randint and the Map class
from random import randint
from rooms import Rooms
from map import Map


class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        self.TILE_SIZE: int = 32
        self.ENEMY_MOVE_SPEED: int = 25
        self.enemy_dict = {}

    def spawn(self, rooms_dict, room_pos):
        

        enemy_count_range = 3, 5

        room_coordinates = Map().main(rooms_dict, room_pos)[0][0]

        spawn_locations = []

        # Checks every tile
        for row_num, row in enumerate(room_coordinates):
            for collum_num, cell in enumerate(row):
                # If cell is a enemy spawn point
                if cell == "S":
                    spawn_locations.append((row_num * self.TILE_SIZE, collum_num * self.TILE_SIZE))


        # How many enemies will spawn in this room
        enemies_to_spawn_count = randint(enemy_count_range[0], enemy_count_range[1])

        for i in range(enemies_to_spawn_count):

            # Selects random spawn location
            temporary_spawn_location = spawn_locations[randint(0, len(spawn_locations) - 1)]

            # Two enemies can't have same spawn spot
            spawn_locations.remove(temporary_spawn_location)

            self.enemy_dict.update({i: (pygame.rect.Rect((temporary_spawn_location[1], temporary_spawn_location[0], 54, 55)), "moving")})

        return self.enemy_dict
    

    def enemy_to_target(self, clone_hitbox, clone_state, id, rooms_dict, room_coordinates, enemy_dict, enemies_previous_pos_dict, enemy_to_update, target_dict, player_hitbox, delta):

        enemy_target_snap_distance = 10
        enemy_desired_distance_from_player = 300
        enemy_change_target_chance = 50

        if target_dict.get(id) == None:
            target_dict.update({id: pygame.Vector2(randint(10, 1400), randint(10, 800))})

        target: pygame.Vector2 = target_dict.get(id)

        enemy_is_enemy = True
        direction = target - pygame.Vector2(clone_hitbox.x, clone_hitbox.y)

        # Go away from player
        enemy_distance_from_player = pygame.Vector2(abs(clone_hitbox.x - player_hitbox.x), abs(clone_hitbox.y - player_hitbox.y))
        enemy_direction_to_player = pygame.Vector2(clone_hitbox.x - player_hitbox.x, clone_hitbox.y - player_hitbox.y).normalize()

        # Snaps to target if close enough
        if abs(clone_hitbox.x - target.x) < enemy_target_snap_distance and abs(clone_hitbox.y - target.y) < enemy_target_snap_distance:
            clone_hitbox.x, clone_hitbox.y = target
            direction = pygame.Vector2(0, 0)

        # Normalizes direction and gets previous direction
        direction = direction.normalize() if direction != pygame.Vector2(0, 0) else direction
        previous_pos = enemies_previous_pos_dict.get(id) if enemies_previous_pos_dict.get(id) != None else pygame.Vector2(0, 0)

        # Does clone collide with wall?
        wall_colide = Rooms().collision(clone_hitbox, rooms_dict, room_coordinates, enemy_dict, enemy_is_enemy)
        
        # Move enemy, if enemy if now colliding with wall, cancel
        clone_hitbox.x += direction.x * self.ENEMY_MOVE_SPEED * delta
        wall_colide = Rooms().collision(clone_hitbox, rooms_dict, room_coordinates, enemy_dict, enemy_is_enemy)

        if wall_colide == "Wall" or wall_colide == "Entrance":
            clone_hitbox.x = previous_pos.x
        else:
            previous_pos.x = clone_hitbox.x


        # Same thing, but for the y axis
        clone_hitbox.y += direction.y * self.ENEMY_MOVE_SPEED * delta
        wall_colide = Rooms().collision(clone_hitbox, rooms_dict, room_coordinates, enemy_dict, enemy_is_enemy)

        if wall_colide == "Wall" or wall_colide == "Entrance":
           clone_hitbox.y = previous_pos.y
        else:
            previous_pos.y = clone_hitbox.y

        # Cycles through enemies one at a time each frame. If its id matches, update the previous pos of the enemy
        if enemy_to_update == id:
            enemies_previous_pos_dict.update({id: previous_pos})
        
        # Fixes enemies getting stuck on walls
        if randint(0, enemy_change_target_chance) == 1:
            target = pygame.Vector2(randint(10, 1400), randint(10, 800))

        enemy_distancing_from_player_multiplier = 15

        if enemy_distance_from_player.x < enemy_desired_distance_from_player and enemy_distance_from_player.y < enemy_desired_distance_from_player:
            direction = pygame.Vector2(pygame.Vector2(clone_hitbox.x, clone_hitbox.y) - pygame.Vector2(player_hitbox.x, player_hitbox.y))
            target = pygame.Vector2(randint(5, 15) * enemy_direction_to_player.x * enemy_distancing_from_player_multiplier + clone_hitbox.x, randint(5, 15) * enemy_direction_to_player.y * enemy_distancing_from_player_multiplier + clone_hitbox.y)
    
        
        target_dict.update({id: target})

        return target_dict, clone_hitbox, clone_state


    def for_this_clone(self, enemy_dict, screen, id, bullet, bullet_spawned, enemies_to_kill: list[int], rooms_dict, room_coordinates, enemies_previous_pos_dict, enemy_to_update, player_hitbox, target_dict, delta):

        # Defines current clone
        clone_hitbox, clone_state = enemy_dict.get(id)

        # Only execute if enemy is still alive
        if clone_hitbox == None:
            return bullet_spawned, enemies_to_kill

        # If collides with bullet, die
        if pygame.Rect.colliderect(bullet, clone_hitbox) and bullet_spawned:
            bullet_spawned = False
            enemies_to_kill.append(id)
        

        target_dict, clone_hitbox, clone_state = self.enemy_to_target(clone_hitbox, clone_state, id, rooms_dict, room_coordinates, enemy_dict, enemies_previous_pos_dict, enemy_to_update, target_dict, player_hitbox, delta)

        # Clone rendering
        pygame.draw.rect(screen, (0, 255, 0, 255), clone_hitbox)

        return bullet_spawned, enemies_to_kill, target_dict


    def correct_dict_order(self, enemy_dict, pos_popped, enemies_previous_pos_dict):

        swap_occured = False

        enemy = None

        # For every enemy
        for enemy_id in range(len(enemy_dict)):
            enemy = enemy_dict.get(enemy_id)

            if enemy != None:

                enemy = enemy[0]

                enemy_key = [enemy_key for enemy_key, val in enemy_dict.items() if val[0] == enemy][0]

                # If key is further in list than an enemy that just died, bring its key's value down
                if enemy_key > pos_popped:
                    swap_occured = True
                    enemy_dict[enemy_key - 1] = enemy_dict.pop(enemy_key)
                    enemies_previous_pos_dict[enemy_key - 1] = enemies_previous_pos_dict.pop(enemy_key)
        
        # Prevents a bug where there's an enemy in the list, but cannot be seen or interacted with in game
        if len(enemy_dict) > 0:
            enemy_key = max(enemy_dict)

            if enemy != None and swap_occured:
                enemy_dict[enemy_key - 1] = enemy_dict.pop(enemy_key)
                enemies_previous_pos_dict[enemy_key - 1] = enemies_previous_pos_dict.pop(enemy_key)

            else:
                enemy_dict[len(enemy_dict)] = enemy_dict.pop(enemy_key)



    def run(self, screen, enemy_dict, bullet, bullet_spawned, room_coordinates, rooms_dict, enemies_previous_pos_dict, enemy_to_update, player_hitbox, target_dict, delta):

        # Enemy related vars
        enemy_id_count = 0
        enemy_id_count = len(enemy_dict)
        enemies_to_kill = []
        enemy_to_update += 1

        if enemy_to_update > len(enemy_dict):
            enemy_to_update = 0

        # For every enemy
        for id in range(enemy_id_count):
            bullet_spawned, enemies_to_kill, target_dict = Enemy().for_this_clone(enemy_dict, screen, id, bullet, bullet_spawned, enemies_to_kill, rooms_dict, room_coordinates, enemies_previous_pos_dict, enemy_to_update, player_hitbox, target_dict, delta)

        # Makes sure that if there was nothing popped, it doesn't swap anything 
        pos_popped = 127

        # Kills enemies
        for enemy in enemies_to_kill:
            pos_popped = enemy
            enemy_dict.pop(enemy)

        # Corrects the dict order
        Enemy().correct_dict_order(enemy_dict, pos_popped, enemies_previous_pos_dict)

        return bullet_spawned, enemy_dict, enemy_to_update, target_dict
