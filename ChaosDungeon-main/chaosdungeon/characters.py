import pygame as pyg
import random


class Projectile(pyg.sprite.Sprite):
    """sprites that fly in direction of player and do damage on collision"""
    def __init__(self, image, screen, player, x, y, move_speed=7, attack_damage=5, spawn_anim=False):
        pyg.sprite.Sprite.__init__(self)
        self.image = image.copy()
        self.rect = image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.attack_damage = attack_damage
        self.screen = screen
        self.player = player
        self.type = "attack"
        self.move_speed = move_speed
        self.spawn_anim = spawn_anim    # determines if projectile should fade in or not
        if self.spawn_anim:
            self.image.set_alpha(0)
        self.spawn_counter = 0
        self.width = self.rect.width
        self.height = self.rect.height

        # calculates direction of projectile based on current player location
        px, py = self.player.get_position()
        x, y = self.rect.centerx, self.rect.centery
        direction_vector = pyg.math.Vector2(px - x, py - y)
        direction_vector.scale_to_length(self.move_speed)
        self.move_vector = direction_vector

    def update(self):
        """logic for moving the projectile"""
        if self.spawn_anim: # fades in before firing if spawn animation
            self.image.set_alpha(self.spawn_counter)
            self.spawn_counter += 15
            if self.spawn_counter == 255:
                self.spawn_anim = False
                # calculates movement direction after fading in
                px, py = self.player.get_position()
                x, y = self.rect.centerx, self.rect.centery
                direction_vector = pyg.math.Vector2(px - x, py - y)
                direction_vector.scale_to_length(self.move_speed)
                self.move_vector = direction_vector
        else:   # moves in same direction until collision
            self.rect.move_ip(self.move_vector)
            if self.rect.colliderect(self.player.rect):
                self.player.take_damage(self.attack_damage)
                self.kill()


class Attack(pyg.sprite.Sprite):
    """sprite that damages enemies on contact spawned by the player"""
    def __init__(self, image, screen, splat, player, all_sprites, x, y, move_speed=4, attack_damage=50):
        pyg.sprite.Sprite.__init__(self)
        self.type = "attack"
        self.splat = splat
        self.rect = image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.attack_damage = player.attack_damage
        self.screen = screen
        self.player = player
        self.all_sprites = all_sprites
        self.move_speed = move_speed
        self.range = player.attack_range

        # calculates direction based on position of mouse in relation to player
        px, py = self.player.get_position()
        x, y = pyg.mouse.get_pos()
        self.enemyhit = False
        self.enemies = []
        origin = pyg.math.Vector2(0,-1)
        direction_vector = pyg.math.Vector2(x - px, y - py)
        angle = -origin.angle_to(direction_vector)
        self.image = pyg.transform.rotate(image, angle)
        direction_vector.scale_to_length(self.move_speed)
        self.move_vector = direction_vector
        self.rect.move_ip(10*self.move_vector)

    def update(self):
        """movement logic for attack"""
        self.rect.move_ip(self.move_vector) # moves in same direction until it reaches max range
        for sprite in self.all_sprites:
            if self.rect.colliderect(sprite.rect) and sprite.type == "enemy":
                if not self.enemyhit:    
                    self.splat.play()   # plays enemy hit sound
                    self.enemyhit = True
                if not self.enemies.__contains__(sprite):
                    sprite.take_damage(self.attack_damage)
                    self.enemies.append(sprite)
        if self.range <= 0:
            self.kill()
            self.enemyhit = False
        self.range -= 1


