# Importing
import pygame
import math

from pygame.key import ScancodeWrapper

class Cube(pygame.sprite.Sprite):

    def __init__(self, pozice, size):
    
        # Sets up the cube fromatting
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft = pozice)
        
from map import Tiles


class Player:
    
    def __init__(self) -> None:
        super.__init__
    
        # Variables
        self.player_movement_speed: int = 50
        self.dodge_roll_mulitplier: int = 25
        self.wall_colide: bool = False
    
    def input_processing(self):
        
        
        # Key input
        key = pygame.key.get_pressed()
        direction: list = [0, 0]

        # Movement
        if key[pygame.K_w] == True:
            direction[1] = -1
        
        if key[pygame.K_s] == True:
            direction[1] = 1

        if key[pygame.K_a] == True:
            direction[0] = -1

        if key[pygame.K_d] == True:
            direction[0] = 1 
        
        return key, direction


    def colliding(self, player_hitbox, prev_pos, delta, direction):


        self.wall_colide = Tiles().collision(player_hitbox)
        
        player_hitbox.x += direction[0] * self.player_movement_speed * delta
        wall_colide = Tiles().collision(player_hitbox)
        if wall_colide == True:
            player_hitbox.x = prev_pos[0]
        else:
            prev_pos[0] = player_hitbox.x
        player_hitbox.y += direction[1] * self.player_movement_speed * delta

        wall_colide: bool = Tiles().collision(player_hitbox)
        if wall_colide == True:
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

    def run(self, player_hitbox, dodge_roll_cooldown, prev_pos, delta):
        
        input_vars = Player().input_processing()

        key = input_vars[0]
        direction = input_vars[1]

        collision_vars = Player().colliding(player_hitbox, prev_pos, delta, direction)

        prev_pos = collision_vars[0]
        player_hitbox = collision_vars[1]

        in_a_dodge_roll = Player().roll(player_hitbox, dodge_roll_cooldown, delta, key, direction)

        return in_a_dodge_roll, prev_pos
