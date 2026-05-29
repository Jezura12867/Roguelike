# Importing pygame
import pygame

# Imports randint and the Map class
from random import randint
from rooms import Rooms
from map import Map


class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        self.TILE_SIZE: int = 32
        self.ENEMY_MOVE_SPEED: int = 50
        self.enemy_dict = {}  

    def spawn(self, rooms_dict, room_pos):

        enemy_count_range = 2, 5

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

            self.enemy_dict.update({i: pygame.rect.Rect((temporary_spawn_location[1], temporary_spawn_location[0], 54, 55))})

        return self.enemy_dict
    

    def enemy_to_target(self, clone_hitbox, id, rooms_dict, room_coordinates, enemy_dict, enemies_previous_pos_dict, enemy_to_update, delta):

        # Sets the target and direction 
        target = pygame.Vector2(69, 77)
        enemy_is_enemy = True
        direction = target - pygame.Vector2(clone_hitbox.x, clone_hitbox.y)

        enemy_target_snap_distance = 3

        # Snaps to target if close enough
        if abs(direction.x) < enemy_target_snap_distance or abs(direction.y) < enemy_target_snap_distance:
            clone_hitbox.x, clone_hitbox.y = target

        # Normalizes direction and gets previous direction
        direction = direction.normalize() if direction != pygame.Vector2(0, 0) else direction
        previous_pos = enemies_previous_pos_dict.get(id) if enemies_previous_pos_dict.get(id) != None else pygame.Vector2(0, 0)

        # If the clone is at its target, don't move
        if target == pygame.Vector2(clone_hitbox.x, clone_hitbox.y):
            return

        # Does clone collide with wall?
        wall_colide = Rooms().collision(clone_hitbox, rooms_dict, room_coordinates, enemy_dict, enemy_is_enemy)
        
        # Move enemy, if enemy if now colliding with wall, cancel
        clone_hitbox.x += direction.x * self.ENEMY_MOVE_SPEED * delta
        wall_colide = Rooms().collision(clone_hitbox, rooms_dict, room_coordinates, enemy_dict, enemy_is_enemy)

        if wall_colide == "Wall":
            clone_hitbox.x = previous_pos.x
        else:
            previous_pos.x = clone_hitbox.x


        # Same thing, but for the y axis
        clone_hitbox.y += direction.y * self.ENEMY_MOVE_SPEED * delta
        wall_colide = Rooms().collision(clone_hitbox, rooms_dict, room_coordinates, enemy_dict, enemy_is_enemy)

        if wall_colide == "Wall":
           clone_hitbox.y = previous_pos.y
        else:
            previous_pos.y = clone_hitbox.y

        # Cycles through enemies one at a time each frame. If its id matches, update the previous pos of the enemy
        if enemy_to_update == id:
            enemies_previous_pos_dict.update({id: previous_pos})


    def for_this_clone(self, enemy_dict, screen, id, bullet, bullet_spawned, enemies_to_kill, rooms_dict, room_coordinates, enemies_previous_pos_dict, enemy_to_update, delta):

        # Defines current clone
        clone_hitbox = enemy_dict.get(id)

        # Only execute if enemy is still alive
        if clone_hitbox == None:
            return bullet_spawned, enemies_to_kill

        # If collides with bullet, die
        if pygame.Rect.colliderect(bullet, clone_hitbox) and bullet_spawned:
            bullet_spawned = False
            enemies_to_kill.append(id)

        self.enemy_to_target(clone_hitbox, id, rooms_dict, room_coordinates, enemy_dict, enemies_previous_pos_dict, enemy_to_update, delta)

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


    def run(self, screen, enemy_dict, bullet, bullet_spawned, room_coordinates, rooms_dict, enemies_previous_pos_dict, enemy_to_update, delta):

        # Enemy related vars
        enemy_id_count = 0
        enemy_id_count = len(enemy_dict)
        enemies_to_kill = []
        enemy_to_update += 1

        if enemy_to_update > len(enemy_dict):
            enemy_to_update = 0

        # For every enemy
        for i in range(enemy_id_count):
            bullet_spawned, enemies_to_kill = Enemy().for_this_clone(enemy_dict, screen, i, bullet, bullet_spawned, enemies_to_kill, rooms_dict, room_coordinates, enemies_previous_pos_dict, enemy_to_update, delta)

        # Makes sure that if there was nothing popped, it doesn't swap anything 
        pos_popped = 127

        # Kills enemies
        for enemy in enemies_to_kill:
            pos_popped = enemy
            enemy_dict.pop(enemy)

        # Corrects the dict order
        enemy_dict = Enemy().correct_dict_order(enemy_dict, pos_popped)

        return bullet_spawned, enemy_dict, enemy_to_update
