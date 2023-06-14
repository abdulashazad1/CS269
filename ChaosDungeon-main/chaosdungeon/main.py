'''this file contains the surface the game runs on and the main event loop'''

# importing the pygame module and own files
import pygame as pyg
import characters as char
import environment as env
import dialogue as dia
import sys
import random


pyg.init()
pyg.mixer.init()


def load_image(image_name, scale=1.0):
    """laods an image based on the given name, scales it, and returns the image"""
    image = pyg.image.load(image_name)
    size = image.get_size()
    image = pyg.transform.scale(image, (size[0] * scale, size[1] * scale))
    image.convert_alpha()
    return image


def load_image_location(image_name, scale=1.0, x=0, y=0):
    """loads an image, scales it, and returns it as a sprite at the given location"""
    img = pyg.sprite.Sprite()
    img.image = load_image(image_name, scale)
    img.image.convert_alpha()
    img.rect = img.image.get_rect()
    img.rect.topleft = [x, y]
    return img


def get_font(size):
    """function to set the font on the buttons for the entire game"""
    return pyg.font.SysFont('cambria', size)


def resetGame(difficulty=0):
    """resets the game"""
    pyg.mixer.music.stop()
    pyg.mixer.music.load('dialogue.wav')
    pyg.mixer.music.play(-1)
    screen.blit(background_img, (0, 0))
    input = dia.scene(screen, 'scene1.txt', bloop)
    start_time = pyg.time.get_ticks()
    game(start_time, input, difficulty=difficulty)


