# 開始介面 + 連線
# 一般 健身環 mode
import pygame as pg
import random
from math import *
from pygame import event
from pygame.locals import K_ESCAPE, KEYDOWN, MOUSEBUTTONDOWN, QUIT
from pygame.math import *
from os import getcwd


WINDOW_SIZE = (720, 480)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WEAPON = getcwd().replace('\\', '/') + '/stick2.png'     # (120 * 150)
ENEMY_IMG = [getcwd().replace('\\', '/') + '/book1.png']
Start_loc = [[WINDOW_SIZE[0]*i/9 , 10] for i in range(9) ]
pivot = (360 , 450)                                      # 軸心
offset = Vector2((0, 75))                                # 偏移 (武器長度的一半)

class Player:
    def __init__(self):
        self.score = 0
        self.hp = 0
    

class Enemy(pg.sprite.Sprite):
    def __init__(self, scr):
        self.appearance = []
        self.x, self.y = scr
        self.speed = 10
        
        for each in ENEMY_IMG:
            self.appearance.append(pg.image.load(each).convert_alpha())

    def attack(self):
        # if not 碰到 棍子
        theta = atan((pivot[1]-self.y)/(pivot[0]-self.x))
        self.x += cos(theta) * self.speed if theta> 0 else cos(theta) * self.speed * -1
        self.y += sin(theta) * self.speed if theta> 0 else sin(theta) * self.speed * -1
        print(self.x, self.y)
        screen.blit(self.appearance[0], (self.x, self.y))


class Interface:
    def __init__(self):
        self.mode = 0
    def pause(self):
        pass 

def start(interface):
    # 建立畫布bg
    bg1 = pg.Surface(screen.get_size())
    bg1 = bg1.convert()
    bg1.fill((255,255,255))
    global run
    # 遊戲名稱
    #font = pg.font.Font(getcwd().replace('\\', '/') + "/msjhbd.ttc", 40)
    #game_name = font.render("你贏了", True, (0,0,255), (224,224,80))
    #screen.blit(game_name, (250,630))
    #繪製幾何圖形
    BTN_mode1 = pg.Rect(100, 250, 500, 60)                 # 健身環MODE
    BTN_mode2 = pg.Rect(100, 350, 500, 60)                # 一般MODE
    pg.draw.rect(bg1, BLUE, BTN_mode1, 4)
    pg.draw.rect(bg1, BLUE, BTN_mode2, 4)

    screen.blit(bg1, (0,0))
    pg.display.update()
    for event in pg.event.get():
        if event.type == KEYDOWN:           # 觸發關閉視窗
            if event.key == K_ESCAPE:
                run = False
        elif event.type == QUIT:
            run = False
        elif event.type == MOUSEBUTTONDOWN:  
            if event.button == 1 and BTN_mode1.collidepoint(event.pos):
                interface.mode = 1
                print(1)
                return
            elif event.button == 1 and BTN_mode2.collidepoint(event.pos):
                interface.mode = 2
                print(2)
                return

def game1():
    # 遊戲bg
    global run
    bg2 = pg.Surface(screen.get_size())
    bg2 = bg2.convert()
    bg2.fill(WHITE)

    clock = pg.time.Clock()
    # 武器
    
    weapon = pg.image.load(WEAPON).convert_alpha()
    #weapon_rect = weapon.get_rect()
    #weapon_rect = weapon_rect.move((WINDOW_SIZE[0]-weapon_rect.width)/2, 300)


    #pg.draw.rect(bg2, BLUE, weapon, 0)
    screen.blit(bg2, (0,0))
    pg.display.update()


    while run:
        for event in pg.event.get():
            if event.type == KEYDOWN:           # 觸發關閉視窗
                if event.key == K_ESCAPE:
                    run = False
            elif event.type == QUIT:
                run = False
            
            rotation_direction = pg.mouse.get_rel()[0]

            #print(rotation_direction)
            rotated_weapon = pg.transform.rotate(weapon, rotation_direction/-5)
            rotated_offset = offset.rotate(rotation_direction/5)

            #print(rotated_weapon)
            screen.fill((255, 255, 255))
            weapon_rect = rotated_weapon.get_bounding_rect()
            weapon_rect.center = pivot - rotated_offset
            
            screen.blit(rotated_weapon, weapon_rect)
            pg.draw.circle(screen, (30, 250, 70), pivot, 3)
            pg.draw.rect(screen, (30, 250, 70), weapon_rect, 1)  # The rect.

            # draw doors
            for i in range(9):
                door = pg.Rect(WINDOW_SIZE[0]*i/9, 0, WINDOW_SIZE[0]/9, 100)
                pg.draw.rect(screen, BLUE, door, 3)
            
                enemies[i].attack()

            # 正式渲染
            pg.display.update()
            clock.tick(30)
            #elif event.type == MOUSEBUTTONDOWN:
        

if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('test')                 # 視窗標題
    screen = pg.display.set_mode(WINDOW_SIZE, pg.RESIZABLE, 32)

    interface = Interface()
    p1 = Player()
    enemies = [Enemy(Start_loc[i]) for i in range(9)]
    
    """
    pg.font.init()
    pg.joystick.init()
    pg.mixer.init()    
    """
    run = True
    while run:
        if interface.mode == 0:
            start(interface)
        if interface.mode == 1 or interface.mode == 2:
            game1()

    quit()   
