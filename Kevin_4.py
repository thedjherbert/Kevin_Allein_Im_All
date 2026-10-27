
#       ▄█   ▄█▄    ▄████████  ▄█    █▄   ▄█  ███▄▄▄▄   
#      ███ ▄███▀   ███    ███ ███    ███ ███  ███▀▀▀██▄ 
#      ███▐██▀     ███    █▀  ███    ███ ███▌ ███   ███ 
#     ▄█████▀     ▄███▄▄▄     ███    ███ ███▌ ███   ███ 
#    ▀▀█████▄    ▀▀███▀▀▀     ███    ███ ███▌ ███   ███ 
#      ███▐██▄     ███    █▄  ███    ███ ███  ███   ███ 
#      ███ ▀███▄   ███    ███ ███    ███ ███  ███   ███ 
#      ███   ▀█▀   ██████████  ▀██████▀  █▀    ▀█   █▀  
#    
# 
#   Kevin 4: Kevin allein im All
#   Made by Carolin Willach, Emma Derkits
#   2025/26
#
#   ein kleiner SChritt für die Meschheit, ein gewaltiger Totalschaden für Kevin
# 
#   Kevin, ein Flüchtling vor dem FBI, entdeckt im Wald ein altes, funktionstüchtiges 
#   Raumschiff. Da er kein Bargeld hatte tauscht er im Dorf seine letzten Robux-Karten gegen 
#   Batterien ein, um das Schiff zu starten und die Erde zu verlassen.

#   GAMEPLAY:
#   Erreiche einen fernen Planeten für einen Neuanfang.
#   Kevin muss Trümmerfeldern (Asteroiden) ausweichen oder diese mit 
#   einem nachgerüsteten Waffen-Modul zerstören.
#   Sammle strahlende Aura-Punkte im All, um genug Energie/Status für 
#   eine sichere Landung auf dem Zielplaneten zu schaffen
#
#   rot = Kevin
#   pink = Aura
#   weiß = Asteroiden


from sense_hat import SenseHat, ACTION_RELEASED
import time
import random

global levelframe
levelframe = 200

sense = SenseHat()
sense.low_light = True

class GameObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y 
        self.should_be_deleted = False

    def draw(self):
        return

    def update(self):
        return
    
    def is_colliding(self, gameObject):
        return
      
class Player(GameObject):
    def __init__(self, x, y):
        # super() --> base (C#)
        super().__init__(x, y)
        self.alive = True
        self.victory = False


    def draw(self):
        sense.set_pixel(player.x, player.y, playercolour)
        if player.y + 1 <= 7:
            sense.set_pixel(player.x, player.y +1, playercolour)

    def update(self):
        pass

    def is_colliding(self, gameObject):
        if self.y == gameObject.y and self.x == gameObject.x:
            return True
        else: 
            
            return False

class Bullet(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)

    def draw(self):
         if 0 <= self.y <= 7:
                sense.set_pixel(self.x, self.y, bullet)

    def update(self):
        if framecounter % 10 == 0:
            if self.y == 0:
                self.should_be_deleted = True 
                return

            if self.y >= 0:
                self.y -= 1

    def is_colliding(self, gameObject):
        if self.y == gameObject.y and self.x == gameObject.x:
            return True
        return False

class Aura(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)

    def draw(self):
         if 0 <= self.y <= 7:
                sense.set_pixel(self.x, self.y, auracolour)
    
    def update(self):    
        if framecounter % 50 == 0:
            if self.y == 7:
                self.should_be_deleted = True 
                return
            else:
                self.y += 1

    def is_colliding(self, gameObject):
        global levelframe
        global aura_counter

        if self.y == gameObject.y and self.x == gameObject.x:
            aura_counter += 1
            self.should_be_deleted = True

            if aura_counter == 5:
                levelframe = 100
            elif aura_counter == 10:
                levelframe = 50

            if aura_counter == 15:
                player.alive = False
                player.victory = True
        return 

