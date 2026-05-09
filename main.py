# Importing pygame
import pygame

# Importing from other scripts
from player import Player
from enemies import Enemy
from guns import GunSystem
from rooms import Rooms


# Global variables
SCREEN_WIDTH: int = 1536
SCREEN_HEIGHT: int = 900
SCREEN_PARAMETERS: tuple = SCREEN_WIDTH, SCREEN_HEIGHT
PLAYER_SIZE: float = 55
BULLET_SIZE: int = 8
BACKGROUND_COLOR = (127, 127, 127)

# Pygame variables
clock = pygame.time.Clock()
screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Top bar variables
icon_sprite: pygame.Surface = pygame.image.load("Assets/Icon.png")
icon_sprite.set_colorkey("White")
icon: None = pygame.display.set_icon(icon_sprite)
title: None = pygame.display.set_caption("Rougeu liek")

# Sprites
player_hitbox = pygame.rect.Rect((SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2, PLAYER_SIZE, PLAYER_SIZE))
gun_rect = pygame.rect.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 32, 16))
gun_image = pygame.image.load("Assets/gun.png").convert()
bullet = pygame.rect.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, BULLET_SIZE, BULLET_SIZE))

gun_image.set_colorkey("White")


# The game
class Game:

    def __init__(self):
        
        self.bullet_spawned: bool = False
        self.bullet_dir = pygame.Vector2(0, 0)
        self.prev_pos = pygame.Vector2(player_hitbox.x, player_hitbox.y)
        self.dodge_roll_cooldown: int = 0
        self.dodge_roll_initiated: bool = False
        self.speed_boost_timer: float = 0
        self.speed_boost_multiplier: float = 1
        self.room_entered: bool = False
        self.enemy_dict = {}

    
    def on_enter_room(self):

        bullet_spawned = False

        return Enemy().spawn(), bullet_spawned


    def process(self):

        # Var assigning
        running = True
        delta: float = 0.0
        rooms_dict = {}
        room = 0, 0

        # Initial spawn
        self.enemy_dict, self.bullet_spawned = Game().on_enter_room()
    
        # Tho main game loop
        while running:


            # Sets the background color
            screen.fill(BACKGROUND_COLOR)

            # Functions
            rooms_dict = Rooms().render(screen, rooms_dict, room)
            player_vars = Player().run(player_hitbox, self.dodge_roll_cooldown, self.prev_pos, delta, rooms_dict, room, self.speed_boost_timer, screen)
            self.enemy_dict = Enemy().run(screen, self.enemy_dict)

            
            rooms_vars = rooms_dict, room
            bullet_info = self.bullet_spawned, self.bullet_dir
            self.bullet_spawned, self.bullet_dir = GunSystem().run(gun_rect, player_hitbox, bullet, SCREEN_PARAMETERS, bullet_info, gun_image, screen, rooms_vars)


            # Player vars
            self.dodge_roll_initiated, self.prev_pos, room, self.speed_boost_multiplier, self.speed_boost_timer, self.room_entered = player_vars

            # Dodge management
            self.dodge_roll_cooldown -= 1

            if self.dodge_roll_initiated == True:
                self.dodge_roll_cooldown = 120

            # Speed boost timer ticks down
            self.speed_boost_timer -= 1


            # Room entrance logic
            if self.room_entered == True:
                self.enemy_dict, self.bullet_spawned = Game().on_enter_room()

            # Quit function
            running = Game().quitting()


            # 60 fps; updating the screen
            delta = clock.tick(60) / 100
            pygame.display.flip()
    
    def quitting(self):

        # Quits the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # Doesn't quit the game
        return True


# Checks if running from this file
if __name__ == "__main__":
    Game().process()