class Characters(pyg.sprite.Sprite):
    """contains various attributes needed by characters"""
    def __init__(self, image, screen, x=0, y=0, maximum_health=100, move_speed=10, attack_damage=10, attack_range=5, level=1):
        pyg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_speed = move_speed
        self.attack_damage = attack_damage
        self.attack_range = attack_range
        self.level = level
        self.screen = screen
        self.current_health = maximum_health
        self.target_health = maximum_health
        self.maximum_health = maximum_health

    # get functions: return value of attribute specified
    def get_position(self):
        return self.rect.centerx, self.rect.centery

    def get_health(self):
        return self.current_health

    def get_move_speed(self):
        return self.move_speed

    def get_attack_damage(self):
        return self.attack_damage

    def get_attack_range(self):
        return self.attack_range

    def get_character_level(self):
        return self.level

    # set functions: change the value of the attribute to the specified value
    def set_position(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y

    def set_current_health(self, new_health):
        self.current_health = new_health

    def set_move_speed(self, new_move_speed):
        self.move_speed = new_move_speed

    def set_attack_damage(self, new_attack_damage):
        self.attack_damage = new_attack_damage

    def set_attack_range(self, new_attack_range):
        self.attack_range = new_attack_range

    def set_character_level(self, level):
        self.level = level

    def heal(self, amount):
        """takes in the amount that the player is supposed to heal and adds it to the total health"""
        if self.current_health < self.maximum_health:
            self.current_health += amount
        if self.current_health >= self.maximum_health:
            self.current_health = self.maximum_health


class Player(Characters):
    """The player of the game, controlled by the user"""
    def __init__(self, image, screen, x=0, y=0, maximum_health=100, move_speed=4, attack_damage=50, attack_range=5, level=1):
        Characters.__init__(self, image, screen, x, y, maximum_health, move_speed, attack_damage, attack_range, level)
        self.type = "player"
        self.health_bar_length = 300  # how long the health bar is in pixels
        self.health_ratio = self.maximum_health/self.health_bar_length
        self.health_change_speed = 1
        self.attack_speed = 20
        self.attack_cooldown = 10

    def update(self):
        # The logic to move the character. Called every frame.
        self.health_bar()
        pressed_keys = pyg.key.get_pressed()  # list of all states of keys
        if pressed_keys[pyg.K_a]:  # if the key is a/left, the player moves to the left
            self.rect.move_ip(self.move_speed * -1, 0)
        if pressed_keys[pyg.K_d]:
            self.rect.move_ip(self.move_speed, 0)
        if pressed_keys[pyg.K_w]:
            self.rect.move_ip(0, self.move_speed * -1)
        if pressed_keys[pyg.K_s]:
            self.rect.move_ip(0, self.move_speed)

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def get_attack_cooldown(self):
        return self.attack_cooldown

    def reset_attack_cooldown(self):
        self.attack_cooldown = self.attack_speed
    
    # the take_dmg and heal functions add or subtract health within a bound of zero and max_health
    def take_damage(self, amount):
        """takes in the amount of dmg taken by the player and subtracts it from the total health"""
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health <= 0:
            self.target_health = 0

    def heal(self, amount):
        """takes in the amount that the player is supposed to heal and adds it to the total health"""
        if self.target_health < self.maximum_health:
            self.target_health += amount
        if self.target_health >= self.maximum_health:
            self.target_health = self.maximum_health

    def health_bar(self):
        """player's health bar and animations for it"""
        transition_width = 0
        transition_color = (0,0,0)

        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health-self.current_health)/self.health_ratio)
            transition_color = (0,255,0)  # green for healing
        elif self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = int((self.target_health-self.current_health)/-self.health_ratio)
            transition_color = (100,62,45)  # yellow for decreasing health

        health_bar_rect = pyg.Rect(35,10,(self.current_health/self.health_ratio),15)
        transitioning_health_rect = pyg.Rect(health_bar_rect.right,10,transition_width,15)

        pyg.draw.rect(self.screen,(210,0,0),health_bar_rect)
        pyg.draw.rect(self.screen,transition_color,transitioning_health_rect)
        pyg.draw.rect(self.screen,(255,255,255),(35,10,self.health_bar_length,15),4)


class Enemy(Characters):
    """enemies that damage the player on contact"""
    def __init__(self, image, screen, player, x=0, y=0, maximum_health=100, move_speed=4, attack_damage=10, attack_range=5,
                 level=1):
        super().__init__(image, screen, x, y, maximum_health, move_speed, attack_damage, attack_range, level)
        self.type = "enemy"
        self.collide = False
        self.hit_cooldown = 0
        self.player = player
        self.player_hit_cooldown = 0    # ensures enemy can only hit the player every few ticks
        self.damaged_cooldown = 0       # ensure the enemy only takes damage every few ticks
        self.dead = False
        self.counted = False

    def die(self):
        """determines if the enemy is dead and deletes its sprite if so"""
        if self.current_health <= 0:
            self.dead = True
            self.kill()

    # the take_dmg and heal functions add or subtract health within a bound of zero and max_health
    def take_damage(self, amount):
        """takes in the amount of dmg taken by the player and subtracts it from the total health"""
        if self.damaged_cooldown <= 0:
            if self.current_health > 0:
                self.current_health -= amount
            if self.current_health <= 0:
                self.current_health = 0
            self.damaged_cooldown = 8


