# Importing libraries
import pygame
from random import randint

# Importing from other scripts
from sprites import Player
from level import Walls
from guns import GunSystem


# Global variables
SCREEN_WIDTH: int = 1550
SCREEN_HEIGHT: int = 900


# Pygame variables
clock = pygame.time.Clock()
screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

icon_sprite: pygame.Surface = pygame.image.load("Assets/Icon.png")
icon_sprite.set_colorkey("White")
icon: None = pygame.display.set_icon(icon_sprite)
title: None = pygame.display.set_caption("Rougeu liek")

# Sprites
player_hitbox = pygame.rect.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 64, 64))
gun = pygame.rect.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 32, 16))
bullet = pygame.rect.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 8, 8))



# The game
class Game:

    def main() -> None:

        
        # NOTE_ TO SELF: CHANGE THESE NUMBERS
        # Decides, what room type you begin in
        map_num: int = 1
        
        bullet_spawned_and_dir: list = [False, 0]
        bullet_dir: int = 1
        prev_pos: list = [0, 0]


        # Sets dodge cooldown
        dodge_roll_cooldown: int = 500

        # Tho main game loop
        while True:

            # Makes the screen gray
            screen.fill((130, 130, 130))          


            # Functions
            colliding_walls_player: bool = Walls.show(screen, map_num, player_hitbox)
            if colliding_walls_player == False:
                prev_pos = [player_hitbox.x, player_hitbox.y]

            player_movement_vars: bool = Player.movement(player_hitbox, SCREEN_WIDTH, SCREEN_HEIGHT, dodge_roll_cooldown, colliding_walls_player, prev_pos, screen, map_num)
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
                    quit
            

            # 60 fps; updating the screen
            clock.tick(60)
            pygame.display.flip()

            


# Checks if running from this file
if __name__ == "__main__":
    Game.main()
