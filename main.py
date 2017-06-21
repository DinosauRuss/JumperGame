
import os
import pygame as pg
import random
import sys
from settings import * 
from sprites import *

class Game():
    
    def __init__(self):
        # Initialize window, etc        
        pg.init()
        pg.mixer.init()
        os.environ['SDL_VIDEO_CENTERED'] = 'True'
        self.screen = pg.display.set_mode((sWidth, sHeight))
        pg.display.set_caption(TITLE)
        
        self.fontName = pg.font.match_font(FONT_NAME)
        
        self.clock = pg.time.Clock()
        self.programRunning = True

        self.turns = 3
        self.loadData()
        
        # Start background music playing
        pg.mixer.music.play(loops = -1)
    
    def new(self):
        # Start a new game       
        self.score = 0
        if self.turns <= 0:
            self.turns = 3
        
        # Create sprites/groups
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.dudes = pg.sprite.Group()
        self.clouds = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        
        self.player1 = Player(self.player_sheet, sWidth/2-30, sHeight*(3/4), 50,\
            PLAYER_IMAGES['idle'],\
            PLAYER_IMAGES['walking'],
            PLAYER_IMAGES['jumping'])
        self.addToGroups(self.player1, self.all_sprites, self.dudes)
        
        # Used to view instance self.rect        
        #~ pg.draw.circle(self.player1.image, (255,0,0), (tmp), self.player1.radius)
        #~ stan = pg.Surface((self.player1.rect.width, self.player1.rect.height))
        #~ stan.fill(GREY)
        #~ stan.set_alpha(100)
        #~ self.player1.image.blit(stan, (0,0))
        
        # Add a player 2
        #~ self.player2 = Player(P2_SPRITESHEET, sWidth/4, sHeight/4,\
            #~ (145, 0, 30, 63), 50, pg.K_s, pg.K_f)
        #~ self.all_sprites.add(self.player2)
        #~ self.dudes.add(self.player2)
        
        # Starting platforms
        for plat in START_PLATFORM_LIST:
            x, y = plat
            p = Platform(self.sprite_sheet, random.choice(list(PLATFORM_CHOICES.values())), x, y)
            self.addToGroups(p, self.all_sprites, self.platforms)
        p = Platform(self.sprite_sheet, (0, 768, 380, 94), sWidth/2, sHeight-55)
        p.overrideWidth(sWidth-50)
        self.addToGroups(p, self.all_sprites, self.platforms)
        
        for i in range(5):
            c = Cloud(self.cloud_sheet)
            c.rect.y += 500
            self.addToGroups(c, self.all_sprites, self.clouds)
        
        self.run()
    
    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            self.waitForEsc()
    
    def update(self):
        # Game Loop - Update
        
        # run update function for all sprites in group
        self.all_sprites.update()
        
        # Don't let platforms overlap
        for i in self.platforms:
            platCollisions = pg.sprite.spritecollide(i, self.platforms, False)
            if platCollisions:
                if platCollisions[0] == i:
                    pass
                else:
                    i.kill()
            
        # Check if player hits platform only if falling
        collisions = pg.sprite.spritecollide(self.player1,\
            self.platforms, False)
        if collisions:
            if self.player1.vel.y > 0:
                # land on lowest platform if touching multiple
                lowestPlat = collisions[0]
                for i in collisions:
                    if i.rect.bottom > lowestPlat.rect.bottom:
                        lowestPlat = i
                    
                if self.player1.pos.y <= lowestPlat.rect.bottom:
                    if self.player1.pos.x > lowestPlat.rect.left-5 and\
                        self.player1.pos.x < lowestPlat.rect.right+5:
                        self.player1.pos.y = lowestPlat.rect.top+1
                        # Add slight bounce when player lands
                        self.player1.vel.y *= -.25
                        if abs(self.player1.vel.y) < .2:
                            self.player1.vel.y = 0 
        
        # Powerups
        powerCollisions = pg.sprite.spritecollide(self.player1,\
            self.powerups, False)
        if powerCollisions:
            for i in powerCollisions:
                # Player shoots upward if bounces on a springv
                if self.player1.vel.y > 0 and\
                    powerCollisions[0].style == 'spring':
                    self.springSound.play()
                    self.player1.vel.y = -PLAYER_JUMP_POWER*2
                # Coin raises score
                if powerCollisions[0].style == 'coin':
                    self.coinSound.play()
                    i.kill()
                    self.score += 500
                    
       
        # Collision check if multiple players on screen            
        #~ hits = pg.sprite.groupcollide(self.dudes, self.platforms,\
            #~ False, False)
        #~ if hits:
            #~ for player, platform in hits.items():
                #~ if player.vel.y > 0:
                    #~ player.pos.y = platform[0].rect.top+1
                    #~ player.vel.y = 0
        
        self.scrollScreen()
        self.spawnNew() 
        self.checkForEnd()       

    def events(self):
        # Game Loop - Events
        for event in pg.event.get():
            # Check for window close button
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                    self.programRunning = False
                    
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.player1.jump(PLAYER_JUMP_POWER, self.jumpSound)
            #~ # Player2 control
            #~ if event.type == pg.KEYDOWN:
                #~ if event.key == pg.K_e:
                    #~ self.player2.jump()
            
            if event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    self.player1.jumpShort()

    def scrollScreen(self):
            # Check if player reaches top 1/4 of screen\
            # scroll accordingly
            if self.player1.rect.top <= sHeight/3:
                self.player1.pos.y += abs(self.player1.vel.y)
                
                for plat in self.platforms:
                    plat.rect.y += abs(self.player1.vel.y)
                    if plat.rect.top >= sHeight:
                        plat.kill()
                        self.score += 10
                for item in self.powerups:
                    item.rect.y += abs(self.player1.vel.y)
                    # Lose powerup if its platform goes away
                    if not self.platforms.has(item.platform):
                        item.kill()
                        self.score += 10
                
                # Small chance of spawning new cloud\
                # on every screen scoll
                if random.randrange(0,100) < 4:
                    c = Cloud(self.cloud_sheet)
                    self.addToGroups(c, self.all_sprites, self.clouds)
                for cloud in self.clouds:
                    # Larger clouds scroll more quickly
                    if cloud.rect.height >= 51:
                        cloud.rect.y += abs(self.player1.vel.y/2)
                    else:
                        cloud.rect.y += abs(self.player1.vel.y/3)

    def spawnNew(self):
        # Spawn new platforms above screen as player\
        # moves upward in world
        while len(self.platforms) < 6:            
            p = Platform(self.sprite_sheet,\
                random.choice(list(PLATFORM_CHOICES.values())),\
                random.randrange(0, sWidth-50),\
                random.randrange(-75, -30))
            self.addToGroups(p, self.all_sprites, self.platforms)
            
            # Spawn powerups randomly
            random_powerup = random.randrange(1,101)
            if random_powerup <= 5:
                j = Powerup(p, 'spring', self.sprite_sheet, POWERUP_IMGS['spring_out'], 30, None)
                self.addToGroups(j, self.all_sprites, self.powerups)
            if random_powerup >= 90:
                coin = Powerup(p, 'coin', self.sprite_sheet, POWERUP_IMGS['bronze_coin'], None, 30)
                self.addToGroups(coin, self.all_sprites, self.powerups)

    def checkForEnd(self):
        if self.player1.pos.y >= sHeight:          
            self.player1.rect.bottom = sHeight
            
            # Follow player down after falling
            self.player1.pos.y -= self.player1.vel.y
            
            # All other objects fly upward
            for plat in self.all_sprites:
                plat.rect.y -= min(10, self.player1.vel.y)
                # Delete platform when it leaves the screen
                if plat.rect.bottom < 0:
                    plat.kill()
                if len(self.platforms) == 0:
                    self.turns -= 1
                    self.playing = False

    def draw(self):
        # Game Loop - Draw
        
        #draw graphics
        self.screen.fill(BG_COLOR)
        self.all_sprites.draw(self.screen)   
        self.drawText(str(self.score), 30, GOLD, sWidth/2, 10)
        self.drawTurns()
        
        pg.display.flip()

    def drawText(self, text, size, color, x, y):
        # Draw some text to the screen
        font = pg.font.Font(self.fontName, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def drawTurns(self):
        # Visually show turns on screen
        for i in range(self.turns):
            w = self.player1.sm_img_rect.width
            xWhere = (sWidth-20)- (w*i*1.5)
            yWhere = 10
            self.screen.blit(self.player1.sm_img, (xWhere,yWhere))

    def showStartScreen(self):
        # Game start/splash screen
        self.drawText('Jumpy Jumper', 60, RED, sWidth/2, sHeight/4)
        self.drawText('Press Any Key to Start', 30, WHITE,\
            sWidth/2, sHeight/2)
        self.drawText('High Score: {}'.format(self.highScore), 30,\
            RED, sWidth/2, sHeight*(3/4))
        
        pg.display.flip()
        
        self.waitForKey()
    
    def showEndScreen(self):
        if self.programRunning != False:
            self.screen.fill(BLACK)
            self.drawText('Game Over', 75, RED, sWidth/2, sHeight/3)
            self.drawText('Score: {}'.format(self.score), 45, GOLD,\
                sWidth/2, sHeight/2)
            self.drawText('Press any key to play again', 20, WHITE,\
                sWidth/2, sHeight*.75)
            self.drawText('(esc) to quit', 20, WHITE,\
                sWidth/2, (sHeight*.75)+25)
            
            # Write high score to file
            if self.score > self.highScore:
                self.highScore = self.score
                with open(os.path.join(self_dir, FILENAME),\
                    'w') as f:
                    f.write('{}\n'.format(self.highScore))
                self.drawText('New High Score!',\
                    25, RED, sWidth/2, (sHeight/2)+50)
                            
            pg.display.flip()
            self.waitForKey()
        
    def waitForKey(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            self.waitForEsc()
            # Check for window close button
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.programRunning = False
                
                if event.type == pg.KEYUP:
                    waiting = False
    
    def loadData(self):
        # Load sprite sheets
        player_sheet_path = os.path.join(img_dir, P1_SPRITESHEET)
        self.player_sheet = pg.image.load(player_sheet_path).convert_alpha()
        sprite_sheet_path = os.path.join(img_dir, ENV_SPRITESHEET)
        self.sprite_sheet = pg.image.load(sprite_sheet_path).convert_alpha()
        cloud_path = os.path.join(img_dir, CLOUD)
        self.cloud_sheet = pg.image.load(cloud_path).convert_alpha()

        
        # Load high score file
        hsFile = os.path.join(self_dir, FILENAME)
        try:
            with open(hsFile, 'r+') as f:
                self.highScore = int(f.read())
        except:
            self.highScore = 0
        
        # Load sound files
        pg.mixer.music.load(os.path.join(snd_dir, SOUND_FILES['BG_MUSIC']))
        pg.mixer.music.set_volume(.5)
        self.jumpSound = pg.mixer.Sound(os.path.join(snd_dir, SOUND_FILES['JUMP']))
        self.jumpSound.set_volume(.3)
        self.coinSound = pg.mixer.Sound(os.path.join(snd_dir, SOUND_FILES['COINS']))
        self.springSound = pg.mixer.Sound(os.path.join(snd_dir, SOUND_FILES['SPRING']))
        self.ouchSound = pg.mixer.Sound(os.path.join(snd_dir, SOUND_FILES['OUCH']))

    def writeFile(self, score):
        with open(SCORE_FILE, 'w') as hs:
            hs.write(str(score))
            
    def waitForEsc(self):
        pressed = pg.key.get_pressed()
        if pressed[pg.K_ESCAPE]:
            self.playing = False
            self.programRunning = False

    def addToGroups(self, instance, *args):
        for i in args:
            i.add(instance)
    
def mainLoop():
    game = Game()
    game.showStartScreen()
    while game.programRunning:
        game.new()
        if game.turns <= 0:
            # only show end screen if no more turns
            game.showEndScreen()
            
    pg.quit()
    sys.exit()
    

if __name__ == '__main__':
    mainLoop()
    