class Boss(Enemy):
    """Boss enemy"""
    def __init__(self, image, circle_image, screen, player, x=500, y=209, maximum_health=3500, move_speed=0, attack_damage=10,
                 attack_range=1, level=1):
        super(Boss, self).__init__(image, screen, player, x, y, maximum_health, move_speed, attack_damage, attack_range, level)
        self.health_bar_length = 300  # how long the health bar is in pixels
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.health_change_speed = 10
        self.image = image.copy()
        self.attack_cooldown = 30
        self.teleport_cooldown = 255
        self.spec_attack_cooldown = 455
        self.teleporting = False
        self.teleported = False
        self.spec_attacking = False
        self.spec_attack_counter = 100
        self.fade_counter = 255
        self.tp_positions = [(38, 209), (538, 55), (1062, 209), (538, 394), (500, 209)]

    def get_attack_cooldown(self):
        return self.attack_cooldown

    def get_spec_attacking(self):
        return self.spec_attacking

    def update(self):
        self.health_bar()
        self.die()
        if self.teleporting:
            if not self.teleported:
                self.fade_counter -= 25.5
                self.image.set_alpha(self.fade_counter)
                if self.fade_counter == 0:
                    self.rect.update(self.tp_positions[random.randint(0,4)], (self.rect.width, self.rect.height))
                    self.teleported = True
            else:
                self.fade_counter += 25.5
                self.image.set_alpha(self.fade_counter)
                if self.fade_counter == 255:
                    self.teleported = False
                    self.teleporting = False
        else:
            if not self.spec_attacking:
                self.attack_cooldown -= 1
                self.spec_attack_cooldown -= 1
                self.teleport_cooldown -= 1
                if self.teleport_cooldown < 0:
                    self.teleport_cooldown = 255
                    self.teleporting = True
                if self.attack_cooldown < 0:
                    self.attack_cooldown = 30
                if self.spec_attack_cooldown < 0:
                    self.spec_attacking = True
                    self.spec_attack_cooldown = 455
            else:
                self.spec_attack_counter -= 1
                if self.spec_attack_counter < 0:
                    self.spec_attacking = False
                    self.spec_attack_counter = 100

        self.damaged_cooldown -= 1
        self.player_hit_cooldown -= 1
        if self.rect.colliderect(self.player.rect) and self.player_hit_cooldown <= 0:
            self.player.take_damage(self.attack_damage)
            self.collide = True
            self.player_hit_cooldown = 10

    def health_bar(self):
        transition_width = 0
        transition_color = (0, 0, 0)

        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (0, 255, 0)  # green for healing
        elif self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / -self.health_ratio)
            transition_color = (100, 62, 45)  # yellow for decreasing health

        health_bar_rect = pyg.Rect(800, 5, (self.current_health / self.health_ratio), 15)
        transitioning_health_rect = pyg.Rect(health_bar_rect.right, 5, transition_width, 15)

        pyg.draw.rect(self.screen, (0, 0, 210), health_bar_rect)
        pyg.draw.rect(self.screen, transition_color, transitioning_health_rect)
        pyg.draw.rect(self.screen, (255, 255, 255), (800, 5, self.health_bar_length, 15), 4)

    def take_damage(self, amount):
        '''takes in the amount of dmg taken by the player and subtracts it from the total health'''
        if self.damaged_cooldown <= 0:
            if self.target_health > 0:
                self.target_health -= amount
            if self.target_health <= 0:
                self.target_health = 0
            self.damaged_cooldown = 8


class Bat(Enemy):
    def __init__(self, image, screen, player, x=0, y=0, maximum_health=50, move_speed=6, attack_damage=5, attack_range=5, level=1):
        super(Bat, self).__init__(image, screen, player, x, y, maximum_health, move_speed, attack_damage, attack_range, level)

    def update(self):
        self.die()
        px, py = self.player.get_position()
        x, y = self.get_position()
        self.player_hit_cooldown -= 1
        self.damaged_cooldown -= 1
        if 300 > self.rect.x - self.player.rect.x > -300 and 200 > self.rect.y - self.player.rect.y > -200:
            move = self.move_speed
            if self.collide:
                move = -self.move_speed
            direction_vector = pyg.math.Vector2(px - x, py - y)
            direction_vector.scale_to_length(move)
            self.rect.move_ip(direction_vector)

        if self.rect.colliderect(self.player.rect) and self.player_hit_cooldown <= 0:
            self.player.take_damage(self.attack_damage)
            self.collide = True
            self.hit_cooldown = 7
            self.player_hit_cooldown = 5

        if not self.rect.colliderect(self.player.rect):
            if self.hit_cooldown == 0:
                self.collide = False
            self.hit_cooldown = self.hit_cooldown - 1


