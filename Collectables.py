from StillImage import *
import json
import random
import math

init()
mixer.init()

health_sound = mixer.Sound("health_sound.mp3")
health_sound.set_volume(0.1)

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
                health_sound.play()
                if self.lives < 5:
                    self.lives += 1
                    new_x = self.HEART_X_BASE + (self.lives - 1) * self.HEART_SPACING
                    self.hearts.append(StillImage(new_x, 0, 45, 45, "hearts.png"))
                self.collectables.remove(item)
                return False
            
        return True

    def lose_a_heart(self):
         
        if self.lives > 0:
            self.lives -= 1
            try:
                self.hearts.pop()
            except IndexError:
                pass

def lerp_colour(c1, c2, t):
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t)
    )

potion_collect = mixer.Sound("potion_sound.mp3")
potion_collect.set_volume(0.1)

class Potions():
    def __init__(self):
        self.potion = StillImage(random.randint(0, 710), random.choice([600, 715]), 70, 70, "strength_potion.png")
        self.draw_or_not = False
        self.active = False
        self.effect_duration = 15000
        self.start_time = None

        self.y_offset = -40
        self.small_height = 35
        self.small_width = 35

        self.follow_knight = False

    def spawn_collectable(self):
        self.potion = StillImage(random.randint(0, 710), random.choice([600, 715]), 70, 70, "strength_potion.png")
        self.draw_or_not = True
        self.active = False
        self.start_time = None

    def pick_up(self, knight_hitbox):
        if self.draw_or_not and knight_hitbox.colliderect(self.potion.rect):
            potion_collect.play()
            self.active = True
            self.start_time = time.get_ticks()
            
            self.follow_knight = True
            self.draw_or_not = False

    def draw(self, window, knight_rect, direction):

        if self.active and knight_rect:
            self.draw_effect(window, knight_rect, direction)

        if self.follow_knight and knight_rect:

            if direction == "right":
                self.potion.rect.centerx = knight_rect.x + knight_rect.width // 2 - 50

            else:
                self.potion.rect.centerx = knight_rect.x + knight_rect.width // 2 + 50
            self.potion.rect.y = knight_rect.top + 15
            scaled_image = transform.scale(self.potion.image, (self.small_width, self.small_height))
            window.blit(scaled_image, scaled_image.get_rect(center=self.potion.rect.center))
        
        elif self.draw_or_not:

            tick = time.get_ticks() // 500 % 2
            if tick == 0:
                self.potion.draw(window)
            else:
                ghost_image = self.potion.image.copy()
                ghost_image.set_alpha(100)
                window.blit(ghost_image, (self.potion.rect.x, self.potion.rect.y))

    def draw_effect(self, window, knight_rect, direction):
        elapsed = time.get_ticks() - self.start_time
        if elapsed > self.effect_duration:
            self.active = False
            self.follow_knight = False
            return

        if direction == "right":
            x = knight_rect.x + knight_rect.width // 2 - 50

        else:
            x = knight_rect.x + knight_rect.width // 2 + 50
        y = knight_rect.top + 48

        radius = 25
        circle_outline = (0, 0, 0)
        fill_start_colour = (131, 201, 242)
        fill_end_colour = (2, 12, 51)

        draw.circle(window, fill_start_colour, (x, y), radius)
        draw.circle(window, circle_outline, (x, y), radius, 2)

        progress =  min(elapsed / self.effect_duration, 1)
        fill_colour = lerp_colour(fill_start_colour, fill_end_colour, progress)

        start_angle = -math.pi / 2
        end_angle = start_angle + progress * 2 * math.pi

        points = [(x, y)]
        step = 0.01
        steps_count = int((end_angle - start_angle) / step) + 1
        for i in range(steps_count):
            angle = start_angle + i * step
            px = x + radius * math.cos(angle)
            py = y + radius * math.sin(angle)
            points.append((px, py))
        points.append((x, y))

        draw.polygon(window, fill_colour, points)