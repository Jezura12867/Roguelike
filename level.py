# Importing
import pygame
from sprites import Cube

# Manages, you guessed it, walls
class Walls:
    
    def show(screen, map_num, player):
        
        # Variables
        cubes = pygame.sprite.Group()
        map_tile_size = 64
        cube_global = None


        # Maps -----------------------------------------------------------------------------------------------------------------------------------------------------------------
        map1 = [
            "                               ",
            "                               ",
            "                               ",
            "                               ",
            "                               ",
            "                               ",
            "                               ",
            "                               ",
            "                               ",
            "                               ",
            "                               ",
            "                               ",
            "                               ",
            "                               ",
            "                               ",
            "                               ",
            "                               ",
            "                               ",
        ]
        map2 = [
            "                               ",
            "                               ",
            "                               ",
            "                               ",
            "                               ",
            "                               ",
            "                               ",
            "                               ",
            "                 XX            ",
            "                 XX            ",
            "                               ",
            "                               ",
            "                               ",
            "                               ",
            "                               ",
            "                               ",
            "                               ",
            "                               ",
        ]
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        
        # MAkes a list of maps
        maps = [map1, map2]


        # Sets the player's state of collision to False
        player_collision = False

        # Checks each tile individualy
        for cislo_radku, radek in enumerate(maps[map_num]):
            for cislo_sloupce, bunka in enumerate(radek):

                if bunka == "X":

                    # Defining cubes
                    x = cislo_sloupce * map_tile_size / 1.3 + 2
                    y = cislo_radku * map_tile_size / 1.325
                    cube = Cube((x, y), map_tile_size)
                    cubes.add(cube)
                    

                    # Rendering cubes
                    cubes.draw(screen)


                    # Player collision
                    cube_global = cube
                    if pygame.Rect.colliderect(player, cube_global) == True:
                        player_collision = True
                        

        return player_collision

        