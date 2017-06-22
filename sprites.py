
import os
import pygame as pg
import random
import sys
import traceback
from settings import *
vect = pg.math.Vector2

# These variables must be imported from a settings file or set here
#~ PLAYER_ACC = 
#~ PLAYER_FRICTION = 
#~ PLAYER_GRAVITY = 
#~ PLAYER_JUMP_POWER = 
#~ sWidth = 
#~ sHeight = 
#~ FPS = 
WHITE = (255,255,255)

    
class Player(pg.sprite.Sprite):
    def __init__(self,  spriteSheet, startx, starty,\
        maxWidth, idleList, walkList, jumpList,\
        leftKey=pg.K_LEFT, rightKey=pg.K_RIGHT):
        super().__init__()
        
        self.maxWidth = maxWidth
        self.sheet = spriteSheet
        self._layer = 2
        
        try:       
            # Load animation images from dictionary
            self.idleImgs = loadAnimImages(self.sheet, self.maxWidth, None, idleList)
            # Add left facing idle image
            self.idleImgs.append(pg.transform.flip(self.idleImgs[0], True, False))
            self.jumpImgs = loadAnimImages(self.sheet, self.maxWidth, None, jumpList)
            self.walkImgsR = loadAnimImages(self.sheet, self.maxWidth, None, walkList)
            self.walkImgsL = []
            for img in self.walkImgsR:
                self.walkImgsL.append(pg.transform.flip(img, True, False))
            
            self.image = self.idleImgs[0]
            
        except Exception as e:
            print(e)
            print(sys.exc_info()[0])
            print(traceback.format_exc())
            # Use generic surface if error loading images
            self.image = pg.Surface((30, 40))
            self.image.fill(WHITE)
        self.sm_img = scaleImg(self.image, 20, None)
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

    def animate(self, whichList):
        # Loop through list of images to animate sprite
        now = pg.time.get_ticks()
        if now - self.lastAnim > self.animDelay:
            self.lastAnim = now
            self.currentFrame += 1
            self.currentFrame %= len(whichList)
            bottom = self.rect.bottom
            self.image = whichList[self.currentFrame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom-5
            self.mask = pg.mask.from_surface(self.image)
    
    def move(self):
        # Use idle image if not moving
        if self.walking == False and self.jumping == False:
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
        # Use jumping image if jumping or falling
        if self.jumping == True:
            bottom = self.rect.bottom
            self.animate(self.jumpImgs)
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

        if self.vel.y != 0:
            self.jumping = True
        else:
            self.jumping = False
            
        self.acc = vect(0, PLAYER_GRAVITY)
        
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
    
    def jump(self, power, *args):
        # Jump only if standing on platform (not moving downward)
        if self.vel.y == 0:
            self.vel.y = -power
            for i in args:
                i.play()
            
    def jumpShort(self):
        # Callback to KEYUP event
        # Cuts jump short
        if self.vel.y < -4:
            self.vel.y /= 2
    
    def update(self):
        self.move()
        self.checkBounds()     

class SpinningMob(pg.sprite.Sprite):
    def __init__(self, spriteSheet, img_rect, maxWidth, maxHeight):
        super().__init__()
        
        self.sheet = spriteSheet
        self.maxWidth = maxWidth
        self.maxHeight = maxHeight
        self._layer = 2
        
        try:
            tmp_img = grabSpriteFromSheet(self.sheet, img_rect, self.maxWidth, None)
            self.spinMobImgs = [tmp_img]
            angle = 0
            for i in range(35):
                angle += 10
                self.spinMobImgs.append(pg.transform.rotate(tmp_img, angle))
            self.image = self.spinMobImgs[0]
        except Exception as e:
            print(e)
            print(sys.exc_info()[0])
            print(traceback.format_exc())
            #~ # Use generic surface if image load error
            self.image = pg.Surface((75, 75))
            self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.choice((-50, sWidth+50))
        self.rect.y = random.randint(0, sHeight/2)
        
        self.animDelay = 100
        self.lastAnim = 0
        self.currentFrame = 0
        
        self.xSpeed = random.choice((1, 2, 3))
        if self.rect.x > 0:
            self.xSpeed *= -1
        self.yAcc = random.choice((-.08, .08))
        self.ySpeed = 0

    def animate(self):
        # Loop through list of images to animate sprite
        if len(self.spinMobImgs) > 1:
            now = pg.time.get_ticks()
            if now - self.lastAnim > self.animDelay:
                self.lastAnim = now
                self.currentFrame += 1
                self.currentFrame %= len(self.spinMobImgs)
                center = self.rect.center
                self.image = self.spinMobImgs[self.currentFrame]
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.mask = pg.mask.from_surface(self.image)
        
    def update(self):
        self.animate()
        
        self.rect.x += self.xSpeed
        # Mobs move in wave pattern across screen
        self.ySpeed += self.yAcc
        self.rect.y += self.ySpeed
        if self.ySpeed >= 4 or self.ySpeed <= -3:
            self.yAcc *= -1
                
class Platform(pg.sprite.Sprite):
    def __init__(self, spriteSheet, img_rect, x, y, maxWidth=200, maxHeight=30):
        super().__init__()
        
        self.sheet = spriteSheet
        self.maxWidth = maxWidth
        self.maxHeight = maxHeight
        self._layer = 1
        
        try:
            self.image = grabSpriteFromSheet(self.sheet, img_rect, None, self.maxHeight)
        except Exception as e:
            print(e)
            print(sys.exc_info()[0])
            print(traceback.format_exc())
            #~ # Use generic surface if image load error
            self.image = pg.Surface((800, 20))
            self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
    def overrideWidth(self, width):
        imgRect = self.image.get_rect()
        tmp_ctr = self.rect.center
        self.image = pg.transform.scale(self.image,\
                (width, int((width*imgRect.height)/imgRect.width)))
        self.rect = self.image.get_rect()
        self.rect.center = tmp_ctr

    def update(self):
        pass
    
class Cloud(pg.sprite.Sprite):
    def __init__(self, spriteSheet, img_rect):
        super().__init__()
        
        self.sheet = spriteSheet
        self.maxHeight = random.randrange(30,81)
        self._layer = 0
        
        try:
            self.image = grabSpriteFromSheet(self.sheet, img_rect, None, self.maxHeight)
        except Exception as e:
            print(e)
            print(sys.exc_info()[0])
            print(traceback.format_exc())
            #~ # Use generic surface if image load error
            self.image = pg.Surface((300, 30))
            self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, sWidth)
        self.rect.y = random.randrange(-500, -50)
    
    def update(self):
        if self.rect.top>= sHeight*2:
            self.kill()

