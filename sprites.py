# Importing
import pygame
import math

from pygame.key import ScancodeWrapper

class Cube(pygame.sprite.Sprite):

    def __init__(self, position, size):
    
        # Sets up the cube formatting
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft = position)

class Entrance(pygame.sprite.Sprite):

    def __init__(self, position, size):
    
        # Sets up the exit formatting
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill("blue")
        self.rect = self.image.get_rect(topleft = position)

from map import Tiles


class Player:
    
    def __init__(self) -> None:
        super.__init__
    
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

    def entrance(self, player_hitbox):

        match player_hitbox.x:
            case _ if player_hitbox.x < 100:
                return "x", 1400
            case _ if player_hitbox.x > 1400:
                return "x", 100

        match player_hitbox.y:
            case _ if player_hitbox.y < 70:
                return "y", 750
            case _ if player_hitbox.y > 750:
                return "y", 70


    def colliding(self, player_hitbox, prev_pos, delta, direction, rooms_dict):


        # Checks if player is colliding with wall
        self.wall_colide = Tiles().collision(player_hitbox, rooms_dict)

        if self.wall_colide == "Entrance":
            entrance_vars: tuple = Player().entrance(player_hitbox)

            if entrance_vars[0] == "x":
                player_hitbox.x = entrance_vars[1]
            else:
                player_hitbox.y = entrance_vars[1]

        

        # Move player, if player if now colliding with wall, cancel
        player_hitbox.x += direction[0] * self.player_movement_speed * delta
        wall_colide = Tiles().collision(player_hitbox, rooms_dict)

        if wall_colide == "Wall":
            player_hitbox.x = prev_pos[0]
        else:
            prev_pos[0] = player_hitbox.x


        # Same thing, but for the y axis
        player_hitbox.y += direction[1] * self.player_movement_speed * delta
        wall_colide = Tiles().collision(player_hitbox, rooms_dict)

        if wall_colide == "Wall":
            player_hitbox.y = prev_pos[1]
        else:
            prev_pos[1] = player_hitbox.y

        
        return prev_pos, player_hitbox

    
    def roll(self, player_hitbox, dodge_roll_cooldown, delta, key, direction):

        # Dodge roll
        dodge_roll_cooldown -= 1

        if dodge_roll_cooldown <= 0:
            if key[pygame.K_SPACE] == True:
                player_hitbox.x += direction[0] * self.player_movement_speed * self.dodge_roll_mulitplier * delta
                player_hitbox.y += direction[1] * self.player_movement_speed * self.dodge_roll_mulitplier * delta
                return True
        
        return False


    # Runs the class functions
    def run(self, player_hitbox, dodge_roll_cooldown, prev_pos, delta, rooms_dict):

        input_vars: tuple = Player().input_processing()

        key: ScancodeWrapper = input_vars[0]
        direction: list = input_vars[1]

        collision_vars = Player().colliding(player_hitbox, prev_pos, delta, direction, rooms_dict)

        prev_pos = collision_vars[0]
        player_hitbox = collision_vars[1]

        in_a_dodge_roll: bool = Player().roll(player_hitbox, dodge_roll_cooldown, delta, key, direction)

        return in_a_dodge_roll, prev_pos
