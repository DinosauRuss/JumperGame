import os

# Game settings
sWidth = 550
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
PLAYER_FRICTION = -0.10
PLAYER_GRAVITY = 0.4
PLAYER_JUMP_POWER = 14
                 
# I/O
self_dir = os.path.dirname(__file__)
img_dir = os.path.join(self_dir, 'Images')
snd_dir = os.path.join(self_dir, 'Sounds')

FILENAME = 'HighScore.txt'
ENV_SPRITESHEET = 'jumper.png'
P1_SPRITESHEET = 'dax.png'
CLOUD = 'cloud9.png'

SOUND_FILES = {'BG_MUSIC': 'Main-Theme.mp3',
               'JUMP': 'jump.ogg',
               'COINS': 'coins.wav',
               'SPRING': 'spring.ogg',
               'OUCH': 'scream.wav'}

# Starting platform list from ENV_SPRITESHEET
START_PLATFORM_LIST = [((sWidth/2)-50, sHeight/2),
                 (125, sHeight-300),
                 (300, 200),
                 (175, 100)]
                
# Locations from sprite sheet xml
PLATFORM_CHOICES = {'ground_grass_small_broken': (382, 204, 200, 100),
                    'ground_grass_broken': (0, 384, 380, 94),
                    'ground_grass': (0, 288, 380, 94),
                    'ground_grass_small': (213, 1662, 201, 100),
                    'ground_sand': (0, 672, 380, 94),
                    'ground_sand_small': (208, 1879, 201, 100),
                    'ground_sand_broken': (0, 1056, 380, 94),
                    'ground_sand_small_broken': (382, 102, 200, 100),
                    'ground_wood': (0, 960, 380, 94),
                    'ground_wood_broken': (0, 864, 380, 94),
                    'ground_wood_small': (218, 1558, 200, 100),
                    'ground_wood_small_broken': (382, 0, 200, 100)}
                    
POWERUP_IMGS = {'spring_out': [(434, 1265, 145, 110)],
                'bronze_coin': [(707, 296, 84, 84),
                                (826, 206, 66, 84),
                                (899, 116, 50, 84),
                                (670, 406, 14, 84),
                                (899, 116, 50, 84),
                                (826, 206, 66, 84)]}

# From P1_SPRITESHEET
PLAYER_IMAGES = {'idle' : [(10, 4, 40, 58)],
                 'walking':[(74, 0 , 40, 62),
                            (136, 0 , 40, 62)],
                 'jumping': [(141, 208, 40, 60)]}
                 
                 
                 