class Astroid(GameObject):
    def __init__(self, shape):
        self.collision_counter = 0            
        self.shape = shape
        if (shape == 1):
            ax = random.randint(0,7)
        else:
            ax = random.randint(1, 7)
        super().__init__(ax, 0)

    def draw(self):
        if(self.shape == 1):
            sense.set_pixel(self.x, self.y, enemy)
        elif self.shape == 2:
            sense.set_pixel(self.x, self.y, enemy)
            sense.set_pixel(self.x-1, self.y, enemy)
        elif self.shape == 3:
            sense.set_pixel(self.x, self.y, enemy)
            sense.set_pixel(self.x-1, self.y, enemy)
            sense.set_pixel(self.x-1, self.y+1, enemy)

    def update(self):
        if framecounter % 50 == 0:
            if self.shape <= 2:
                if self.y == 7:
                    self.should_be_deleted = True 
                    return
            else:
                if self.y == 6:
                    self.should_be_deleted = True 
                    return
                
            if self.y <= 6:
                self.y += 1

    def is_colliding(self, gameObject):
            if self.shape == 1:
                if self.y == gameObject.y and self.x == gameObject.x:
                    self.should_be_deleted = True
                    gameObject.should_be_deleted = True
                    
            elif self.shape == 2:
                if self.y == gameObject.y  and (self.x == gameObject.x or self.x-1 == gameObject.x):
                    self.collision_counter += 1
                    if self.collision_counter == 2:
                        self.should_be_deleted = True
                    gameObject.should_be_deleted = True
                        
            elif self.shape == 3:
                if self.y == gameObject.y  and (self.x == gameObject.x or self.x-1 == gameObject.x) or (self.y+1 == gameObject.y and self.x == gameObject.x):
                    self.collision_counter += 1
                    if self.collision_counter == 3:
                        self.should_be_deleted = True
                    gameObject.should_be_deleted = True
            return 
        
# Startposition player
x = 4
y = 6
bullets = []
astroids = []
aura = []
player = Player(x, y)


#       ▄████████    ▄████████    ▄████████ ▀█████████▄     ▄████████ ███▄▄▄▄   
#      ███    ███   ███    ███   ███    ███   ███    ███   ███    ███ ███▀▀▀██▄ 
#      ███    █▀    ███    ███   ███    ███   ███    ███   ███    █▀  ███   ███ 
#     ▄███▄▄▄       ███    ███  ▄███▄▄▄▄██▀  ▄███▄▄▄██▀   ▄███▄▄▄     ███   ███ 
#    ▀▀███▀▀▀     ▀███████████ ▀▀███▀▀▀▀▀   ▀▀███▀▀▀██▄  ▀▀███▀▀▀     ███   ███ 
#      ███          ███    ███ ▀███████████   ███    ██▄   ███    █▄  ███   ███ 
#      ███          ███    ███   ███    ███   ███    ███   ███    ███ ███   ███ 
#      ███          ███    █▀    ███    ███ ▄█████████▀    ██████████  ▀█   █▀  
#                                ███    ███                                     

green = (0, 255, 0)
enemy = (236, 204, 85)
bullet = (0, 248, 255)
playercolour = (255, 0, 0)
white = (255,255,255)
space = (0,0,69)
black = (0, 0, 69)
auracolour = (201, 0, 255)

#       ▄████████ ███    █▄  ███▄▄▄▄    ▄████████     ███      ▄█   ▄██████▄  ███▄▄▄▄      ▄████████ 
#      ███    ███ ███    ███ ███▀▀▀██▄ ███    ███ ▀█████████▄ ███  ███    ███ ███▀▀▀██▄   ███    ███ 
#      ███    █▀  ███    ███ ███   ███ ███    █▀     ▀███▀▀██ ███▌ ███    ███ ███   ███   ███    █▀  
#     ▄███▄▄▄     ███    ███ ███   ███ ███            ███   ▀ ███▌ ███    ███ ███   ███   ███        
#    ▀▀███▀▀▀     ███    ███ ███   ███ ███            ███     ███▌ ███    ███ ███   ███ ▀███████████ 
#      ███        ███    ███ ███   ███ ███    █▄      ███     ███  ███    ███ ███   ███          ███ 
#      ███        ███    ███ ███   ███ ███    ███     ███     ███  ███    ███ ███   ███    ▄█    ███ 
#      ███        ████████▀   ▀█   █▀  ████████▀     ▄████▀   █▀    ▀██████▀   ▀█   █▀   ▄████████▀  
#                                                                                                    

def clamp(value, min_value=0, max_value=7):
    return min(max_value, max(min_value, value))

def move_left(event):
    if event.action != ACTION_RELEASED:
        player.x = clamp(player.x - 1)

def move_right(event):
    if event.action != ACTION_RELEASED:
        player.x = clamp(player.x + 1)

