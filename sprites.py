
import os
import pygame as pg
from settings import *

vect = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self,  spriteSheet, startx, starty,\
        maxWidth, idleList, walkList, jumpList,\
        leftKey=pg.K_LEFT, rightKey=pg.K_RIGHT):
        super().__init__()
        
        self.maxWidth = maxWidth
        try:            
            # Load image from spritesheet + resize
            #~ self.sheetPath = os.path.join(img_dir, spriteSheet)
            #~ self.image = self.grabSpriteFromSheet(self.sheetPath,\
                #~ imgSheetLoc, maxWidth)
                
            # Load animation images from dictionary
            self.idleImgs = self.loadAnimImages(spriteSheet, idleList)
            self.idleImgs.append(pg.transform.flip(self.idleImgs[0], True, False))
            self.jumpImg = self.loadAnimImages(spriteSheet, jumpList)[0]
            self.walkImgsR = self.loadAnimImages(spriteSheet, walkList)
            self.walkImgsL = []
            for img in self.walkImgsR:
                self.walkImgsL.append(pg.transform.flip(img, True, False))
            
            self.image = self.idleImgs[0]
        except:
            self.image = pg.Surface((30, 40))
            self.image.fill(GOLD)
        self.sm_img = self.scaleImg(self.image, 10)
        self.sm_img_rect = self.sm_img.get_rect()
        self.rect = self.image.get_rect()
        #~ self.rect.center = (startx, starty)        
        self.pos = vect(startx, starty)
        self.vel = vect(0,0)
        self.acc = vect(0,0)
        self.radius = int(self.rect.height/2)
        
        self.walking = False
        self.jumping = False
        self.rightFlag = True
        self.animDelay = 200
        self.lastAnim = 0
        self.currentFrame = 0
        
        self.leftKey = leftKey
        self.rightKey = rightKey
        
        #~ # Used to view instance self.rect
        #~ stan = pg.Surface((self.rect.width, self.rect.height))
        #~ stan.fill(GREY)
        #~ stan.set_alpha(100)
        #~ self.image.blit(stan, (0,0))
    
    def grabSpriteFromSheet(self, sheetPath, rect, maxWidth):
        self.sheet = pg.image.load(sheetPath).convert_alpha()
        x, y, width, height = rect
        
        img = pg.Surface((width, height))
        img.set_colorkey(BLACK)
        img.blit(self.sheet, (0,0), (x,y,width,height))
        
        img = self.scaleImg(img, maxWidth)
        
        return img
    
    def scaleImg(self, image, maxWidth):
        imgRect = image.get_rect()
        if imgRect.width > maxWidth or imgRect.width < maxWidth:
            img = pg.transform.scale(image,\
                (maxWidth, int((maxWidth*imgRect.height)/imgRect.width)))
            return img
        return image
    
    def loadAnimImages(self, spriteSheet, *args):
        sheetPath = os.path.join(img_dir, spriteSheet)
        imgList = []
        for i in args:
            for rect in i:
                img = self.grabSpriteFromSheet(sheetPath, rect, self.maxWidth)
                imgList.append(img)
        return imgList
    
    def animate(self, whichList):
        now = pg.time.get_ticks()
        if now - self.lastAnim > self.animDelay:
            self.lastAnim = now
            self.currentFrame += 1
            self.currentFrame %= len(whichList)
            bottom = self.rect.bottom
            self.image = whichList[self.currentFrame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom-5
    
    def move(self):
        # Use idle image if not moving
        if self.walking == False and self.jumping == False:
            #~ self.image = self.idleImgs[0]
            if self.rightFlag == True:
                self.image = self.idleImgs[0]
            else:
                self.image = self.idleImgs[1]
            self.rect = self.image.get_rect()
        
        # Use walking images if walking
        if self.walking == True and self.jumping == False:
            if self.vel.x > 0:
                self.rightFlag = True
                self.animate(self.walkImgsR)
            if self.vel.x < 0:
                self.rightFlag = False
                self.animate(self.walkImgsL)
        
        if self.jumping == True:
            bottom = self.rect.bottom
            self.image = self.jumpImg
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

        if self.vel.y != 0:
            self.jumping = True
        else:
            self.jumping = False
            
        self.acc = vect(0,PLAYER_GRAVITY)
        
        pressed = pg.key.get_pressed()
        if pressed[self.leftKey]:
            self.acc.x = -PLAYER_ACC
            self.walking = True
            
        elif pressed[self.rightKey]:
            self.acc.x = PLAYER_ACC
            self.walking = True
        else:
            self.walking = False
        
        # Apply horizontal friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        
        # Motion formulas
        self.vel += self.acc
        self.pos += self.vel + (0.5 * self.acc)
        
        self.rect.midbottom = self.pos
        
    def checkBounds(self):
        # Wrap around sides of screen
        half = int(self.rect.width/2)
        if self.pos.x < -half:
            self.pos.x = sWidth
        if self.pos.x > sWidth + half:
            self.pos.x = 0
    
    def jump(self, power=PLAYER_JUMP_POWER):
        # Jump only if standing on platform (not moving downward)
        if self.vel.y == 0:
            self.vel.y = -power
            
    def jumpShort(self):
        # Callback to KEYUP event
        # Cuts jump short
        if self.vel.y < -4:
            self.vel.y /= 2
    
    def update(self):
        self.move()
        self.checkBounds()
        #~ self.checkForDirection()        
        
class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        
        self.image = pg.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    
        
