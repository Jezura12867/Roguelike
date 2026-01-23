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
        
from level import Walls


class Player:
    
    
    def movement(player_hitbox, SCREEN_WIDTH, SCREEN_HEIGHT, dodge_roll_cooldown, wall_colide, prev_pos, screen, map_num) -> bool:
        
        # Variables
        player_movement_speed: int = 5
        direction:list = [0, 0]
        prev_x = player_hitbox.x
        prev_y = player_hitbox.y
        
        
        # Key input
        key: ScancodeWrapper = pygame.key.get_pressed()


        # Movement
        if key[pygame.K_w] == True:
            direction[1] = -1
        
        if key[pygame.K_s] == True:
            direction[1] = 1

        if key[pygame.K_a] == True:
            direction[0] = -1

        if key[pygame.K_d] == True:
            direction[0] = 1     

        
        player_hitbox.x += direction[0] * player_movement_speed
        wall_colide: bool = Walls.show(screen, map_num, player_hitbox)
        if wall_colide == True:
            player_hitbox.x = prev_pos[0]
        player_hitbox.y += direction[1] * player_movement_speed

        wall_colide: bool = Walls.show(screen, map_num, player_hitbox)
        if wall_colide == True:
            player_hitbox.y = prev_pos[1]

        


        # Dodge roll
        dodge_roll_cooldown -= 1

        if dodge_roll_cooldown <= 0:
            if key[pygame.K_SPACE] == True:
                player_hitbox.x += direction[0] * player_movement_speed * 50
                player_hitbox.y += direction[1] * player_movement_speed * 50
                return True, prev_pos
        
        return False, prev_pos

        




    