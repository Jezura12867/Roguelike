# Importing libraries
import pygame

# Importing from other scripts
from player import Player
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
        self.dodge_roll_cooldown: int = 0
        self.in_a_dodge_roll: bool = False
        self.speed_boost_timer: int = 0
        self.has_speed_boost: bool = False


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
            self.in_a_dodge_roll, self.prev_pos, room, self.has_speed_boost, self.speed_boost_timer = Player().run(player_hitbox, self.dodge_roll_cooldown, self.prev_pos, delta, rooms_dict, room, self.speed_boost_timer)
            bullet_spawned_and_dir = GunSystem().run(gun, player_hitbox, bullet, SCREEN_WIDTH, SCREEN_HEIGHT, self.bullet_spawned, self.bullet_dir)


            # Changing vars
            managed_vars = Game().var_management(colliding_walls_player, self.in_a_dodge_roll, self.prev_pos,
                                                                                self.dodge_roll_cooldown, bullet_spawned_and_dir, self.speed_boost_timer, self.has_speed_boost)

            self.in_a_dodge_roll, self.prev_pos, self.bullet_spawned, self.bullet_dir, self.dodge_roll_cooldown, self.speed_boost_timer, self.has_speed_boost = managed_vars


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

    def var_management(self, colliding_walls_player, in_a_dodge_roll, prev_pos, dodge_roll_cooldown, bullet_spawned_and_dir, speed_boost_timer, has_speed_boost):

        if colliding_walls_player != True:
            prev_pos = prev_pos
        
        bullet_spawned = bullet_spawned_and_dir[0]
        bullet_dir = bullet_spawned_and_dir[1]

        # Dodge management
        dodge_roll_cooldown -= 1
        if in_a_dodge_roll == True:
            dodge_roll_cooldown = 120

        speed_boost_timer -= 1

        
        return in_a_dodge_roll, prev_pos, bullet_spawned, bullet_dir, dodge_roll_cooldown, speed_boost_timer, has_speed_boost
    
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