def shoot_bullet(event):

    # Die Koordinaten von Kevin
    # 'global bullets' ist hier optional für .append(), 
    # aber schadet nicht für die Klarheit.
    
    if event.action != ACTION_RELEASED and len(bullets) <= 5:
        new_bullet = Bullet(player.x, 5)  # startet einen Pixel vor Kevin
        bullets.append(new_bullet)

#def spawnAstroid():
#    if framecounter % 500 == 0:
#            astroids.append(Astroid(random.randint(0, 2)))

#---------------------------------------------------------------------------------------------------------------

# Joystick-Events zuweisen
sense.stick.direction_left = move_left
sense.stick.direction_right = move_right
sense.stick.direction_up = shoot_bullet

#---------------------------------------------------------------------------------------------------------------
sense.show_message("3 2 1", text_colour = green)
global level
global aura_counter
global framecounter    
framecounter = 0
aura_counter = 0

#       ▄██████▄     ▄████████   ▄▄▄▄███▄▄▄▄      ▄████████  ▄█        ▄██████▄   ▄██████▄     ▄███████▄ 
#      ███    ███   ███    ███ ▄██▀▀▀███▀▀▀██▄   ███    ███ ███       ███    ███ ███    ███   ███    ███ 
#      ███    █▀    ███    ███ ███   ███   ███   ███    █▀  ███       ███    ███ ███    ███   ███    ███ 
#     ▄███          ███    ███ ███   ███   ███  ▄███▄▄▄     ███       ███    ███ ███    ███   ███    ███ 
#    ▀▀███ ████▄  ▀███████████ ███   ███   ███ ▀▀███▀▀▀     ███       ███    ███ ███    ███ ▀█████████▀  
#      ███    ███   ███    ███ ███   ███   ███   ███    █▄  ███       ███    ███ ███    ███   ███        
#      ███    ███   ███    ███ ███   ███   ███   ███    ███ ███▌    ▄ ███    ███ ███    ███   ███        
#      ████████▀    ███    █▀   ▀█   ███   █▀    ██████████ █████▄▄██  ▀██████▀   ▀██████▀   ▄████▀      
#              
                                                                                
while player.alive:

    framecounter += 1
    framecounter %= 1000    # wenn bulletframcounter größer als 200 ist wird es auf 0 zurückgesetzt 
                            # (dividiere durch 200 --> rest wird gespeichert)

    #gamelogic

#                     _       _       
#                    | |     | |      
#     _   _ _ __   __| | __ _| |_ ___ 
#    | | | | '_ \ / _` |/ _` | __/ _ \
#    | |_| | |_) | (_| | (_| | ||  __/
#     \__,_| .__/ \__,_|\__,_|\__\___|
#          | |                        
#          |_|               

    if framecounter % levelframe == True:
        astroids.append(Astroid(random.randint(1,3)))
        
    if framecounter % 200 == True:
        aura.append(Aura(random.randint(0,7), 0))

       # aura.append(Aura(1,0))
    for b in bullets:
        b.update()

        for a in astroids:
            a.is_colliding(b)

        if b.should_be_deleted == True:
            bullets.remove(b)

    for a in aura:
        # print("Aura Update",framecounter)
        a.update()
        a.is_colliding(player)

        if a.should_be_deleted == True:
            aura.remove(a)

    for a in astroids:
        a.update()

        if a.should_be_deleted == True:
            astroids.remove(a)

        if player.is_colliding(a) == True:
            player.alive = False
            
    sense.clear(space)

#         _                    
#        | |                   
#      __| |_ __ __ ___      __
#     / _` | '__/ _` \ \ /\ / /
#    | (_| | | | (_| |\ V  V / 
#     \__,_|_|  \__,_| \_/\_/  
#                              
#                              

    for a in aura:
        a.draw()

    for b in bullets:
        #zeichnet alle Objekte die im GameObject  gespeichert wird
        b.draw()

    for astroid in astroids:
        astroid.draw()
    
    player.draw()
        
    time.sleep(0.02)

