from pygame import *
import json
from AnimatedSprite import *
from StillImage import *

class Item(AnimatedSprite):

    def __init__(self, filename, x, y, w, h, item): 
        super().__init__(filename, x, y, w, h)       
        
        self.item = item
        with open ("upgrades.json", "r") as file:
            data =  json.load(file)[2]
        self.type = data[self.item]

    def change_item(self, new_type, item):

        self.item = item
        self.image.set_image(f"Knight1/Inventory/{new_type}.png") 
        self.type = new_type

background = StillImage(0, 0, 800, 800, "select_background.png")
knight_custom = Item( "Knight_1/Idle.png", 100, 100, 128, 128, "sword")
knight_custom.resize(640, 640)

def inventory(window):

    background.draw(window)
    knight_custom.draw(window)

    return True