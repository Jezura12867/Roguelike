# Importing libraries
import pygame
from random import randint

# Importing from other scripts
from sprites import Player
from rooms import Tiles
from guns import GunSystem


# Global variables
SCREEN_WIDTH: int = 1536
SCREEN_HEIGHT: int = 900
PLAYER_SIZE: int = 64
BULLET_SIZE: int = 8
BACKGROUND_COLOR = (127, 127, 127)


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
        
        self.bullet_spawned: bool = False
        self.bullet_dir: int = 1
        self.prev_pos: list = [player_hitbox.x, player_hitbox.y]
        self.in_a_dodge_roll: bool = False
        self.dodge_roll_cooldown: int = 0


    def process(self):

        # Var assigning
        running = True
        delta: float = 1.0
        rooms_dict = {}
        room = 0, 0
    
        # Tho main game loop
        while running:

            # Sets the background color
            screen.fill(BACKGROUND_COLOR)          

            # Functions
            rooms_dict = Tiles().render(screen, rooms_dict, room)
            colliding_walls_player = Tiles().collision(player_hitbox, rooms_dict, room)
            player_movement_vars = Player().run(player_hitbox, self.dodge_roll_cooldown, self.prev_pos, delta, rooms_dict, room)
            bullet_spawned_and_dir = GunSystem().run(gun, player_hitbox, bullet, SCREEN_WIDTH, SCREEN_HEIGHT, self.bullet_spawned, self.bullet_dir)


            # Changing vars
            managed_vars = Game().var_management(colliding_walls_player, player_movement_vars, self.in_a_dodge_roll, self.prev_pos,
                                                                                self.dodge_roll_cooldown, bullet_spawned_and_dir)

            self.in_a_dodge_roll, self.prev_pos, self.bullet_spawned, self.bullet_dir, self.dodge_roll_cooldown, room = managed_vars


            # Quit function
            running = Game().quitting()

            # Rendering
            pygame.draw.rect(screen, (0, 255, 175), player_hitbox)
            pygame.draw.rect(screen, (200, 200, 0), gun)
            if self.bullet_spawned == True:
                pygame.draw.rect(screen, (200, 200, 0), bullet)



            # 60 fps; updating the screen
            delta = clock.tick(60) / 100
            pygame.display.flip()

    def var_management(self, colliding_walls_player, player_movement_vars, in_a_dodge_roll, prev_pos, dodge_roll_cooldown, bullet_spawned_and_dir):

        # Var updatring
        in_a_dodge_roll = player_movement_vars[0]
        if colliding_walls_player != True:
            prev_pos = player_movement_vars[1]
        
        bullet_spawned = bullet_spawned_and_dir[0]
        bullet_dir = bullet_spawned_and_dir[1]

        # Dodge management
        dodge_roll_cooldown -= 1
        if in_a_dodge_roll == True:
            dodge_roll_cooldown = 120
        
        return in_a_dodge_roll, prev_pos, bullet_spawned, bullet_dir, dodge_roll_cooldown, player_movement_vars[2]
    
    def quitting(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                return False
        
        return True




# Checks if running from this file
if __name__ == "__main__":
    Game().process()
