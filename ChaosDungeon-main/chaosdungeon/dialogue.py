import pygame as pyg
import sys
import main


class Script():
    """Script reads and formats text files for the dialogue"""
    def __init__ (self, file):
        self.file = file
        self.queue = []
        self.reformatted = []

        # Automatically read text file and store every line on a list
        file = open(self.file, 'r', encoding='utf-8')
        self.queue = file.readlines()
        file.close()
    
    def reformat(self):
        # This function reformats the list of text so that it can be used in Scene
        copy = self.queue.copy()
        line = copy.pop(0)
        while len(copy) != 0:
            if line[0] == "-" or line[0] == "*" or line[0] == "+" or line[0] == "~":
                self.reformatted.append(line[0])
                line = copy.pop(0)
                box = ""
                while line[0] != "-" and line[0] != "*" and line[0] != "+" and line[0] != "~":
                    box = box + line
                    line = copy.pop(0)
                self.reformatted.append(box)
                if len(copy) > 0:
                    line = copy.pop(0)


class Dialogue(pyg.sprite.Sprite):
    """Dialogue directly alters the screen and puts text on the screen"""
    def __init__(self, screen, font, text_color, db_image, spkr1,  text = "", spkr2 = None ):
        pyg.sprite.Sprite.__init__(self)
        self.font = font
        self.screen = screen
        self.text_color = text_color
        self.lastChoice = None
        
        # dialogue box
        self.db_img = db_image
        self.db_x = self.db_img.get_width() # the width of the db
        self.db_y = self.db_img.get_height() # the height of the db
        self.x_pos = (self.screen.get_width()-self.db_x)/2 # the x_pos of the db
        self.y_pos = (self.screen.get_height()/2 - self.db_y)/2 + self.screen.get_height()/2 # the y pos of the db
        self.x = self.x_pos + 40
        self.y = self.y_pos + 60
        self.db_rect = self.db_img.get_rect()
        self.spkr1 = spkr1
        #self.spkr1 = pyg.transform.scale(spkr1, (int(screen.get_width()*3/18), int(screen.get_height()/4*3)))
        self.spkr1_rect = self.spkr1.get_rect().move((screen.get_width()/6,screen.get_height()/10))
        if spkr2 != None:
            size = spkr2.get_size()
            self.spkr2 = pyg.transform.scale(spkr2, (size[0]*.6, size[1]*.6))
            # self.spkr2 = pyg.transform.scale(spkr2, (int(screen.get_width()*3/10), int(screen.get_height()/6*4)))
            self.spkr2_rect = self.spkr2.get_rect().move((screen.get_width()/7*4, screen.get_height()/9))
        else:
            self.spkr2 = None


        # text box
        self.text_input = text
        self.text = self.font.render(self.text_input, True, self.text_color)
        self.text_rect = self.text.get_rect(topleft = (self.x_pos, self.y_pos), topright= ((self.x_pos + self.db_x), self.y_pos))

    # display the diolog box image
    def db_display(self):
        self.screen.blit(self.db_img, [self.x_pos, self.y_pos])
    
    def display_player(self):
        self.screen.blit(self.spkr1, self.spkr1_rect)
        if self.spkr2 != None:
            self.screen.blit(self.spkr2, self.spkr2_rect)

    # update the dialogue box
    def update(self, screen):
        self.display_player()
        self.db_display()
        words = []
        for word in self.text_input.split("\n"):
            if word != None:
                words.append(word.split(' '))
        space = self.font.size(' ')[0]
        max_width, max_height = self.text.get_size()
        max_width = 990
        x = self.x
        y = self.y
        for line in words:
            for word in line:
                word_surface = self.font.render(word, 0, self.text_color)
                
                word_width, word_height = word_surface.get_size()

                if x + word_width >= max_width:
                    x = self.x
                    y += word_height
                screen.blit(word_surface, (x,y))
                x+= word_width + space
            x = self.x
            y += word_height