def pause(difficulty=0, game_status=None, score=None, p_time=None):
    """press escape in game to pause the game, also handles pausing on player death and boss defeat"""
    paused = True
    musicstopped = False
    
    while paused:
        menu_mouse_pos = pyg.mouse.get_pos()
        if game_status == 'won':
            firstTime = False
            if musicstopped == False:
                firstTime = True
                pyg.mixer.music.stop()
                pyg.mixer.music.load('victory.wav')
                pyg.mixer.music.play(-1)
                musicstopped = True
            screen.fill((0,0,0))
            you_won = char.Button(None, pos=[600, 80], font=get_font(70), text_input='You Won!', base_color="green", hovering_color='green')
            play_time = char.Button(None, pos=[400, 200], font=get_font(30), text_input='Play Time:', base_color="white", hovering_color='yellow')
            play_score = char.Button(None, pos=[700, 200], font=get_font(30), text_input='Kill Score: ' +  str(score), base_color="white", hovering_color='yellow')
            new_game_button = char.Button(None, pos=[600, 300], font=get_font(25), text_input='Play Again', base_color="white", hovering_color='yellow')
            menu_button = char.Button(None, pos=[600, 400], font=get_font(25), text_input='Main Menu', base_color="white", hovering_color='yellow')
            exit_button = char.Button(None, pos=[600, 500], font=get_font(25), text_input='Quit Game', base_color="white", hovering_color='yellow')
            you_won.update(screen)
            play_time.update(screen)
            play_score.update(screen)
            font=pyg.freetype.SysFont('Times New Roman', 30)
            font.origin=True
            font.render_to(screen, (480, 212), p_time, pyg.Color('white'))
            for button in [new_game_button, menu_button, exit_button]:
                button.change_color(menu_mouse_pos)
                button.update(screen)

            pyg.display.update() 
            if firstTime:
                pyg.time.delay(1500)
            
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    pyg.quit()
                    quit()
                
                if event.type == pyg.MOUSEBUTTONDOWN and not firstTime:
                    if new_game_button.input_check(menu_mouse_pos):
                        resetGame(difficulty=difficulty)
                    if exit_button.input_check(menu_mouse_pos):
                        pyg.quit()
                        quit()
                    if menu_button.input_check(menu_mouse_pos):
                        main_menu(difficulty=difficulty)

        if game_status =='dead':
            firstTime = False
            if musicstopped == False:
                firstTime = True
                pyg.mixer.music.stop()
                pyg.mixer.music.load('gameover.wav')
                pyg.mixer.music.play(-1)
                musicstopped = True
            screen.fill((0,0,0))
            game_over = char.Button(None, pos=[600, 80], font=get_font(70), text_input='You Died', base_color="red", hovering_color='red')
            play_time = char.Button(None, pos=[400, 200], font=get_font(30), text_input='Play Time:', base_color="white", hovering_color='white')
            play_score = char.Button(None, pos=[700, 200], font=get_font(30), text_input='Kill Score: ' +  str(score), base_color="white", hovering_color='white')
            new_game_button = char.Button(None, pos=[600, 300], font=get_font(25), text_input='Try Again', base_color="white", hovering_color='red')
            menu_button = char.Button(None, pos=[600, 400], font=get_font(25), text_input='Main Menu', base_color="white", hovering_color='red')
            exit_button = char.Button(None, pos=[600, 500], font=get_font(25), text_input='Quit Game', base_color="white", hovering_color='red')
            game_over.update(screen)
            play_time.update(screen)
            play_score.update(screen)
            font=pyg.freetype.SysFont('Times New Roman', 30)
            font.origin=True
            font.render_to(screen, (480, 212), p_time, pyg.Color('white'))
            # font2=pyg.freetype.SysFont('Times New Roman', 30)
            # font2.origin=True
            # font2.render_to(screen, (480, 212), score, pyg.Color('white'))
            for button in [new_game_button, menu_button, exit_button]:
                button.change_color(menu_mouse_pos)
                button.update(screen)

            pyg.display.update() 
            if firstTime:
                pyg.time.delay(1500)#this doesn't belong here
            
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    pyg.quit()
                    quit()
                
                if event.type == pyg.MOUSEBUTTONDOWN and not firstTime:
                    if new_game_button.input_check(menu_mouse_pos):
                        resetGame(difficulty=difficulty)
                    if exit_button.input_check(menu_mouse_pos):
                        pyg.quit()
                        quit()
                    if menu_button.input_check(menu_mouse_pos):
                        main_menu(difficulty=difficulty)

        if game_status == None:
            pyg.mixer.music.pause()
            new_game_button = char.Button(button_surface, pos=[600, 200], font=get_font(25), text_input='New Game', base_color="white", hovering_color='black')
            menu_button = char.Button(button_surface, pos=[600, 300], font=get_font(25), text_input='Main Menu', base_color="white", hovering_color='black')
            exit_button = char.Button(button_surface, pos=[600, 400], font=get_font(25), text_input='Quit Game', base_color="white", hovering_color='red')

            for button in [new_game_button, menu_button, exit_button]:
                button.change_color(menu_mouse_pos)
                button.update(screen)

            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    pyg.quit()
                    quit()
            
                if event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_ESCAPE:
                        screen.blit(cover_img, (450,150))
                        paused = False
                
                    elif event.key == pyg.K_q:
                        pyg.quit()
                        sys.exit()
                
                if event.type == pyg.MOUSEBUTTONDOWN:
                    if new_game_button.input_check(menu_mouse_pos):
                        resetGame(difficulty=difficulty)
                    if menu_button.input_check(menu_mouse_pos):
                        main_menu(difficulty=difficulty)
                    if exit_button.input_check(menu_mouse_pos):
                        pyg.quit()
                        quit()
        pyg.display.update() 
    pyg.mixer.music.unpause()


def collide_wall(character, walls):
    """determines if character has collided with a wall and moves/kills them accordingly"""
    if character.rect.colliderect(walls[0]):
        if type(character) == char.Projectile:  # projectiles are killed on collision with a wall
            character.kill()
        elif type(character) == char.Attack:    # attacks go through walls
            pass
        else:                                   # characters are moved to the edge of the wall
            character.rect.left = walls[0].right
    if character.rect.colliderect(walls[1]):
        if type(character) == char.Projectile:
            character.kill()
        elif type(character) == char.Attack:
            pass
        else:
            character.rect.right = walls[1].left
    if character.rect.colliderect(walls[2]):
        if type(character) == char.Projectile:
            character.kill()
        elif type(character) == char.Attack:
            pass
        else:
            character.rect.top = walls[2].bottom
    if character.rect.colliderect(walls[3]):
        if type(character) == char.Projectile:
            character.kill()
        elif type(character) == char.Attack:
            pass
        else:
            character.rect.bottom = walls[3].top


