# Importing pygame
import pygame
import math

class GunSystem:

    def __init__(self):

        self.bullet_spawned: bool = False
        self.bullet_dir = pygame.Vector2(0, 0)
        self.bullet_speed = 15
        self.gun_player_offset = pygame.Vector2(50, 0)


    def rotate_around_pivot(self, image, angle, pivot, pos):

        # Surface is rotated image
        surface = pygame.transform.rotate(image, angle)
    
        # Image offset from pivot
        image_offset = pygame.Vector2(pivot.x, pivot.y) + (pos - pygame.Vector2(pivot.x, pivot.y)).rotate(-angle)
        gun = surface.get_rect(center = image_offset)
        
        return surface, gun

        
    def position(self, pivot, gun_rect, gun_image, screen):

        # Position offset from pivot        
        pos = pivot + self.gun_player_offset

        # Saves original gun image
        original_image = gun_image

        # Saves flipped and unflipped variant of image
        image_unflipped = original_image
        image_flipped = pygame.transform.flip(original_image, False, True)
        
        # Gun rect has same position and size as gun_image
        gun_rect = gun_image.get_rect(center = pos)

        # Mouse position setting
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        
        # Sets mouse offset and angle with some mathy fcky wucky bullsht
        mouse_offset = mouse_pos - pivot
        mouse_angle = -math.degrees(math.atan2(mouse_offset.y, mouse_offset.x))

        # Image flipping
        if mouse_pos.x < pivot.x:
            original_image = image_flipped
        else:
            original_image = image_unflipped
            
        # Rotating the gun around pivot
        image, gun_rect = GunSystem().rotate_around_pivot(original_image, mouse_angle, pivot, pos)

        # Rednders both gun rect and image
        pygame.draw.rect(screen, (105, 0, 10), gun_rect)
        screen.blit(image, gun_rect)

        # Sets the bullet direction to normalized Vector2 using, again, some math
        theta = mouse_angle * (math.pi / 180)
        self.bullet_dir = pygame.Vector2(math.cos(theta), -math.sin(theta)).normalize()

        return gun_rect


    def shoot(self, bullet, SCREEN_WIDTH, SCREEN_HEIGHT, gun):


        # Detects if you click the mouse
        if pygame.mouse.get_pressed()[0] == True:
            self.bullet_spawned = True
        

        # Checks if bullet has spawned, if yes, changes its position; else, sets its position to the gun's
        if self.bullet_spawned == True:
            bullet.x += self.bullet_dir.x * self.bullet_speed
            bullet.y += self.bullet_dir.y * self.bullet_speed
        else:
            bullet.x, bullet.y = gun.x, gun.y
        

        # Despawns the bullet when it's offscreen
        if bullet.x < 0 or bullet.y < 0 or bullet.x > SCREEN_WIDTH or bullet.y > SCREEN_HEIGHT == True:
            self.bullet_spawned = False
        

    def run(self, gun_rect, player_hitbox, bullet, SCREEN_WIDTH, SCREEN_HEIGHT, bullet_spawned, image, screen):

        # Vatiables
        self.bullet_spawned = bullet_spawned
        
        # Runs the whole function in the correct order
        gun_rect = GunSystem.position(self, pygame.Vector2(player_hitbox.x, player_hitbox.y) + pygame.Vector2(player_hitbox.w, player_hitbox.h)/2, gun_rect, image, screen)
        GunSystem.shoot(self, bullet, SCREEN_WIDTH, SCREEN_HEIGHT, gun_rect)
        
        return self.bullet_spawned