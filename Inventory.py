from pygame import *
import json
from AnimatedSprite import *
from StillImage import *

class Item(AnimatedSprite):

    def __init__(self, filename, x, y, w, h, item): 
        super().__init__(filename, x, y, w, h)       
        
        self.item = item
        with open ("upgrades.json", "r") as file:
            data =  json.load(file)
        self.type =  data[2]["type"][self.item]

    def change_item(self, new_type_sheild, new_type_sword, item):

        self.item = item
        self.set_image(f"Knight_1/Inventory/{new_type_sheild}_{new_type_sword}.png") 

background = StillImage(0, 0, 800, 800, "select_background.png")

with open ("upgrades.json", "r") as file:
    data = json.load(file)

knight_custom = Item(f"Knight_1/Inventory/{data[2]['type']['sword']}_{data[2]['type']['sheild']}.png", 250, -300, 128, 128, "sword")
knight_custom.resize(640, 640)

wooden_sword = StillImage(100, 370, 200, 200, "wooden_sword.png")
iron_sword = StillImage(339, 410, 120, 120, "iron_sword.png")
diamond_sword = StillImage(550, 420, 100, 100, "diamond_sword.png")

wooden_sheild = StillImage(137, 600, 128, 128, "wooden_shield.png")
iron_sheild = StillImage(337, 600, 128, 128, "iron_shield.png")
diamond_sheild = StillImage(537, 600, 128, 128, "diamond_shield.png")

unlocked = data[2]["unlocked"]
unlocked_keys = list(unlocked.keys())
padlocks = []

start_x = 100 
start_y_top = 340
start_y_bottom = 540
spacing_x = 200

col_index = 1
row_toggle = 0 

for i, unlocked_key in enumerate(unlocked_keys):
    y = start_y_top if i % 2 == 0 else start_y_bottom

    if unlocked[unlocked_key]:
        x = start_x 
    else:
        x = start_x + spacing_x * col_index

        if row_toggle == 1:
            col_index += 1

    if not unlocked[unlocked_key]:
        row_toggle = 1 - row_toggle

        padlock = StillImage(x, y, 200, 200, "padlock.png")
        padlock.set_alpha(90)
        padlocks.append(padlock)


def inventory(window):

    mouse_x, mouse_y = mouse.get_pos()

    background.draw(window)
    knight_custom.draw(window)

    wooden_sword.draw(window)
    iron_sword.draw(window)
    diamond_sword.draw(window)

    wooden_sheild.draw(window)
    iron_sheild.draw(window)
    diamond_sheild.draw(window)

    for padlock in padlocks:
        padlock.draw(window)

    return True