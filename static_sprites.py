# Importing pygame
import pygame

class Cube(pygame.sprite.Sprite):

    def __init__(self, position, size):
    
        # Sets up the cube formatting
        super().__init__()

        self.image = pygame.Surface((size, size))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft = position)


class Entrance(pygame.sprite.Sprite):

    def __init__(self, position, size):
    
        # Sets up the entrance formatting
        super().__init__()

        self.image = pygame.Surface((size, size))
        self.image.fill("blue")
        self.rect = self.image.get_rect(topleft = position)


class Enemy(pygame.sprite.Sprite):

    def __init__(self, position, size):
    
        # Sets up the enemy formatting
        super().__init__()

        self.image = pygame.Surface((size, size))
        self.image.fill("green")
        self.rect = self.image.get_rect(topleft = position)
