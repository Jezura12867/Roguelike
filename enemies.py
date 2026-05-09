import pygame


class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        self.enemy_dict = {}  

    def spawn(self):

        SCREEN_WIDTH: int = 1536
        SCREEN_HEIGHT: int = 900

        # Enemy template
        enemy_hitbox = pygame.rect.Rect((SCREEN_WIDTH / 1.75, SCREEN_HEIGHT / 2, 55, 55))

        # Spawns in enemies
        self.enemy_dict.update({0: enemy_hitbox, 1: pygame.rect.Rect((SCREEN_WIDTH / 1.5, SCREEN_HEIGHT / 2, 55, 55)), 2: pygame.rect.Rect((SCREEN_WIDTH / 1.25, SCREEN_HEIGHT / 2, 55, 55))})

        return self.enemy_dict   


    def for_this_clone(self, enemy_dict, screen, id):

        # Defines current clone
        hitbox = enemy_dict.get(id)

        hitbox.x += id * 1.25

        # Clone rendering
        pygame.draw.rect(screen, (240, 0, hitbox.x / 10), hitbox)
  

    def run(self, screen, enemy_dict):

        enemy_id_count = 0

        # ID, hitbox, state
        enemy_id_count = len(enemy_dict)

        for i in range(enemy_id_count):
            Enemy().for_this_clone(enemy_dict, screen, i)

        return enemy_dict