class Skeleton(Enemy):
    def __init__(self, image, screen, player, x=0, y=0, maximum_health=80, move_speed=3, attack_damage=5, attack_range=5,
                 level=1, attack_speed=70):
        super(Skeleton, self).__init__(image, screen, player, x, y, maximum_health, move_speed, attack_damage, attack_range, level)
        self.attack_speed = attack_speed
        self.attack_cooldown = self.attack_speed

    def update(self):
        self.die()
        px, py = self.player.get_position()
        x, y = self.get_position()
        self.player_hit_cooldown -= 1
        self.damaged_cooldown -= 1
        if 150 > self.rect.x - self.player.rect.x > -150 and 150 > self.rect.y - self.player.rect.y > -150:
            move = -self.move_speed
            if self.collide:
                move = -self.move_speed
            direction_vector = pyg.math.Vector2(px - x, py - y)
            direction_vector.scale_to_length(move)
            self.rect.move_ip(direction_vector)
        else:   # skeleton can't attack while running away
            self.attack_cooldown -= 1
        if self.rect.colliderect(self.player.rect) and self.player_hit_cooldown <= 0:
            self.player.take_damage(self.attack_damage)
            self.collide = True
            self.player_hit_cooldown = 5
            self.hit_cooldown = 7

        if not self.rect.colliderect(self.player.rect):
            if self.hit_cooldown == 0:
                self.collide = False
            self.hit_cooldown = self.hit_cooldown - 1


    def get_attack_cooldown(self):
        return self.attack_cooldown

    def reset_attack_cooldown(self):
        self.attack_cooldown = self.attack_speed


class Goblin(Enemy):
    def __init__(self, image, screen, player, x=0, y=0, maximum_health=200, move_speed=3, attack_damage=5, attack_range=5,
                 level=1):
        super(Goblin, self).__init__(image, screen, player, x, y, maximum_health, move_speed, attack_damage, attack_range, level)

    def update(self):
        self.die()
        px, py = self.player.get_position()
        x, y = self.get_position()
        self.player_hit_cooldown -= 1
        self.damaged_cooldown -= 1
        move = self.move_speed
        if self.collide:
            move = -self.move_speed

        direction_vector = pyg.math.Vector2(px - x, py - y)
        direction_vector.scale_to_length(move)
        self.rect.move_ip(direction_vector)

        if self.rect.colliderect(self.player.rect) and self.player_hit_cooldown <= 0:
            self.player.take_damage(self.attack_damage)
            self.collide = True
            self.player_hit_cooldown = 5
            self.hit_cooldown = 7

        if not self.rect.colliderect(self.player.rect):
            if self.hit_cooldown == 0:
                self.collide = False
            self.hit_cooldown = self.hit_cooldown - 1

            
class Obstacles(Enemy):
    def __init__(self, image, screen, player, all_sprites, x=0, y=0, health=100, move_speed=0, attack_damage=1.5, attack_range=0, level=1, spawn_anim=False, powerup=False):
        super().__init__(image, screen, player, x, y, health, move_speed, attack_damage, attack_range, level)
        self.all_sprites = all_sprites
        self.type = "obstacle"
        self.spawn_anim = spawn_anim
        self.powerup = powerup
        if spawn_anim:
            self.image.set_alpha(0)
        self.spawn_counter = 0
    
    def update(self):
        if self.spawn_anim:
            self.spawn_counter += 5
            self.image.set_alpha(self.spawn_counter)
            if self.spawn_counter == 255:
                self.spawn_anim = False
        else:
            for sprite in self.all_sprites:
                if sprite.rect.colliderect(self.rect):
                    if type(sprite) == Projectile:
                        sprite.kill()
                    elif type(sprite) == Attack:
                        pass
                    elif type(sprite) == Bat:
                        if abs(self.rect.top - sprite.rect.bottom) < 8:
                            sprite.rect.move_ip(sprite.move_speed, sprite.move_speed*-1)
                        if abs(self.rect.bottom - sprite.rect.top) < 8:
                            sprite.rect.move_ip(sprite.move_speed, sprite.move_speed)
                        if abs(self.rect.right - sprite.rect.left) < 8:
                            sprite.rect.move_ip(sprite.move_speed*2, 0)
                        if abs(self.rect.left - sprite.rect.right) < 8:
                            sprite.rect.move_ip(0, 0)
                        sprite.rect.move_ip(sprite.move_speed * -1, 0)
                    else:
                        if not self.powerup:
                            if abs(self.rect.top - sprite.rect.bottom) < 8:
                                sprite.rect.move_ip(sprite.move_speed, sprite.move_speed*-1)
                            if abs(self.rect.bottom - sprite.rect.top) < 8:
                                sprite.rect.move_ip(sprite.move_speed, sprite.move_speed)
                            if abs(self.rect.right - sprite.rect.left) < 8:
                                sprite.rect.move_ip(sprite.move_speed*2, 0)
                            if abs(self.rect.left - sprite.rect.right) < 8:
                                sprite.rect.move_ip(0, 0)
                            sprite.rect.move_ip(sprite.move_speed * -1, 0)          
            
            
