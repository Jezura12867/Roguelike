# Importing libraries
import pygame
from random import randint

# Importing from other scripts
from sprites import Player
from map import Tiles
from guns import GunSystem


# Global variables
SCREEN_WIDTH: int = 1550
SCREEN_HEIGHT: int = 900
PLAYER_SIZE: int = 64
BULLET_SIZE: int = 8


# Pygame variables
clock = pygame.time.Clock()
screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

icon_sprite: pygame.Surface = pygame.image.load("Assets/Icon.png")
icon_sprite.set_colorkey("White")
icon: None = pygame.display.set_icon(icon_sprite)
title: None = pygame.display.set_caption("Rougeu liek")

# Sprites
player_hitbox = pygame.rect.Rect((SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2, PLAYER_SIZE, PLAYER_SIZE))
gun = pygame.rect.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 32, 16))
bullet = pygame.rect.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, BULLET_SIZE, BULLET_SIZE))



# The game
class Game:

    def __init__(self) -> None:
        pass

    def main(self) -> None:

        
        # NOTE_ TO SELF: CHANGE THESE NUMBERS
        # Decides, what room type you begin in
        map_num: int = 1
        
        bullet_spawned_and_dir: list = [False, 0]
        bullet_dir: int = 1
        prev_pos: list = [player_hitbox.x, player_hitbox.y]
        running = True
        delta: float = 1.0


        # Sets dodge cooldown
        dodge_roll_cooldown: int = 500

        # Tho main game loop
        while running:

            # Makes the screen gray
            screen.fill((130, 130, 130))          


            # Functions
            Tiles().run(screen, player_hitbox)
            colliding_walls_player = Tiles().collision(player_hitbox)
            player_movement_vars = Player().run(player_hitbox, dodge_roll_cooldown, prev_pos, delta)
            bullet_spawned_and_dir = GunSystem().run(gun, player_hitbox, bullet, SCREEN_WIDTH, SCREEN_HEIGHT, bullet_spawned_and_dir[0], bullet_dir)

            # Var updatring
            in_a_dodge_roll = player_movement_vars[0]
            if colliding_walls_player != True:
                prev_pos = player_movement_vars[1]
            

            bullet_dir = bullet_spawned_and_dir[1]
            
            # Dodge management
            dodge_roll_cooldown -= 1
            if in_a_dodge_roll == True:
                dodge_roll_cooldown = 120


            # Rendering
            pygame.draw.rect(screen, (0, 255, 175), player_hitbox)
            pygame.draw.rect(screen, (200, 200, 0), gun)
            if bullet_spawned_and_dir[0] == True:
                pygame.draw.rect(screen, (200, 200, 0), bullet)


            # Quit function
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                    quit()
            

            # 60 fps; updating the screen
            delta = clock.tick(60) / 100
            pygame.display.flip()

            


# Checks if running from this file
if __name__ == "__main__":
    Game().main()
