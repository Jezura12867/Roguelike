# Importing
import pygame
import math


class Player:
    
    def movement(player_hitbox, SCREEN_WIDTH, SCREEN_HEIGHT, dodge_roll_cooldown, wall_colide) -> bool:
    
        # Variables
        player_movement_speed: int = 5
        direction:list = [0, 0]
        
        
        # Key input
        key = pygame.key.get_pressed()


        # Movement
        if key[pygame.K_w] == True:
            player_hitbox.y -= 1 * player_movement_speed
            direction[1] = -1
        
        if key[pygame.K_s] == True:
            player_hitbox.y += 1 * player_movement_speed
            direction[1] = 1

        if key[pygame.K_a] == True:
            player_hitbox.x -= 1 * player_movement_speed
            direction[0] = -1

        if key[pygame.K_d] == True:
            player_hitbox.x += 1 * player_movement_speed
            direction[0] = 1

        # Collision
        if wall_colide == True:
            for i in range(math.ceil(abs(direction[0] * player_movement_speed))):
                if wall_colide == True:
                    player_hitbox.x += direction[0] * player_movement_speed / abs(direction[0] * player_movement_speed) * -1
        
        if wall_colide == True:    
            for i in range(math.floor(abs(direction[1] * player_movement_speed))):
                if wall_colide == True:
                    player_hitbox.y += direction[1] * player_movement_speed / abs(direction[1] * player_movement_speed) * -1


        # Dodge roll
        dodge_roll_cooldown -= 1

        if dodge_roll_cooldown <= 0:
            if key[pygame.K_SPACE] == True:
                player_hitbox.x += direction[0] * player_movement_speed * 50
                player_hitbox.y += direction[1] * player_movement_speed * 50
                return True
            else:
                return False
        else:
            return False
        



class Cube(pygame.sprite.Sprite):

    def __init__(self, pozice, size):
    
        # Sets up the cube fromatting
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft = pozice)

    