class Button:
    '''doesn't inherit anything, just used to set up buttons'''
    def __init__(self, image, pos, font, text_input, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image == None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        
    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
        
    def input_check(self, position):
        '''checks to see if the mouse is on the button'''
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def change_color(self, position):
        '''changes the color of the button when the mouse is hovering over it'''
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

            
class Board:
    def __init__(self, room, screen, player, locks, unlocks, bosslocks, bossunlocks, background_img, all_sprites, obstacle_imgs, locked=True):
        self.room = room
        self.screen = screen
        self.player = player
        self.locked = locked
        self.lDraw = []
        self.unlocks = unlocks
        self.bossunlocks = bossunlocks
        self.uDraw = []
        self.locks = locks
        self.bosslocks = bosslocks
        self.background_img = background_img
        self.all_sprites = all_sprites
        self.obstacle_imgs = obstacle_imgs
        self.change = False
        self.leftIncluded = False
        self.rightIncluded = False
        self.topIncluded = False
        self.bottomIncluded = False
        self.door_imgs = pyg.sprite.RenderUpdates([self.locks])

    def draw(self):
        if self.room.left != None and not self.leftIncluded:
            if self.room.type == "boss" or self.room.leftboss == True:
                self.lDraw.append(self.bosslocks[0])
                self.uDraw.append(self.bossunlocks[0])
                self.leftIncluded = True
            else:
                self.lDraw.append(self.locks[0])
                self.uDraw.append(self.unlocks[0])
                self.leftIncluded = True
        
        if self.room.right != None and not self.rightIncluded:
            if self.room.type == "boss" or self.room.rightboss == True:
                self.lDraw.append(self.bosslocks[1])
                self.uDraw.append(self.bossunlocks[1])
                self.leftIncluded = True
            else:
                self.lDraw.append(self.locks[1])
                self.uDraw.append(self.unlocks[1])
                self.rightIncluded = True
        
        if self.room.top != None and not self.topIncluded:
            if self.room.type == "boss" or self.room.topboss == True:
                self.lDraw.append(self.bosslocks[2])
                self.uDraw.append(self.bossunlocks[2])
                self.leftIncluded = True
            else:
                self.lDraw.append(self.locks[2])
                self.uDraw.append(self.unlocks[2])
                self.topIncluded = True
        
        if self.room.bottom != None and not self.bottomIncluded:
            if self.room.type == "boss" or self.room.bottomboss == True:
                self.lDraw.append(self.bosslocks[3])
                self.uDraw.append(self.bossunlocks[3])
                self.leftIncluded = True
            else:
                self.lDraw.append(self.locks[3])
                self.uDraw.append(self.unlocks[3])
                self.bottomIncluded = True

        objs_list = self.door_imgs.draw(self.screen)
        pyg.display.update(objs_list)

    def updateRoom(self, room):
        self.room = room

    def clearDoors(self):
        self.uDraw = []
        self.lDraw = []
        self.leftIncluded = False
        self.rightIncluded = False
        self.topIncluded = False
        self.bottomIncluded = False
        
    def update(self):
        if self.change:
            if self.locked:
                self.door_imgs.clear(self.screen, self.background_img)
                self.door_imgs = pyg.sprite.RenderUpdates(self.lDraw)
                self.draw()
            else:
                self.door_imgs.clear(self.screen, self.background_img)
                self.door_imgs = pyg.sprite.RenderUpdates(self.uDraw)
                self.draw()
            self.change = False
        else:
            if self.locked:
                self.door_imgs = pyg.sprite.RenderUpdates(self.lDraw)
                self.draw()
            else:
                self.door_imgs = pyg.sprite.RenderUpdates(self.uDraw)
                self.draw()