def loadRoom(board, origin, all_sprites, proj_enemies):
    """loads the given room"""
    board.clearDoors()
    for sprite in board.all_sprites:
        if sprite.type != "player":
            board.all_sprites.remove(sprite)
    for obstacle in origin.obstacles:
        board.all_sprites.add(obstacle)
    board.updateRoom(origin)
    for enemy in origin.enemies:
        all_sprites.add(enemy)
        if type(enemy) == char.Skeleton or type(enemy) == char.Boss:
            proj_enemies.append(enemy)


def stopwatch(screen, start_time):
    """keeps track of time in game"""
    clock=pyg.time.Clock()
    font=pyg.freetype.SysFont('Times New Roman', 20)
    font.origin=True

    stopwatch_bacgkround = pyg.rect.Rect(1150, 0, 1150, 30)
    pyg.draw.rect(screen, (100,62,45), stopwatch_bacgkround)
    ticks=pyg.time.get_ticks()-start_time
    seconds=int(ticks/1000 % 60)
    minutes=int(ticks/60000 % 24)
    out='{minutes:02d}:{seconds:02d}'.format(minutes=minutes, seconds=seconds)
    font.render_to(screen, (1150, 25), out, pyg.Color('white'))
    pyg.display.flip()
    clock.tick(60)
    return out


def count_enemies(screen, enemies, previous_count = 0):
    """keeps track of number of enemies killed"""
    count = int(previous_count)
    for enemy in enemies:
        if enemy.dead == True:
            if enemy.counted != True:
                count += 1
                enemy.counted = True
    font=pyg.freetype.SysFont('Times New Roman', 20)
    font.origin=True
    count_background = pyg.rect.Rect(420, 0, 370, 30)
    pyg.draw.rect(screen, (100, 62, 45), count_background)
    text = 'Kills: ' + str(count)
    font.render_to(screen, (420, 25), text, pyg.Color('white'))
    return count


def empower(player, userInput):
    """increases player's stats based on their choice"""
    if userInput == 1:
        player.attack_damage += 10
    elif userInput == 2:
        player.maximum_health += 50
        player.health_bar_length = 370
        player.health_ratio = player.maximum_health / player.health_bar_length
    elif userInput == 3:
        player.attack_range += 5
    elif userInput == 4:
        player.heal(10000)


