from StillImage import *
import json
import random

class Hearts():

    def __init__(self, lives_rate):

        self.lives_rate = lives_rate
        self.max_lives = 5
        self.lives = 5

        self.collectables = []

        self.hearts = []
        self.HEART_X_BASE = 135
        self.HEART_SPACING = 50
        self.last_spawn_time = time.get_ticks()
        self.COLLECTABLE_LIFETIME = 10000

        for i in range(5):
            heart = StillImage(self.HEART_X_BASE + i * self.HEART_SPACING, 0, 45, 45, "hearts.png")
            self.hearts.append(heart)

    def spawn_collectable(self, current_time):
        new_heart = StillImage(random.randint(-117, 710), random.choice([600, 715]), 45, 45, "hearts.png")
        self.collectables.append({
                "obj": new_heart,
                "spawn": current_time
            })

    def update(self, current_time):

        self.COLLECTABLE_LIFETIME = 10000

        for item in self.collectables[:]:
            if current_time - item["spawn"] > self.COLLECTABLE_LIFETIME:
                self.collectables.remove(item)

    def draw(self, window):
         
        for heart in self.hearts:
            heart.draw(window)

        for item in self.collectables:
            c = item["obj"]
            tick = time.get_ticks() // 500 % 2
            if tick == 0:
                c.draw(window)
            else:
                ghost_image = c.image.copy()
                ghost_image.set_alpha(100)
                window.blit(ghost_image, (c.rect.x, c.rect.y))

    def pick_up(self, knight_hitbox):
        
        for item in self.collectables[:]:
            
            collectable = item["obj"]
            if knight_hitbox.colliderect(collectable.rect):
                if self.lives < 5:
                    self.lives += 1
                    new_x = self.HEART_X_BASE + (self.lives - 1) * self.HEART_SPACING
                    self.hearts.append(StillImage(new_x, 0, 45, 45, "hearts.png"))
                self.collectables.remove(item)

    def lose_a_heart(self):
         
        if self.lives > 0:
            self.lives -= 1
            try:
                self.hearts.pop()
            except IndexError:
                pass

class Potions():

    def __init__(self):
        
        self.potion = StillImage(random.randint(-117, 710), random.choice([600, 715]), 70, 70, "strength_potion.png")

        self.draw_or_not = True

    def spawn_collectable(self, current_time):

        self.potion = StillImage(random.randint(-117, 710), random.choice([600, 715]), 70, 70, "strength_potion.png")
        self.spawn_time = current_time

        self.draw_or_not = True

    def draw(self, window):

        tick = time.get_ticks() // 500 % 2
        if tick == 0:
            self.potion.draw(window)
        else:
            ghost_image = self.potion.image.copy()
            ghost_image.set_alpha(100)
            window.blit(ghost_image, (self.potion.rect.x, self.potion.rect.y))

    def update(self, current_time):

        self.COLLECTABLE_LIFETIME = 10000

        for item in self.collectables[:]:
            if current_time - self.spawn_time > self.COLLECTABLE_LIFETIME:
                self.collectables.remove(item)

    def pick_up(self, knight_hitbox):

        if knight_hitbox.colliderect(self.potion.rect):

            self.draw_or_not = False