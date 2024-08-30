import pygame

class GunSystem:

    def __init__(self) -> None:

        super.__init__
        self.bullet_spawned:bool = False
        self.gun_dir = 1
        self.bullet_dir = 0

        
        
    

    def posanddir(self, gun, player, bullet_spawned):

        # Changes direction of gun according to the mouse's
        if player.x > pygame.mouse.get_pos()[0]:
            self.gun_dir = -1
        else:
            self.gun_dir = 1
        
        if bullet_spawned == False:
            if player.x > pygame.mouse.get_pos()[0]:
                self.bullet_dir = -1
            else:
                self.bullet_dir = 1
        


        # Makes the gun follow you
        gun.x = player.x + 55 * self.gun_dir
        gun.y = player.y + 10

        # Bug patch
        if self.gun_dir == -1:
            gun.x += 35



    
    
    def shoot(self, bullet, SCREEN_WIDTH, SCREEN_HEIGHT, gun):

        # Detects if you click the mouse
        if pygame.mouse.get_pressed()[0] == True:
            self.bullet_spawned = True
        

        # Checks if bullet has spawned, if yes, changes its position; else, sets its position to the gun's
        if self.bullet_spawned == True:
            bullet.x += 10 * self.gun_dir
        else:
            bullet.x = gun.x
            bullet.y = gun.y
        
        # Despawns the bullet when it's offscreen
        if bullet.x < 0 or bullet.y < 0 or bullet.x > SCREEN_WIDTH or bullet.y > SCREEN_HEIGHT == True:
            self.bullet_spawned = False
        
        



    def run(self, gun, player, bullet, SCREEN_WIDTH, SCREEN_HEIGHT, bullet_spawned, bullet_dir):

        # Vatiables
        self.bullet_spawned = bullet_spawned
        self.bullet_dir = bullet_dir
        
        # Runs the whole function in the correct order
        GunSystem.shoot(self, bullet, SCREEN_WIDTH, SCREEN_HEIGHT, gun)
        GunSystem.posanddir(self, gun, player, bullet_spawned)
        return self.bullet_spawned, self.bullet_dir