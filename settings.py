import os

# Game settings
sWidth = 450
sHeight = 600
FPS = 60
TITLE = 'Gravity Game'
FONT_NAME = 'garamond'

# Define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GREY = (148,148,148)
GOLD = (255, 215, 0)
BG_COLOR = (204,229,255)

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.11
PLAYER_GRAVITY = 0.4
PLAYER_JUMP_POWER = 14

P1_IMAGE = (801, 609, 110, 141)

# Starting platform list
PLATFORM_LIST = [(0, sHeight-40, sWidth, 40),
                 ((sWidth/2)-50, sHeight*(3/4), 150, 20),
                 (125, sHeight-300, 100, 20),
                 (300, 200, 100, 20),
                 (175, 100, 50, 20)]

PLAYER_IMAGES = {'idle' : [(10, 4, 40, 58)],
                 'walking':[(74, 0 , 40, 62),
                            (136, 0 , 40, 62)],
                 'jumping': [(141, 208, 40, 60)]}
                 
# I/O
self_dir = os.path.dirname(__file__)
img_dir = os.path.join(self_dir, 'Images')

FILENAME = 'HighScore.txt'
SPRITESHEET = 'spritesheet_jumper.png'
P2_SPRITESHEET = 'dax.png'