def game(start_time, input, difficulty = 0):
    """contains the main game loop and all setup for the game to run"""
    pyg.display.set_caption('Chaos Dungeon')
    all_sprites = pyg.sprite.RenderUpdates()    # contains all moving sprites (player and enemies)
    combat = False
    combatmusic = False
    emptymusic = False
    teleported = False
    total_killed = 0
    firstclear = True
    firstpower = True
    
    # create player based on first player choice
    if input == 1:
        player = char.Player(player1_img, screen, 45, 300, attack_damage=80)
    elif input == 2:
        player = char.Player(player1_img, screen, 45, 300, maximum_health=150)
    elif input == 3:
        player = char.Player(player1_img, screen, 45, 300, attack_range=15)
    elif input == 4:
        player = char.Player(player1_img, screen, 45, 300, move_speed=6)
    else:
        player = char.Player(player1_img, screen, 45, 300)
    all_sprites.add(player)
    # power up giver sprite
    powerup_giver = char.Obstacles(power_giver_img, screen, player, all_sprites, 575, 255, attack_damage=0, spawn_anim=True, powerup=True)
    #player.current_health = 1
    # create dungeon rooms
    origin = env.Room(enemy_imgs, obstacle_imgs, screen, player, all_sprites, boss_img, circle_img)
    origin.moreRooms()

    # changes player health based on difficulty
    if difficulty == 0:
        pass

    if difficulty == 1:
        player.current_health = 1
        player.maximum_health = 30
        player.target_health = 30
        player.health_ratio = player.maximum_health/player.health_bar_length
        
    if difficulty == -1:
        player.health_change_speed = 60
        player.maximum_health = 120
        player.target_health = 120
        player.health_change_speed = 1
        player.health_ratio = player.maximum_health/player.health_bar_length
    proj_enemies = []
    for enemy in origin.enemies:
        all_sprites.add(enemy)
        if type(enemy) == char.Skeleton or type(enemy) == char.Boss:
            proj_enemies.append(enemy)
    
    # put background onto screen
    screen.blit(background_img, (0, 0))

    # create rectangles to represent walls
    left_wall = pyg.rect.Rect(38, 38, 28, 494)
    right_wall = pyg.rect.Rect(1162, 38, 28, 494)
    top_wall = pyg.rect.Rect(38, 38, 1152, 28)
    bottom_wall = pyg.rect.Rect(38, 548, 1152, 28)
    walls = [left_wall, right_wall, top_wall, bottom_wall]

    # changing game icon to our own art, the icon variable can also be used for desktop shortcuts
    icon = pyg.image.load('dragon.png')  # change dragon.png to the art for our title
    pyg.display.set_icon(icon)

    running = True
    # loads the starting room
    board = char.Board(origin, screen, player, locks, unlocks, bosslocks, bossunlocks, background_img, all_sprites, obstacle_imgs)
    loadRoom(board, origin, all_sprites, proj_enemies)
    board.draw()

    # stops menu music
    pyg.mixer.music.stop()

    # main game loop
    while running:
        time = stopwatch(screen, start_time)
        total_killed = count_enemies(screen, origin.enemies, total_killed)
        combat = False
        for sprite in all_sprites:  # determines combat state based on remaining enemies
            if sprite.type == "enemy":
                combat = True

        if combat:
            emptymusic = False
            if combatmusic == False:
                board.locked = True
                board.change = True
                if origin.type == "boss":
                    pyg.mixer.music.stop()
                    pyg.mixer.music.load('dialogue.wav')
                    pyg.mixer.music.play(-1)
                    checkInput = dia.scene(screen, "scene4.txt", bloop, s2="omni")
                    screen.blit(background_img, (0, 0))
                    pyg.mixer.music.stop()
                    pyg.mixer.music.load('boss.wav')
                    pyg.mixer.music.play(-1)
                else:
                    pyg.mixer.music.stop()
                    pyg.mixer.music.load('fightmusic.wav')
                    pyg.mixer.music.play(-1)
                combatmusic = True
        else:
            teleported = False
            board.locked = False
            combatmusic = False
            if emptymusic == False:
                board.locked = False
                enemies_killed = len(origin.enemies)
                origin.roomCleared()
                count_enemies(screen, origin.enemies, enemies_killed)
                enemies_killed = len(origin.enemies)

                if firstclear:
                    pyg.mixer.music.stop()
                    pyg.mixer.music.load('dialogue.wav')
                    pyg.mixer.music.play(-1)
                    checkInput = dia.scene(screen, "scene2.txt", bloop, s2="omni")
                    screen.blit(background_img, (0, 0))
                    firstclear = False

                pyg.mixer.music.stop()
                pyg.mixer.music.load('empty.wav')
                powerup_giver.spawn_anim = True
                powerup_giver.spawn_counter = 0
                origin.obstacles.append(powerup_giver)
                loadRoom(board,origin,all_sprites,proj_enemies)
                pyg.mixer.music.play(-1)
                emptymusic = True
            if powerup_giver.rect.colliderect(player.rect) and not origin.collected and powerup_giver.spawn_anim==False:
                # gives player powerup dialogue if they collide with powerup giver
                pyg.mixer.music.stop()
                pyg.mixer.music.load('dialogue.wav')
                pyg.mixer.music.play(-1)
                checkInput = None

                if firstpower:
                    checkInput = dia.scene(screen, "scene3.txt", bloop, s2="giver")
                    firstpower = False
                else:
                    checkInput = dia.scene(screen, "powerup.txt", bloop, s2="giver")

                empower(player,checkInput)
                origin.powerupCollected()
                # origin.obstacles.remove(powerup_giver)
                loadRoom(board, origin, all_sprites, proj_enemies)
                screen.blit(background_img, (0, 0))
                board.update()
                pyg.mixer.music.stop()
                pyg.mixer.music.load('empty.wav')
                pyg.mixer.music.play(-1)

            pressed_keys = pyg.key.get_pressed()
            # next 4 ifs allow player to move rooms by going through unlocked door
            if origin.right != None and not teleported:
                if player.get_position()[0] >= 1130:
                    in_position = (290 <= player.get_position()[1] <= 378)
                    if in_position and pressed_keys[pyg.K_d]:
                        origin = origin.right
                        loadRoom(board, origin, all_sprites, proj_enemies)
                        player.rect.centerx = 50
                        teleported = True
            
            if origin.left != None and not teleported:
                if player.get_position()[0] <= 90:
                    in_position = (290 <= player.get_position()[1] <= 378)
                    if in_position and pressed_keys[pyg.K_a]:
                        origin = origin.left
                        loadRoom(board, origin, all_sprites, proj_enemies)
                        player.rect.centerx = 1050
                        teleported = True
            
            if origin.top != None and not teleported:
                if player.get_position()[1] <= 90:
                    in_position = (575 <= player.get_position()[0] <= 663)
                    if in_position and pressed_keys[pyg.K_w]:
                        origin = origin.top
                        loadRoom(board, origin, all_sprites, proj_enemies)
                        player.rect.centery = 510
                        teleported = True
            
            if origin.bottom != None and not teleported:
                if player.get_position()[1] >= 520:
                    in_position = (575 <= player.get_position()[0] <= 663)
                    if in_position and pressed_keys[pyg.K_s]:
                        origin = origin.bottom
                        loadRoom(board, origin, all_sprites, proj_enemies)
                        player.rect.centery = 50
                        teleported = True
            
            if not all_sprites.has(powerup_giver) and origin.cleared and not origin.collected:
                loadRoom(board, origin, all_sprites, proj_enemies)
            board.change = True

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                running = False  # setting up the window to close when the close button is hit
                pyg.quit()
                sys.exit()

            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_1:
                    pass
                    # player.heal(15)
                if event.key == pyg.K_ESCAPE:
                    pause(difficulty=difficulty)    # pauses game when escape key is pressed
        if player.current_health <= 0:  # displays death screen when player health goes to 0
            pause(difficulty=difficulty, game_status="dead", score=total_killed, p_time=time)

        board.update()          # update board (doors and obstacles)
        all_sprites.update()    # update characters (player, enemies, projectiles)
    
        for character in all_sprites:   # check for wall collision
            collide_wall(character, walls)

        for enemy in proj_enemies:  # spawns projectiles when projectile enemies' cooldowns reach 0
            if type(enemy) == char.Skeleton and enemy.get_attack_cooldown() == 0:
                projectile = char.Projectile(bone_img, screen, player, enemy.rect.center[0], enemy.rect.center[1])
                projectile.add(all_sprites)
                enemy.reset_attack_cooldown()
            elif type(enemy) == char.Boss:
                if enemy.current_health <= 0:
                    pause(difficulty=difficulty, game_status='won', score= total_killed, p_time=time)
                if enemy.get_attack_cooldown() == 0:
                    # allows boss to spawn projectiles from 4 locations on his body
                    spawn_points = [(enemy.rect.centerx-73, enemy.rect.centery+65),
                                    (enemy.rect.centerx+69, enemy.rect.centery+65),
                                    (enemy.rect.centerx-71, enemy.rect.centery+18),
                                    (enemy.rect.centerx+85, enemy.rect.centery-15)]
                    rand = random.randint(0, 3)
                    projectile = char.Projectile(circle_img, screen, player, spawn_points[rand][0], spawn_points[rand][1],
                                                 spawn_anim=True)
                    projectile.add(all_sprites)
                if enemy.get_spec_attacking():
                    if enemy.spec_attack_counter % 4 == 0:
                        # spawns a projectile every 4 ticks while boss is special attacking
                        projectile = char.Projectile(circle_img, screen, player, enemy.rect.centerx, enemy.rect.centery-20,
                                                    spawn_anim=True)
                        projectile.add(all_sprites)

        left, middle, right = pyg.mouse.get_pressed()
        if left:
            if player.get_attack_cooldown() == 0:   # spawns attack in direction player clicks
                swoosh.play()
                attack = char.Attack(attack_img, screen, splat, player, all_sprites, player.rect.center[0], player.rect.center[1])
                attack.add(all_sprites)
                player.reset_attack_cooldown()

        all_sprites.clear(screen, background_img)   # clears sprites with background image
        rect_list = all_sprites.draw(screen)        # draws sprites in new locations
        pyg.display.update(rect_list)               # updates only the parts of the screen that have changed
        clock.tick(30)  # controls tick speed