def get_input():
    # This function waits for a number input from the user and returns that number
    while True: 
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                sys.exit()

            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_1:
                    return 1
                elif event.key == pyg.K_2:
                    return 2
                elif event.key == pyg.K_3:
                    return 3
                elif event.key == pyg.K_4:
                    return 4


def scene(screen, file, bloop, s2=None, lastInput=None):
    # This function reads a formatted list of text and feeds it into dialogue
    # This function also waits for user inputs
    pyg.font.init()

    script = Script(file)
    script.reformat()

    reformatCopy = script.reformatted

    font = pyg.font.Font('freesansbold.ttf', 20)
    white = (255, 255, 255)

    transparent = pyg.Surface([screen.get_width(),screen.get_height()], pyg.SRCALPHA, 32)
    transparent = transparent.convert_alpha()
    black = pyg.Surface([screen.get_width(),screen.get_height()])
    black.fill(pyg.color.Color(0,0,0))
    black = black.convert_alpha()
    screen.blit(transparent, (0,0))


    db = pyg.image.load('db3.png')
    player = main.load_image('player.png', .65)
    omni = main.load_image('omnipotent.png', 1)
    giver = main.load_image('giver.png', .5)

    spkr1 = player

    # Check who is speaker 2
    if s2 == "omni":
        spkr2 = omni
    elif s2 == "giver":
        spkr2 = giver
    else:
        spkr2 = None

    pyg.display.update()

    while len(reformatCopy) != 0:
        lineType = reformatCopy.pop(0)
        # Normal dialogue
        if lineType[0] == '-':
            dialogue = Dialogue(screen, font, white, db, spkr1, reformatCopy.pop(0), spkr2)
            dialogue.display_player()
            dialogue.db_display()
            dialogue.update(screen)
            pyg.display.update()
            waiting = True
            while waiting:
                for event in pyg.event.get():
                    if event.type == pyg.QUIT:
                        pyg.quit()
                        sys.exit()
                    if event.type == pyg.KEYDOWN:
                        if event.key == pyg.K_SPACE:
                            waiting = False
        
        # Numerical input expected
        if lineType[0] == '*':
            dialogue = Dialogue(screen, font, white, db, spkr1, reformatCopy.pop(0), spkr2)
            dialogue.display_player()
            dialogue.db_display()
            dialogue.update(screen)
            pyg.display.update()
            lastInput = get_input()
        
        # Dialogue will give player powerup
        if lineType[0] == '+':
            for i in range(2*(lastInput - 1)):
                reformatCopy.pop(0)
            dialogue = Dialogue(screen, font, white, db, spkr1, reformatCopy.pop(0), spkr2)
            dialogue.display_player()
            dialogue.db_display()
            dialogue.update(screen)
            pyg.display.update()
            bloop.play()
            waiting = True
            while waiting:
                for event in pyg.event.get():
                    if event.type == pyg.KEYDOWN:
                        if event.key == pyg.K_SPACE:
                            waiting = False
            for i in range(2*(4 - lastInput)):
                reformatCopy.pop(0)
        
        # Branching dialogue
        if lineType[0] == '~':
            for i in range(2*(lastInput - 1)):
                reformatCopy.pop(0)
            dialogue = Dialogue(screen, font, white, db, spkr1, reformatCopy.pop(0), spkr2)
            dialogue.display_player()
            dialogue.db_display()
            dialogue.update(screen)
            pyg.display.update()
            waiting = True
            while waiting:
                for event in pyg.event.get():
                    if event.type == pyg.KEYDOWN:
                        if event.key == pyg.K_SPACE:
                            waiting = False
            for i in range(2*(4 - lastInput)):
                reformatCopy.pop(0)
    
    return lastInput


if __name__ == '__main__':
    pyg.init
    pyg.mixer.init()
    bloop = pyg.mixer.Sound('powerup.wav')
    scene(pyg.display.set_mode((1024,512)), 'powerup.txt', bloop)