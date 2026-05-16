# Importing pygame
import pygame

# Importing from the rooms script
from rooms import Rooms


class Player:
    
    def __init__(self):
    
        # Variables
        self.player_movement_speed: int = 65
        self.dodge_roll_mulitplier: int = 5
        self.dodge_roll_duration: int = 3
        self.wall_colide = False


    def input_processing(self):
        
        # Key input
        key = pygame.key.get_pressed()
        direction: pygame.Vector2 = pygame.Vector2(0, 0)

        # Direction
        if key[pygame.K_w] == True:
            direction.y = -1
        
        if key[pygame.K_s] == True:
            direction.y = 1

        if key[pygame.K_a] == True:
            direction.x = -1

        if key[pygame.K_d] == True:
            direction.x = 1 
        

        # Direction normalization
        if direction != pygame.Vector2(0, 0):
            direction = direction.normalize()

        return key, direction


    def entrance(self, player_hitbox, room) -> list:

        # Sorry for the spaghetti code, idk how else to do this, because tha match function only processes == operations, but not >/< operations
        if player_hitbox.x < 100:
            return ["x", 1400, (room[0] - 1, room[1])]
        if player_hitbox.x > 1400:
            return ["x", 100, (room[0] + 1, room[1])]

        if player_hitbox.y < 70:
            return ["y", 750, (room[0], room[1] - 1)]
        if player_hitbox.y > 750:
            return ["y", 70, (room[0], room[1] + 1)]
        

        # Dw about this
        return [None]

    def colliding(self, player_hitbox, prev_pos, delta, direction, rooms_dict, room, speed_boost_multiplier):

        # Checks if player is colliding with wall
        self.wall_colide = Rooms().collision(player_hitbox, rooms_dict, room)

        room_entered = False

        # If exiting room
        if self.wall_colide == "Entrance":

            room_entered = True

            entrance_vars: list = Player().entrance(player_hitbox, room)

            room = tuple(entrance_vars[2])

            if entrance_vars[0] == "x":
                player_hitbox.x = entrance_vars[1]
            else:
                player_hitbox.y = entrance_vars[1]
        

        # Move player, if player if now colliding with wall, cancel
        player_hitbox.x += direction.x * self.player_movement_speed * speed_boost_multiplier * delta
        wall_colide = Rooms().collision(player_hitbox, rooms_dict, room)

        if wall_colide == "Wall":
            player_hitbox.x = prev_pos.x
        else:
            prev_pos.x = player_hitbox.x


        # Same thing, but for the y axis
        player_hitbox.y += direction.y * self.player_movement_speed * speed_boost_multiplier * delta
        wall_colide = Rooms().collision(player_hitbox, rooms_dict, room)

        if wall_colide == "Wall":
            player_hitbox.y = prev_pos.y
        else:
            prev_pos.y = player_hitbox.y

        
        return prev_pos, player_hitbox, room, room_entered

    
    def dodge_roll(self, dodge_roll_cooldown, key) -> bool:

        # Dodge roll
        if dodge_roll_cooldown <= 0:
            if key[pygame.K_SPACE] == True:
                return True
        
        return False


    def speed_boost(self, boost_timer, dodge_roll_initiated) -> tuple[float, float]:

        # Deafult value
        boost_multiplier = 1

        # Starts speed boost timer
        if dodge_roll_initiated == True:
            boost_timer = self.dodge_roll_duration


        # Actually applies speed boost
        if boost_timer > 0:
            boost_multiplier = self.dodge_roll_mulitplier

        return boost_multiplier, boost_timer


    # Runs the class functions
    def run(self, player_hitbox, dodge_roll_cooldown, prev_pos, delta, rooms_dict, room, speed_boost_timer, screen):

        key, direction = Player().input_processing()

        dodge_roll_initiated: bool = Player().dodge_roll(dodge_roll_cooldown, key)
        speed_boost_multiplier, speed_boost_timer = Player().speed_boost(speed_boost_timer, dodge_roll_initiated)
       
        prev_pos, player_hitbox, room, room_entered = Player().colliding(player_hitbox, prev_pos, delta, direction, rooms_dict, room, speed_boost_multiplier)

        pygame.draw.rect(screen, (0, 255, 175), player_hitbox)

        return dodge_roll_initiated, prev_pos, room, speed_boost_multiplier, speed_boost_timer, room_entered