def main_menu(fromTutorial=False, difficulty = 0):
    """this is the function that is called when the game is launched"""
    pyg.display.set_caption('Menu')
    if not fromTutorial:
        pyg.mixer.music.stop()
        pyg.mixer.music.load('menu.wav')
        pyg.mixer.music.play(-1)

    while True:
        screen.blit(menu_img, (0, 0))
        icon = pyg.image.load('dragon.png')  # change dragon.png to the art for our title
        pyg.display.set_icon(icon)
        menu_mouse_pos = pyg.mouse.get_pos()
        
        start_button = char.Button(button_surface, pos=[170, 500], font=get_font(25), text_input='Start Game', base_color="white", hovering_color='black')
        options_button = char.Button(button_surface, pos=[470, 500], font=get_font(25), text_input='Options', base_color="white", hovering_color='black')
        exit_button = char.Button(button_surface, pos=[1070, 500], font=get_font(25), text_input='Quit Game', base_color="white", hovering_color='red')
        tutorial_button = char.Button(button_surface, pos=[770, 500], font=get_font(25), text_input='Instructions', base_color='white', hovering_color='black')

        for button in [start_button, options_button, exit_button, tutorial_button]:
            button.change_color(menu_mouse_pos)
            button.update(screen)
        
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                sys.exit()

            if event.type == pyg.MOUSEBUTTONDOWN:
                if exit_button.input_check(menu_mouse_pos):
                    pyg.quit()
                    sys.exit()

                if start_button.input_check(menu_mouse_pos):
                    resetGame(difficulty=difficulty)
                
                if tutorial_button.input_check(menu_mouse_pos):
                    tutorial_window(difficulty=difficulty)
                
                if options_button.input_check(menu_mouse_pos):
                    options_window(difficulty=difficulty)
        pyg.display.update() 