class Powerup(pg.sprite.Sprite):
    def __init__(self, platform, style, spriteSheet, img_rect, maxWidth, maxHeight):
        super().__init__()
        
        self.sheet = spriteSheet
        self.maxWidth = maxWidth
        self.maxHeight = maxHeight
        self.style = style
        self.platform = platform
        self._layer = 1
        
        try:            
            self.idleImgs = loadAnimImages(self.sheet, self.maxWidth, self.maxHeight, img_rect)
            self.image = self.idleImgs[0]
        except Exception as e:
            print(e)
            print(sys.exc_info()[0])
            print(traceback.format_exc())
            #~ # Use generic surface if image load error
            self.image = pg.Surface((20, 20))
            self.image.fill(WHITE)
            
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.platform.rect.midtop
        self.rect.y -= 5
        
        self.animDelay = 200
        self.lastAnim = 0
        self.currentFrame = 0
        
    def animate(self, whichList):
        # Loop through list of images to animate sprite
        if len(whichList) > 1:
            now = pg.time.get_ticks()
            if now - self.lastAnim > self.animDelay:
                self.lastAnim = now
                self.currentFrame += 1
                self.currentFrame %= len(whichList)
                midbottom = self.rect.midbottom
                self.image = whichList[self.currentFrame]
                self.rect = self.image.get_rect()
                self.rect.midbottom = midbottom
        
    def update(self):
        self.animate(self.idleImgs)
        self.rect.midbottom = self.platform.rect.midtop
        self.rect.y -= 5


def grabSpriteFromSheet(spriteSheet, rect, maxWidth, maxHeight):
    x, y, width, height = rect
    
    img = pg.Surface((width, height))
    #~ img.set_colorkey(BLACK)
    img.set_colorkey(img.get_at((1,1)))
    img.blit(spriteSheet, (0,0), (x,y,width,height))
    
    if maxHeight != None:
        img = scaleImg(img, None, maxHeight)
    if maxWidth != None:
        img = scaleImg(img, maxWidth, None)
    return img  
        
def scaleImg(image, maxWidth, maxHeight):
    # Scale images proportionally to a given width or height
    imgRect = image.get_rect()
    
    if maxWidth != None:
        if imgRect.width > maxWidth or imgRect.width < maxWidth:
            img = pg.transform.scale(image,\
                (maxWidth, int((maxWidth*imgRect.height)/imgRect.width)))
            return img
    if maxHeight != None:
        if imgRect.height > maxHeight or imgRect.height < maxHeight:
            img = pg.transform.scale(image,\
                (int((maxHeight*imgRect.width)/imgRect.height), maxHeight))
            return img
    return image
        
def loadAnimImages(spriteSheet, maxWidth, maxHeight, *args):
    imgList = []
    for i in args:
        for rect in i:
            img = grabSpriteFromSheet(spriteSheet, rect, maxWidth, maxHeight)
            imgList.append(img)
    return imgList

        
        
