# Importing pygame
import pygame
import math

# Importing from the rooms script
from rooms import Rooms

class GunSystem:

    def __init__(self):

        self.BULLET_SPEED = 100
        self.GUN_PLAYER_OFFSET = pygame.Vector2(50, 0)
        self.MOUSE_ANGLE_DIFFERENCE: float = 7.5
        self.bullet_spawned_dict: dict = {}
        for i in range(-4, 5):
            self.bullet_spawned_dict.update({i: False})
        self.bullet_dir = pygame.Vector2(0, 0)

    def spawn(self, base_bullet):

        bullet_dict = {}
        for id in range(-4, 5):
            bullet_dict.update({id: pygame.rect.Rect((base_bullet.x + id, base_bullet.y, base_bullet.w, base_bullet.h))})
        
        return bullet_dict


    def rotate_around_pivot(self, image, angle, pivot, pos):

        # Surface is rotated image
        surface = pygame.transform.rotate(image, angle)
    
        # Image offset from pivot
        image_offset = pygame.Vector2(pivot.x, pivot.y) + (pos - pygame.Vector2(pivot.x, pivot.y)).rotate(-angle)
        gun = surface.get_rect(center = image_offset)
        
        return surface, gun

        
    def position(self, pivot, gun_rect, gun_image, screen, gun_cooldown):

        # Var setting      
        pos = pivot + self.GUN_PLAYER_OFFSET
        original_image = gun_image
        image_unflipped = original_image
        image_flipped = pygame.transform.flip(original_image, False, True)
        gun_rect = gun_image.get_rect(center = pos)
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
        
        # If the bullet isn't spawned, set its direction
        for id in self.bullet_spawned_dict:
            id_value = self.bullet_spawned_dict.get(id)
            if id_value == False and gun_cooldown < 0:
                
                # Sets the bullet direction to normalized Vector2 using, again, some math
                theta = mouse_angle * (math.pi / 180)
                self.bullet_dir = pygame.Vector2(math.cos(theta), -math.sin(theta)).normalize()

        # Renders both gun rect and image
        gun_color = (55, 155, 10) if gun_cooldown < 0 else (105, 0, 10)
        pygame.draw.rect(screen, gun_color, gun_rect)
        screen.blit(image, gun_rect)

        return gun_rect, mouse_angle


    def for_this_bullet(self, id, bullet_dict, gun, SCREEN_WIDTH, SCREEN_HEIGHT, rooms_dict, room, mouse_angle, delta):

        # Fetches current bullet
        bullet = bullet_dict.get(id)
        bullet_spawned = self.bullet_spawned_dict.get(id)

        gun_is_enemy = False

        # Despawns the bullet when it's offscreen or touches static object
        if bullet.x < 0 or bullet.y < 0 or bullet.x > SCREEN_WIDTH or bullet.y > SCREEN_HEIGHT or Rooms().collision(bullet, rooms_dict, room, None, gun_is_enemy) != False:
            self.bullet_spawned_dict.update({id: False})

        # Decides angle based on general bullet direction and id
        theta = math.atan2(-self.bullet_dir.y, self.bullet_dir.x)
        bullet_angle = theta / (math.pi / 180)
        bullet_angle += id * self.MOUSE_ANGLE_DIFFERENCE
        theta = bullet_angle * (math.pi / 180)
        bullet_dir = pygame.Vector2(math.cos(theta), -math.sin(theta)).normalize()


        # Checks if bullet has spawned, if yes, changes its position; else, sets its position to the gun's
        if bullet_spawned:
            bullet.x += bullet_dir.x * self.BULLET_SPEED * delta
            bullet.y += bullet_dir.y * self.BULLET_SPEED * delta
        else:
            bullet.x, bullet.y = gun.center

        # Saves changes to dictionary
        bullet_dict.update({id: bullet})

        return bullet_dict


    def shoot(self, bullet_dict, SCREEN_WIDTH, SCREEN_HEIGHT, gun, rooms_dict, room, gun_cooldown, mouse_angle, delta):
        
        # For each bullet
        for id in range (-4, 5):
            bullet_dict = self.for_this_bullet(id, bullet_dict, gun, SCREEN_WIDTH, SCREEN_HEIGHT, rooms_dict, room, mouse_angle, delta)
        
        # Shoots bullets and sets gun cooldown when clicking
        if pygame.mouse.get_pressed()[0] == True and gun_cooldown < 0:
            self.bullet_spawned_dict = {-2: True, -1: True, 0: True, 1: True, 2: True}
            gun_cooldown = 60
        
        # Despawn bullets after a short time
        if gun_cooldown < 35:
            self.bullet_spawned_dict = {-2: False, -1: False, 0: False, 1: False, 2: False}
        
        # Gun_cooldown will never go below -1
        gun_cooldown = 0 if gun_cooldown < 0 else gun_cooldown

        return gun_cooldown, self.bullet_spawned_dict, bullet_dict
           

    def run(self, gun_rect, player_hitbox, bullet_dict, SCREEN_PARAMATERS, bullet_info, image, screen, room_vars, gun_cooldown, delta):

        # Variables
        SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_PARAMATERS
        rooms_dict, room = room_vars
        self.bullet_spawned_dict, self.bullet_dir = bullet_info

        # Runs the whole function in the correct order
        gun_rect, mouse_angle = GunSystem.position(self, pygame.Vector2(player_hitbox.x, player_hitbox.y) + pygame.Vector2(player_hitbox.w, player_hitbox.h)/2, gun_rect, image, screen, gun_cooldown)
        gun_cooldown, self.bullet_spawned_dict, bullet_dict = GunSystem.shoot(self, bullet_dict, SCREEN_WIDTH, SCREEN_HEIGHT, gun_rect, rooms_dict, room, gun_cooldown, mouse_angle, delta)

        # Rendering bullets
        for id in range(-4, 5):

            bullet = bullet_dict.get(id)
            bullet_spawned = self.bullet_spawned_dict.get(id)

            if bullet_spawned:
                pygame.draw.rect(screen, (200, 200, 0), bullet)
        
        return self.bullet_spawned_dict, self.bullet_dir, gun_cooldown, bullet_dict