def tutorial_window(difficulty=0):
    """determines what shows up on tutorial window"""
    pyg.display.set_caption('Instructions')
    while True:
        screen.fill((24,20,37)) #blue background w the same rgb tuple as the main menu screen
        icon = pyg.image.load('dragon.png')  # change dragon.png to the art for our title
        pyg.display.set_icon(icon)
        menu_mouse_pos = pyg.mouse.get_pos()

        back_button = char.Button(button_surface, pos=[1100, 550], font=get_font(25), text_input='Back', base_color="white", hovering_color='black')
        back_button.change_color(menu_mouse_pos)
        back_button.update(screen)

        #text using the button class
        instructions = char.Button(None, pos=[170, 50], font=get_font(40), text_input='INSTRUCTIONS', base_color=(90,105,136), hovering_color=(90,105,136))
        move_inst = char.Button(None, pos=[300, 120], font=get_font(25), text_input='To move your character, use the WASD keys.', base_color='white', hovering_color='white')
        attack_inst = char.Button(None, pos=[587, 170], font=get_font(25), text_input='To attack an enemy character, approach them using the WASD keys and left click in their direction.', base_color='white', hovering_color='white')
        dungeon_clear_inst = char.Button(None, pos=[400, 240], font=get_font(25), text_input='Once you kill all the enemies in any room, you will receive:', base_color='white', hovering_color='white')
        power_up = char.Button(None, pos=[340, 280], font=get_font(25), text_input='A power-up from the fairy.', base_color='white', hovering_color='white')
        room_access = char.Button(None, pos=[400, 320], font=get_font(25), text_input='Access to other rooms in the dungeon.', base_color='white', hovering_color='white')
        game_clear = char.Button(None, pos=[500, 420], font=get_font(25), text_input='To win the game, you must defeat the dungeon master waiting in one of the rooms!', base_color='white', hovering_color='white')
        pause_inst = char.Button(None, pos=[170, 520], font=get_font(18), text_input='*Press escape to pause', base_color='white', hovering_color='white')

        for button in [back_button, instructions, move_inst, attack_inst, dungeon_clear_inst, power_up, room_access, game_clear, pause_inst]:
            button.change_color(menu_mouse_pos)
            button.update(screen)
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                sys.exit()
            if event.type == pyg.MOUSEBUTTONDOWN:
                if back_button.input_check(menu_mouse_pos):
                    main_menu(difficulty=difficulty, fromTutorial=True)
        #needs the instructions
        #needs the back to main menu button
        pyg.display.update()         