red = (255, 0, 0)
if player.victory == True:
    

    yellow = (255, 241, 78)


        
    def Landing1():
        G= green
        K = playercolour
        O = black
        logo = [
        O, G, G, G, G, G, G, O, 
        O, G, G, G, G, G, G, O,
        O, O, G, G, G, G, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, K, O, O, O,
        ]
        return logo
        
    def Landing2():

        G= green
        K = playercolour
        O = black
        logo = [
        G, G, G, G, G, G, G, G, 
        O, G, G, G, G, G, G, O,
        O, O, G, G, G, G, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, K, O, O, O,
        O, O, O, O, K, O, O, O,
        ]
        return logo

    def Landing3():

        G= green
        K = playercolour
        O = black
        logo = [
        G, G, G, G, G, G, G, G, 
        G, G, G, G, G, G, G, G,
        O, G, G, G, G, G, G, O,
        O, O, G, G, G, G, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, K, O, O, O,
        O, O, O, O, K, O, O, O,
        ]
        return logo
        
        
    def Landing4():

        G= green
        K = playercolour
        O = black
        logo = [
        G, G, G, G, G, G, G, G, 
        G, G, G, G, G, G, G, G,
        O, G, G, G, G, G, G, O,
        O, O, G, G, G, G, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, K, O, O, O,
        O, O, O, O, K, O, O, O,
        O, O, O, O, O, O, O, O,
        ]
        return logo

        
    def Landing5():

        G= green
        K = playercolour
        O = black
        logo = [
        G, G, G, G, G, G, G, G, 
        G, G, G, G, G, G, G, G,
        O, G, G, G, G, G, G, O,
        O, O, G, G, G, G, O, O,
        O, O, O, O, K, O, O, O,
        O, O, O, O, K, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        ]
        return logo
        
        
            
    def Landing6():

        G= green
        K = playercolour
        O = black
        logo = [
        G, G, G, G, G, G, G, G, 
        G, G, G, G, G, G, G, G,
        O, G, G, G, G, G, G, O,
        O, O, G, G, K, G, O, O,
        O, O, O, O, K, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        ]
        return logo
        
        
            
    def Landing7():

        G= green
        K = playercolour
        O = black
        logo = [
        G, G, G, G, G, G, G, G, 
        G, G, G, G, G, G, G, G,
        O, G, G, G, K, G, G, O,
        O, O, G, G, K, G, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        ]
        return logo
        
        
    def Landing8():

        G= green
        K = playercolour
        O = black
        logo = [
        G, G, G, G, G, G, G, G, 
        G, G, G, G, K, G, G, G,
        O, G, G, G, K, G, G, O,
        O, O, G, G, G, G, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        ]
        return logo
        
        
    def Landing9():

        G= green
        K = playercolour
        O = black
        logo = [
        G, G, G, G, K, G, G, G, 
        G, G, G, G, K, G, G, G,
        O, G, G, G, G, G, G, O,
        O, O, G, G, G, G, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        ]
        return logo

    def Landing10():

        G= green
        K = playercolour
        O = black
        logo = [
        G, G, G, G, K, G, G, G, 
        G, G, G, G, K, G, G, G,
        O, G, G, G, G, G, G, O,
        O, O, G, G, G, G, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        ]
        return logo


    def Landing11():

        G= green
        K = playercolour
        O = black
        logo = [
        G, G, G, G, K, G, G, G, 
        G, G, G, G, K, G, G, G,
        G, G, G, G, G, G, G, G,
        O, G, G, G, G, G, G, O,
        O, O, G, G, G, G, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        ]
        return logo

    def Landing11():

        G= green
        K = playercolour
        O = black
        logo = [
        G, G, G, G, K, G, G, G, 
        G, G, G, G, K, G, G, G,
        G, G, G, G, G, G, G, G,
        O, G, G, G, G, G, G, O,
        O, O, G, G, G, G, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        ]
        return logo

    def trophy():

        Y = yellow
        O = black
        logo = [
        O, O, O, O, O, O, O, O, 
        O, Y, Y, Y, Y, Y, Y, O,
        O, Y, Y, Y, Y, Y, Y, O, 
        O, O, Y, Y, Y, Y, O, O,
        O, O, O, Y, Y, O, O, O,
        O, O, O, Y, Y, O, O, O,
        O, O, Y, Y, Y, Y, O, O,
        O, O, Y, Y, Y, Y, O, O,
        ]
        return logo

    images = [Landing1,Landing2,Landing3,Landing4,Landing5,Landing6,Landing7,Landing8,Landing9,Landing10,Landing11]
    count = 0
    countT = 0

    while True: 
        sense.set_pixels(images[count % len(images)]())
        time.sleep(.75)
        count += 1
else:
    sense.show_message("GAME OVER", text_colour = red)
    