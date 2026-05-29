# Importing pygame
import pygame

# Importing from the rooms script
from rooms import Rooms


class Player:
    
    def __init__(self):
    
        # Variables
        self.PLAYER_MOVEMENT_SPEED: int = 65
        self.DODGE_ROLL_MULTIPLIER: int = 5
        self.DODGE_ROLL_DURATION: int = 3


    def input_processing(self):
        
        # Key input
        key_pressed = pygame.key.get_pressed()
        player_direction: pygame.Vector2 = pygame.Vector2(0, 0)

        # Direction
        if key_pressed[pygame.K_w]:
            player_direction.y = -1
        
        if key_pressed[pygame.K_s]:
            player_direction.y = 1

        if key_pressed[pygame.K_a]:
            player_direction.x = -1

        if key_pressed[pygame.K_d]:
            player_direction.x = 1
        

        # Direction normalization
        if player_direction != pygame.Vector2(0, 0):
            player_direction = player_direction.normalize()

        return key_pressed, player_direction


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

    def colliding(self, player_hitbox, previous_pos, delta, player_direction, rooms_dict, room_coordinates, speed_boost_multiplier, enemy_dict):

        player_is_enemy = False

        # Checks if player is colliding with wall
        wall_colide = Rooms().collision(player_hitbox, rooms_dict, room_coordinates, enemy_dict, player_is_enemy)

        room_entered = False

        # If exiting room
        if wall_colide == "Entrance":

            room_entered = True

            entrance_vars: list = Player().entrance(player_hitbox, room_coordinates)

            room_coordinates = tuple(entrance_vars[2])

            if entrance_vars[0] == "x":
                player_hitbox.x = entrance_vars[1]
            else:
                player_hitbox.y = entrance_vars[1]
        

        # Move player, if player if now colliding with wall, cancel
        player_hitbox.x += player_direction.x * self.PLAYER_MOVEMENT_SPEED * speed_boost_multiplier * delta
        wall_colide = Rooms().collision(player_hitbox, rooms_dict, room_coordinates, enemy_dict, player_is_enemy)

        if wall_colide == "Wall":
            player_hitbox.x = previous_pos.x
        else:
            previous_pos.x = player_hitbox.x


        # Same thing, but for the y axis
        player_hitbox.y += player_direction.y * self.PLAYER_MOVEMENT_SPEED * speed_boost_multiplier * delta
        wall_colide = Rooms().collision(player_hitbox, rooms_dict, room_coordinates, enemy_dict, player_is_enemy)

        if wall_colide == "Wall":
            player_hitbox.y = previous_pos.y
        else:
            previous_pos.y = player_hitbox.y

        
        return previous_pos, player_hitbox, room_coordinates, room_entered

    
    def dodge_roll(self, dodge_roll_cooldown, key_pressed) -> bool:

        # Dodge roll
        if dodge_roll_cooldown <= 0:
            if key_pressed[pygame.K_SPACE]:
                return True
        
        return False


    def speed_boost(self, boost_timer, dodge_roll_initiated) -> tuple[float, float]:

        # Deafult value
        boost_multiplier = 1

        # Starts speed boost timer
        if dodge_roll_initiated:
            boost_timer = self.DODGE_ROLL_DURATION


        # Actually applies speed boost
        if boost_timer > 0:
            boost_multiplier = self.DODGE_ROLL_MULTIPLIER

        return boost_multiplier, boost_timer


    # Runs the class functions
    def run(self, player_hitbox, dodge_roll_cooldown, previous_pos, delta, rooms_dict, room_coordinates, speed_boost_timer, screen, enemy_dict):

        key_pressed, player_direction = Player().input_processing()

        dodge_roll_initiated: bool = Player().dodge_roll(dodge_roll_cooldown, key_pressed)
        speed_boost_multiplier, speed_boost_timer = Player().speed_boost(speed_boost_timer, dodge_roll_initiated)
       
        previous_pos, player_hitbox, room_coordinates, room_entered = Player().colliding(player_hitbox, previous_pos, delta, player_direction, rooms_dict, room_coordinates, speed_boost_multiplier, enemy_dict)

        pygame.draw.rect(screen, (0, 255, 175), player_hitbox)

        return dodge_roll_initiated, previous_pos, room_coordinates, speed_boost_multiplier, speed_boost_timer, room_entered