def options_window(difficulty = 0):
    # determines what shows up on options window
    pyg.display.set_caption('Options')

    while True:
        screen.fill((24,20,37))
        icon = pyg.image.load('dragon.png') 
        pyg.display.set_icon(icon)
        menu_mouse_pos = pyg.mouse.get_pos()

        back_button = char.Button(button_surface, pos=[1100, 550], font=get_font(25), text_input='Back', base_color="white", hovering_color='black')
        back_button.change_color(menu_mouse_pos)
        back_button.update(screen)

        options = char.Button(None, pos=[170, 50], font=get_font(40), text_input='OPTIONS', base_color=(90,105,136), hovering_color=(90,105,136))
        fullscreen_button = char.Button(button_surface, pos=[600, 200], font=get_font(25), text_input='Go Fullscreen', base_color="white", hovering_color='black')
        difficulty_text = char.Button(None, pos=[600, 300], font=get_font(35), text_input='Set Difficulty', base_color="grey", hovering_color='grey')
        difficulty_increase_button = char.Button(None, pos=[680, 400], font=get_font(25), text_input='>', base_color="white", hovering_color='black')
        difficulty_decrease_button = char.Button(None, pos=[520, 400], font=get_font(25), text_input='<', base_color="white", hovering_color='black')
        
        for button in [back_button, options, fullscreen_button, difficulty_increase_button, difficulty_decrease_button, difficulty_text]:
            button.change_color(menu_mouse_pos)
            button.update(screen)

        for event in pyg.event.get():

                if event.type == pyg.QUIT: 
                    pyg.quit()
                    sys.exit()
                if event.type == pyg.MOUSEBUTTONDOWN:
                    if back_button.input_check(menu_mouse_pos):
                        main_menu(fromTutorial=True, difficulty=difficulty)
                    if fullscreen_button.input_check(menu_mouse_pos):
                        pyg.display.toggle_fullscreen()

                    if difficulty_decrease_button.input_check(menu_mouse_pos):
                        difficulty -= 1
                        if difficulty <= -1:
                            difficulty = -1
                    if difficulty_increase_button.input_check(menu_mouse_pos):
                        difficulty += 1
                        if difficulty >= 1:
                            difficulty = 1
                
        if difficulty == 1:
            font=pyg.freetype.SysFont('Times New Roman', 28)
            font.origin=True
            font.render_to(screen, (540, 410), 'Impossible', pyg.Color('grey'))
        if difficulty == 0:
            font=pyg.freetype.SysFont('Times New Roman', 28)
            font.origin=True
            font.render_to(screen, (560, 410), 'Normal', pyg.Color('grey'))
        if difficulty == -1:
            font=pyg.freetype.SysFont('Times New Roman', 28)
            font.origin=True
            font.render_to(screen, (570, 410), 'Easy', pyg.Color('grey'))
        
        pyg.display.update() 


