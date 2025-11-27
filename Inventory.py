from pygame import *
import json
from AnimatedSprite import *
from StillImage import *
from ResourceManager import *

class Item(AnimatedSprite):

    def __init__(self, filename, x, y, w, h): 
        super().__init__(filename, x, y, w, h)      
        self.x = x
        self.y = y
        self.w = w
        self.h = h 

        with open (resource_path("upgrades.json"), "r") as file:
            data =  json.load(file)
        self.sword =  data[2]["type"]["sword"]
        self.sheild = data[2]["type"]["sheild"]

        self.strength = 0
        self.hp = 0

    def change_item(self, new_type_sword, new_type_sheild):

        self.change_animation(resource_path(f"images/Knight_1/Inventory/{new_type_sword}_{new_type_sheild}.png"), self.w, self.h) 
        self.sword = new_type_sword
        self.sheild = new_type_sheild

background = StillImage(0, 0, 800, 800, resource_path("images/select_background.png"))

with open (resource_path("upgrades.json"), "r") as file:
    data = json.load(file)

knight_custom = Item(resource_path(f"images/Knight_1/Inventory/{data[2]['type']['sword']}_{data[2]['type']['sheild']}.png"), 250, -300, 128, 128)
knight_custom.resize(640, 640)

base_strength = data[0].get("strength", 0)
base_hp = data[0].get("hp", 0)

wooden_sword = StillImage(100, 370, 200, 200, resource_path("images/wooden_sword.png"))
iron_sword = StillImage(339, 410, 120, 120, resource_path("images/iron_sword.png"))
diamond_sword = StillImage(550, 420, 100, 100, resource_path("images/diamond_sword.png"))

wooden_sheild = StillImage(137, 600, 128, 128, resource_path("images/wooden_shield.png"))
iron_sheild = StillImage(337, 600, 128, 128, resource_path("images/iron_shield.png"))
diamond_sheild = StillImage(537, 600, 128, 128, resource_path("images/diamond_shield.png"))

unlocked = data[2]["unlocked"]
unlocked_keys = list(unlocked.keys())
padlocks = []

start_x = 100
start_y_top = 340
start_y_bottom = 540
spacing_x = 200

grid_order = [
    "wooden_sword", "iron_sword", "diamond_sword",
    "wooden_sheild", "iron_sheild", "diamond_sheild"
]
grid_positions = {}

for i, unlocked_key in enumerate(grid_order):
    row = 0 if i < 3 else 1
    col = i % 3
    x = start_x + spacing_x * col
    y = start_y_top if row == 0 else start_y_bottom

    grid_positions[unlocked_key] = (x, y)

    grid_positions[unlocked_key] = (x, y)

for unlocked_key in ["iron_sword", "diamond_sword", "iron_sheild", "diamond_sheild"]:
    if not unlocked[unlocked_key]:
        x, y = grid_positions[unlocked_key]
        padlock = StillImage(x, y, 200, 200, resource_path("images/padlock.png"))
        padlock.set_alpha(90)
        padlocks.append(padlock)

back_arrow = StillImage(5, 10, 90, 90, resource_path("images/back_arrow.png"))

mouse_was_pressed = False
inventory_mouse_consumed = False

def inventory(window, mouse_pressed):
    global mouse_was_pressed, inventory_mouse_consumed, base_strength, base_hp

    mouse_x, mouse_y = mouse.get_pos()
    current_mouse_pressed = mouse.get_pressed()[0]
    click = current_mouse_pressed and not mouse_was_pressed

    background.draw(window)
    knight_custom.draw(window)
    
    back_arrow.draw(window)

    wooden_sword.draw(window)
    iron_sword.draw(window)
    diamond_sword.draw(window)

    wooden_sheild.draw(window)
    iron_sheild.draw(window)
    diamond_sheild.draw(window)

    for padlock in padlocks:
        padlock.draw(window)

    if (mouse_x >= wooden_sword.rect.x and mouse_x <= wooden_sword.rect.x + wooden_sword.rect.width and mouse_y >= wooden_sword.rect.y and mouse_y <= wooden_sword.rect.y + wooden_sword.rect.height):
        if current_mouse_pressed:

            knight_custom.change_item("wooden", knight_custom.sheild)
            knight_custom.strength = data[2]["bonuses"]["wood"]
            data[2]["type"]["sword"] = "wooden"

    if (mouse_x >= iron_sword.rect.x and mouse_x <= iron_sword.rect.x + iron_sword.rect.width and mouse_y >= iron_sword.rect.y and mouse_y <= iron_sword.rect.y + iron_sword.rect.height):
        if current_mouse_pressed and unlocked["iron_sword"]:

            knight_custom.change_item("iron", knight_custom.sheild)
            knight_custom.strength = data[2]["bonuses"]["iron"]
            data[2]["type"]["sword"] = "iron"

    if (mouse_x >= diamond_sword.rect.x and mouse_x <= diamond_sword.rect.x + diamond_sword.rect.width and mouse_y >= diamond_sword.rect.y and mouse_y <= diamond_sword.rect.y + diamond_sword.rect.height):
        if current_mouse_pressed and unlocked["diamond_sword"]:

            knight_custom.change_item("diamond", knight_custom.sheild)
            knight_custom.strength = data[2]["bonuses"]["diamond"]
            data[2]["type"]["sword"] = "diamond"

    if (mouse_x >= wooden_sheild.rect.x and mouse_x <= wooden_sheild.rect.x + wooden_sheild.rect.width and mouse_y >= wooden_sheild.rect.y and mouse_y <= wooden_sheild.rect.y + wooden_sheild.rect.height):
        if current_mouse_pressed:

            knight_custom.change_item(knight_custom.sword, "wooden")
            knight_custom.hp = data[2]["bonuses"]["wood"]
            data[2]["type"]["sheild"] = "wooden"

    if (mouse_x >= iron_sheild.rect.x and mouse_x <= iron_sheild.rect.x + iron_sheild.rect.width and mouse_y >= iron_sheild.rect.y and mouse_y <= iron_sheild.rect.y + iron_sheild.rect.height):
        if current_mouse_pressed and unlocked["iron_sheild"]:

            knight_custom.change_item(knight_custom.sword, "iron")
            knight_custom.hp = data[2]["bonuses"]["iron"]
            data[2]["type"]["sheild"] = "iron"

    if (mouse_x >= diamond_sheild.rect.x and mouse_x <= diamond_sheild.rect.x + diamond_sheild.rect.width and mouse_y >= diamond_sheild.rect.y and mouse_y <= diamond_sheild.rect.y + diamond_sheild.rect.height):
        if current_mouse_pressed and unlocked["diamond_sheild"]:

            knight_custom.change_item(knight_custom.sword, "diamond")
            knight_custom.hp = data[2]["bonuses"]["diamond"]
            data[2]["type"]["sheild"] = "diamond"

    data[0]["strength"] = base_strength + knight_custom.strength
    data[0]["hp"] = base_hp + knight_custom.hp

    if (mouse_x >= back_arrow.rect.x and mouse_x <= back_arrow.rect.x + back_arrow.rect.width and mouse_y >= back_arrow.rect.y and mouse_y <= back_arrow.rect.y + back_arrow.rect.height) and click:
        with open (resource_path("upgrades.json"), "w") as file:
            json.dump(data, file, indent=4)
        
        mouse_was_pressed = current_mouse_pressed
        inventory_mouse_consumed = True

        return False

    mouse_was_pressed = current_mouse_pressed
    return True