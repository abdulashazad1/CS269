import characters as char
import random


class Room():
    """Room contains all the information for one dungeon room"""
    def __init__(self, enemy_imgs, obstacle_imgs, screen, player, all_sprites, bossimage, circleimage, left=None, right=None, top=None, bottom=None, type="normal"):
        self.enemy_imgs = enemy_imgs
        self.obstacle_imgs = obstacle_imgs
        self.screen = screen
        self.player = player
        self.all_sprites = all_sprites
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.enemies = []
        self.obstacles = []
        self.cleared = False
        self.collected = False
        self.type = type
        self.bossimage = bossimage
        self.circleimage = circleimage
        self.leftboss = False
        self.rightboss = False
        self.topboss = False
        self.bottomboss = False

        # When room is called, automatically sets up room based on type
        if self.type == "boss":
            self.spawnBoss()
        else:
            self.spawn_enemies()
            self.spawn_obstacles()

    def spawnBoss(self):
        # Adds boss type enemy to the room
        self.enemies.append(char.Boss(self.bossimage, self.circleimage, self.screen, self.player))
    
    def spawn_enemies(self, num_enemies=None):
        # Randomly selects a bunch of normal enemies to be spawned in the room (between 3 and 6)
        if num_enemies == None:
            num_enemies = random.randint(3,6)
        for i in range(num_enemies):
            choose = random.randint(0, 2)
            position_x = random.randint(150, 1130)
            position_y = random.randint(50, 530)
            color = random.random()
            if choose == 0:
                if color > .1:
                    self.enemies.append(char.Skeleton(self.enemy_imgs[0], self.screen, self.player, position_x, position_y))
                else:
                    self.enemies.append(char.Skeleton(self.enemy_imgs[1], self.screen, self.player, position_x, position_y, attack_speed=10))
            if choose == 1:
                if color > .1:
                    self.enemies.append(char.Goblin(self.enemy_imgs[2], self.screen, self.player, position_x, position_y))
                else:
                    self.enemies.append(char.Goblin(self.enemy_imgs[3], self.screen, self.player, position_x, position_y, maximum_health=300))
            if choose == 2:
                if color > .1:
                    self.enemies.append(char.Bat(self.enemy_imgs[4], self.screen, self.player, position_x, position_y))
                else:
                    self.enemies.append(char.Bat(self.enemy_imgs[5], self.screen, self.player, position_x, position_y, move_speed=8))
    
    def spawn_obstacles(self, num_obstacles=None):
        # Randomly spawns 1 to 3 obstacles in the room
        if num_obstacles == None:
            num_obstacles = random.randint(1,3)
        for i in range(num_obstacles):
            choose = random.randint(0, 3)
            position_x = random.randint(250, 1030)
            position_y = random.randint(150, 430)
            self.obstacles.append(char.Obstacles(self.obstacle_imgs[choose], self.screen, self.player, self.all_sprites, position_x, position_y))
    
    def roomCleared(self):
        # Called when a room is cleared to make adjustments accordingly
        self.enemies = []
        self.cleared = True
    
    def powerupCollected(self):
        # Called when the powerup is collected to make adjustments accordingly
        self.collected = True
        for obstacle in self.obstacles:
            if obstacle.powerup:
                obstacle.kill()
                self.obstacles.remove(obstacle)
    
    def addRoom(self, direction):
        # Function adds a room in the specified direction
        if direction == "left":
            self.left = Room(self.enemy_imgs, self.obstacle_imgs, self.screen, self.player, self.all_sprites, self.bossimage, self.circleimage, right=self)
        
        if direction == "right":
            self.right = Room(self.enemy_imgs, self.obstacle_imgs, self.screen, self.player, self.all_sprites, self.bossimage, self.circleimage, left=self)
        
        if direction == "top":
            self.top = Room(self.enemy_imgs, self.obstacle_imgs, self.screen, self.player, self.all_sprites, self.bossimage, self.circleimage, bottom=self)
        
        if direction == "bottom":
            self.bottom = Room(self.enemy_imgs, self.obstacle_imgs, self.screen, self.player, self.all_sprites, self.bossimage, self.circleimage, top=self)

    def moreRooms(self, roomsLeft=6, bossLeft=1, currentroom=0):
        # This recursive funtion generates a dungeon with roomsLeft + 1 rooms with 1 boss room
        list = []
        if self.left == None:
            list.append("left")
        if self.right == None:
            list.append("right")
        if self.top == None:
            list.append("top")
        if self.bottom == None:
            list.append("bottom")
        
        doors = random.randint(1, len(list))

        if roomsLeft > doors:
            roomsLeft -= doors
        else:
            doors = roomsLeft
            roomsLeft = 0
        
        for i in range(doors):
            if currentroom != 0 and bossLeft != 0:
                choice = random.choice(list)
                self.addBoss(choice)
                list.remove(choice)
                if choice == "left":
                    self.leftboss = True
                if choice == "right":
                    self.rightboss = True
                if choice == "top":
                    self.topboss = True
                if choice == "bottom":
                    self.bottomboss = True
                bossLeft = 0
            else:
                choice = random.choice(list)
                self.addRoom(choice)
                if choice == "left":
                    roomsLeft, bossLeft = self.left.moreRooms(roomsLeft, bossLeft=bossLeft, currentroom=currentroom+1)
                if choice == "right":
                    roomsLeft, bossLeft = self.right.moreRooms(roomsLeft, bossLeft=bossLeft, currentroom=currentroom+1)
                if choice == "top":
                    roomsLeft, bossLeft = self.top.moreRooms(roomsLeft, bossLeft=bossLeft, currentroom=currentroom+1)
                if choice == "bottom":
                    roomsLeft, bossLeft = self.bottom.moreRooms(roomsLeft, bossLeft=bossLeft, currentroom=currentroom+1)
                list.remove(choice)
        
        if roomsLeft != 0 and doors == 0:
            roomsLeft, bossLeft = self.moreRooms(roomsLeft)
        
        return roomsLeft, bossLeft
    
    def addBoss(self, direction):
        # This functions adds a boss room in the specified direction
        if direction == "left":
            self.left = Room(self.enemy_imgs, self.obstacle_imgs, self.screen, self.player, self.all_sprites, self.bossimage, self.circleimage, right=self, type="boss")
        
        if direction == "right":
            self.right = Room(self.enemy_imgs, self.obstacle_imgs, self.screen, self.player, self.all_sprites, self.bossimage, self.circleimage, left=self, type="boss")
        
        if direction == "top":
            self.top = Room(self.enemy_imgs, self.obstacle_imgs, self.screen, self.player, self.all_sprites, self.bossimage, self.circleimage, bottom=self, type="boss")
        
        if direction == "bottom":
            self.bottom = Room(self.enemy_imgs, self.obstacle_imgs, self.screen, self.player, self.all_sprites, self.bossimage, self.circleimage, top=self, type="boss")