if __name__ == '__main__':
    # making a screen
    screen = pyg.display.set_mode((1024 * 1.2, 512 * 1.2), pyg.SCALED)  # in landscape mode like all good games are
    clock = pyg.time.Clock()

    # loading sound
    swoosh = pyg.mixer.Sound('missed_target.wav')
    splat = pyg.mixer.Sound('sword_swing.wav')
    bloop = pyg.mixer.Sound('powerup.wav')

    # image loading module
    attack_img = load_image('attack.png', 0.3)
    attack_img = pyg.transform.rotate(attack_img, 20)
    player1_img = load_image('cat.png', .15)
    background_img = load_image('background_rect.png', 1.2)
    skeleton_img = load_image('skeleton.png', .13)
    gskeleton_img = load_image('gskeleton.png', .13)
    bat_img = load_image('bat.png', .15)
    rbat_img = load_image('rbat.png', .15)
    bone_img = load_image('bone.png', .2)
    button_surface = load_image('menu_button.png', 0.75)
    menu_img = load_image('bg.png', 1.2)
    goblin_img = load_image('goblin.png', .15)
    bgoblin_img = load_image('bgoblin.png', .15)
    cover_img = load_image('cover_up.png', 0.5)
    power_giver_img = load_image('powerup_giver.png', .35)
    boss_img = load_image('omnipotent_being.png', .2)
    circle_img = load_image('circle.png', .05)
    # list of enemy images
    enemy_imgs = [skeleton_img, gskeleton_img, goblin_img, bgoblin_img, bat_img, rbat_img, boss_img]

    # locked and unlocked doors in all 4 directions
    left_locked = load_image_location('locked.png', .31, 0, 225)
    left_unlocked = load_image_location('unlocked.png', .416, 0, 225)
    right_locked = load_image_location('locked.png', .31, 1160, 225)
    right_unlocked = load_image_location('unlocked.png', .416, 1097, 225)
    right_locked.image = pyg.transform.rotate(right_locked.image, 180)
    right_unlocked.image = pyg.transform.rotate(right_unlocked.image, 180)
    top_locked = load_image_location('locked.png', .31, 510, 0)
    top_unlocked = load_image_location('unlocked.png', .416, 510, 0)
    top_locked.image = pyg.transform.rotate(right_locked.image, 90)
    top_unlocked.image = pyg.transform.rotate(right_unlocked.image, 90)
    bottom_locked = load_image_location('locked.png', .31, 510, 546)
    bottom_unlocked = load_image_location('unlocked.png', .416, 510, 483)
    bottom_locked.image = pyg.transform.rotate(right_locked.image, 270)
    bottom_unlocked.image = pyg.transform.rotate(right_unlocked.image, 270)

    # boss doors
    bossleft_locked = load_image_location('bosslocked.png', .31, -2, 150)
    bossleft_unlocked = load_image_location('bossunlocked.png', .31, -2, 150)
    bossright_locked = load_image_location('bosslocked.png', .31, 1157, 150)
    bossright_unlocked = load_image_location('bossunlocked.png', .31, 1118, 150)
    bossright_locked.image = pyg.transform.rotate(bossright_locked.image, 180)
    bossright_unlocked.image = pyg.transform.rotate(bossright_unlocked.image, 180)
    bosstop_locked = load_image_location('bosslocked.png', .31, 450, -2)
    bosstop_unlocked = load_image_location('bossunlocked.png', .31, 450, -2)
    bosstop_locked.image = pyg.transform.rotate(bossright_locked.image, 90)
    bosstop_unlocked.image = pyg.transform.rotate(bossright_unlocked.image, 90)
    bossbottom_locked = load_image_location('bosslocked.png', .31, 450, 543)
    bossbottom_unlocked = load_image_location('bossunlocked.png', .31, 450, 503)
    bossbottom_locked.image = pyg.transform.rotate(bossright_locked.image, 270)
    bossbottom_unlocked.image = pyg.transform.rotate(bossright_unlocked.image, 270)

    # lists of doors
    locks = [left_locked, right_locked, top_locked, bottom_locked]
    unlocks = [left_unlocked, right_unlocked, top_unlocked, bottom_unlocked]
    bosslocks = [bossleft_locked, bossright_locked, bosstop_locked, bossbottom_locked]
    bossunlocks = [bossleft_unlocked, bossright_unlocked, bosstop_unlocked, bossbottom_unlocked]

    # obstacles
    rock1_img = load_image('rock1.png', 0.3)
    rock2_img = load_image('rock2.png', 0.3)
    rock3_img = load_image('rock3.png', 0.2)
    bone2_img = load_image('bone2.png', 0.3)
    obstacle_imgs = [rock1_img, rock2_img, rock3_img, bone2_img]

    # starts the game
    main_menu()
