# Importing
import pygame

from rooms import Tiles


class Player:
    
    def __init__(self) -> None:

        super().__init__()
    
        # Variables
        self.player_movement_speed: int = 50
        self.dodge_roll_mulitplier: int = 25
        self.wall_colide = False


    def input_processing(self):
        
        # Key input
        key = pygame.key.get_pressed()
        direction: list = [0, 0]

        # Direction
        if key[pygame.K_w] == True:
            direction[1] = -1
        
        if key[pygame.K_s] == True:
            direction[1] = 1

        if key[pygame.K_a] == True:
            direction[0] = -1

        if key[pygame.K_d] == True:
            direction[0] = 1 
        
        return key, direction


    def entrance(self, player_hitbox, room):

        # Sorry for the spaghetti code, idk how else to do this, because tha match function only processes == operations, but not >/< operations
        if player_hitbox.x < 100:
            return "x", 1400, (room[0] - 1, room[1])
        if player_hitbox.x > 1400:
            return "x", 100, (room[0] + 1, room[1])

        if player_hitbox.y < 70:
            return "y", 750, (room[0], room[1] - 1)
        if player_hitbox.y > 750:
            return "y", 70, (room[0], room[1] + 1)


    def colliding(self, player_hitbox, prev_pos, delta, direction, rooms_dict, room, has_speed_boost):

        # Checks if player is colliding with wall
        self.wall_colide = Tiles().collision(player_hitbox, rooms_dict, room)

        if self.wall_colide == "Entrance":
            entrance_vars: tuple = Player().entrance(player_hitbox, room)

            room = tuple(entrance_vars[2])

            if entrance_vars[0] == "x":
                player_hitbox.x = entrance_vars[1]
            else:
                player_hitbox.y = entrance_vars[1]
        

        if has_speed_boost == True:
            speed_boost_multiplier = 7.5
        else:
            speed_boost_multiplier = 1
        

        # Move player, if player if now colliding with wall, cancel
        player_hitbox.x += direction[0] * self.player_movement_speed * speed_boost_multiplier * delta
        wall_colide = Tiles().collision(player_hitbox, rooms_dict, room)

        if wall_colide == "Wall":
            player_hitbox.x = prev_pos[0]
        else:
            prev_pos[0] = player_hitbox.x


        # Same thing, but for the y axis
        player_hitbox.y += direction[1] * self.player_movement_speed * speed_boost_multiplier * delta
        wall_colide = Tiles().collision(player_hitbox, rooms_dict, room)

        if wall_colide == "Wall":
            player_hitbox.y = prev_pos[1]
        else:
            prev_pos[1] = player_hitbox.y

        
        return prev_pos, player_hitbox, room

    
    def roll(self, dodge_roll_cooldown, delta, key, direction):

        # Dodge roll
        if dodge_roll_cooldown <= 0:
            if key[pygame.K_SPACE] == True:
                return True
        
        return False


    def speed_boost(self, speed_boost_timer, in_a_dodge_roll):

        if in_a_dodge_roll == True:
            speed_boost_timer = 3


        # Speed boost
        if speed_boost_timer <= 0:
            return False, speed_boost_timer
        
        return True, speed_boost_timer


    # Runs the class functions
    def run(self, player_hitbox, dodge_roll_cooldown, prev_pos, delta, rooms_dict, room, speed_boost_timer):

        input_vars: tuple = Player().input_processing()

        key = input_vars[0]
        direction: list = input_vars[1]

        in_a_dodge_roll: bool = Player().roll(dodge_roll_cooldown, delta, key, direction)
        has_speed_boost, speed_boost_timer = Player().speed_boost(speed_boost_timer, in_a_dodge_roll)
       

        prev_pos, player_hitbox, room = Player().colliding(player_hitbox, prev_pos, delta, direction, rooms_dict, room, has_speed_boost)

        return in_a_dodge_roll, prev_pos, room, has_speed_boost, speed_boost_timer
