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

    def change_item(self, new_type_shield, new_type_sword, item):

        self.item = item
        self.image.set_image(f"Knight1/Inventory/{new_type_shield}_{new_type_sword}.png") 

background = StillImage(0, 0, 800, 800, "select_background.png")
knight_custom = Item( "Knight_1/Inventory/wooden_iron.png", 250, -300, 128, 128, "sword")
knight_custom.resize(640, 640)

wooden_sword = StillImage(100, 370, 200, 200, "wooden_sword.png")
iron_sword = StillImage(300, 400, 150, 150, "iron_sword.png")
diamond_sword = StillImage(500, 410, 120, 120, "diamond_sword.png")

wooden_shield = StillImage(100, 600, 128, 128, "wooden_shield.png")
iron_sheild = StillImage(300, 600, 128, 128, "iron_shield.png")
diamond_sheild = StillImage(500, 600, 128, 128, "diamond_shield.png")

def inventory(window):

    mouse_x, mouse_y = mouse.get_pos()

    background.draw(window)
    knight_custom.draw(window)

    wooden_sword.draw(window)
    iron_sword.draw(window)
    diamond_sword.draw(window)

    wooden_shield.draw(window)
    iron_sheild.draw(window)
    diamond_sheild.draw(window)

    return True