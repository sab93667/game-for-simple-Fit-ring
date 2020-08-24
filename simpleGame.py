# 開始介面 + 連線
# 一般 健身環 mode
import pygame as pg
import random
from math import *
from pygame import event
from pygame.locals import K_ESCAPE, KEYDOWN, MOUSEBUTTONDOWN, QUIT
from pygame.math import *
from os import getcwd

pg.font.init()
WINDOW_SIZE = (720, 480)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WEAPON = getcwd().replace('\\', '/') + '/stick3.png'     # (120 * 150)
ENEMY_IMG = [getcwd().replace('\\', '/') + '/book2.png', getcwd().replace('\\', '/') + '/book3.png', getcwd().replace('\\', '/') + '/book4.png',\
             getcwd().replace('\\', '/') + '/book5.png', getcwd().replace('\\', '/') + '/book6.png', getcwd().replace('\\', '/') + '/book7.png',\
             getcwd().replace('\\', '/') + '/book8.png', getcwd().replace('\\', '/') + '/book9.png', getcwd().replace('\\', '/') + '/book10.png']
HEART = getcwd().replace('\\', '/') + '/heart1.png'
score_font = pg.font.Font(getcwd().replace('\\', '/') + "/msjhbd.ttc", 20)
title_font = pg.font.Font(getcwd().replace('\\', '/') + "/msjhbd.ttc", 40)
Start_loc = [[WINDOW_SIZE[0]*i/9 , 10] for i in range(9) ]
pivot = (360 , 450)                                      # 軸心
offset = Vector2((0, 75))                                # 偏移 (武器長度的一半)

class Weapon(pg.sprite.Sprite):    
    def __init__(self, img):
        super().__init__()
        self.image = pg.image.load(img).convert_alpha()
        self.org_image = pg.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.total_angle = 0

    def rotation(self, dir):
        self.total_angle += dir / -3
        rotated_weapon = pg.transform.rotate(self.org_image, self.total_angle)
        rotated_offset = offset.rotate(-1*self.total_angle)
        self.rect = rotated_weapon.get_bounding_rect()
        self.rect.center = pivot - rotated_offset
        self.image = rotated_weapon
        #print(self.rect)
        #return rotated_weapon, self.rect


class Enemy(pg.sprite.Sprite):
    def __init__(self, pos, img):
        super().__init__()
        self.image = pg.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.speed = int(WINDOW_SIZE[1] / 48 )
        self.valid = False 
        #self.x, self.y = pos
        #self.rect.x, self.rect.y = pos
        #for each in ENEMY_IMG:
            #self.appearance.append(pg.image.load(each).convert_alpha())

    def appear(self, i):
        self.rect.topleft = Start_loc[i]
        self.valid = True

    def attack(self):
        #theta = atan((pivot[1]-self.y)/(pivot[0]-self.x))
        #self.x += cos(theta) * self.speed if theta> 0 else cos(theta) * self.speed * -1
        #self.y += sin(theta) * self.speed if theta> 0 else sin(theta) * self.speed * -1
        theta = atan((pivot[1]-self.rect.y)/(pivot[0]-self.rect.x)) if (pivot[0]-self.rect.x) !=0 else 90
        #self.rect = self.image.get_rect()
        self.rect.x += cos(theta) * self.speed if theta> 0 else cos(theta) * self.speed * -1
        self.rect.y += sin(theta) * self.speed if theta> 0 else sin(theta) * self.speed * -1
        #print(self.rect)
    def back(self):
        theta = atan((pivot[1]-self.rect.y)/(pivot[0]-self.rect.x)) if (pivot[0]-self.rect.x) !=0 else 90
        self.rect.x -= cos(theta) * self.speed*5 if theta> 0 else cos(theta) * self.speed * -5
        self.rect.y -= sin(theta) * self.speed*5 if theta> 0 else sin(theta) * self.speed * -5


class Interface(pg.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.mode = 0
        self.score = 0
        self.hp = 3
        self.image = pg.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
    
    def show(self):
        for i in range(self.hp):
            self.rect.x = WINDOW_SIZE[0]*(0.8 + 0.05*i)
            self.rect.y = WINDOW_SIZE[1]*0.9
            screen.blit(self.image, self.rect)
        text_surface = score_font.render('Score : '+ str(self.score), True, (0, 0, 0))
        screen.blit(text_surface, (WINDOW_SIZE[0]*0.05, WINDOW_SIZE[1]*0.9))    

    def pause(self):
        pass 

def start(interface):
    # 建立畫布bg
    global screen, WINDOW_SIZE, run
    bg1 = pg.Surface(screen.get_size())
    bg1 = bg1.convert()
    bg1.fill(WHITE)

    screen.blit(bg1, (0,0))
    pg.display.update()
    while run:
        bg1 = pg.Surface(screen.get_size())
        bg1 = bg1.convert()
        bg1.fill(WHITE)
        BTN_mode1 = pg.Rect(WINDOW_SIZE[0]/5, WINDOW_SIZE[1]/2, WINDOW_SIZE[0]*3/5, WINDOW_SIZE[1]/8)                 # 健身環MODE
        BTN_mode2 = pg.Rect(WINDOW_SIZE[0]/5, WINDOW_SIZE[1]/1.4, WINDOW_SIZE[0]*3/5, WINDOW_SIZE[1]/8)                # 一般MODE
        pg.draw.rect(bg1, BLUE, BTN_mode1, 4)
        pg.draw.rect(bg1, BLUE, BTN_mode2, 4)
        screen.blit(bg1, (0,0))
        game_name = title_font.render('健身環大冒險(暫)', True, (0, 0, 0))  # 大小需要調整
        text_mode1 = title_font.render('健身環模式', True, (0, 0, 0))
        text_mode2 = title_font.render('一般模式', True, (0, 0, 0))
        screen.blit(game_name, (WINDOW_SIZE[0]/4, WINDOW_SIZE[1]/4))
        screen.blit(text_mode1, (WINDOW_SIZE[0]/2.5, WINDOW_SIZE[1]/2))
        screen.blit(text_mode2, (WINDOW_SIZE[0]/2.5, WINDOW_SIZE[1]/1.4))
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
            elif event.type == pg.VIDEORESIZE:
                WINDOW_SIZE = event.size
                screen = pg.display.set_mode(WINDOW_SIZE, pg.RESIZABLE, 32)

        


def game1(interface):  # 已知問題  開始縮放有問題 速度隨分數增加
    # 遊戲bg
    global run, screen, WINDOW_SIZE, pivot, offset, Start_loc, all_sprites, block_list
    bg2 = pg.Surface(screen.get_size())
    bg2 = bg2.convert()
    bg2.fill(WHITE)

    clock = pg.time.Clock()
    # 武器
    w1 = Weapon(WEAPON)
    interface.hp = 3
    interface.score = 0
    # 敵方
    enemies = [Enemy(Start_loc[i], ENEMY_IMG[i]) for i in range(9)]
    beaten = []
    screen.blit(bg2, (0,0))
    pg.display.update()
    # 清空物件
    all_sprites.empty()
    block_list.empty()
    all_sprites.add(w1)
    #all_sprites.add(interface)
    #all_sprites.add(each for each in enemies)
    #block_list.add(each for each in enemies)
    #print(all_sprites, block_list)

    while run:
        for event in pg.event.get():
            if event.type == KEYDOWN:           # 觸發關閉視窗
                if event.key == K_ESCAPE:
                    run = False
            elif event.type == QUIT:
                run = False
            elif event.type == pg.VIDEORESIZE:
                WINDOW_SIZE = event.size
                screen = pg.display.set_mode(WINDOW_SIZE, pg.RESIZABLE, 32)
        
        pivot = (int(WINDOW_SIZE[0]/2) , int(WINDOW_SIZE[1]*15/16))                                      # 軸心
        offset = Vector2((0, 75))                                # 偏移 (武器長度的一半)
        Start_loc = [[WINDOW_SIZE[0]*i/9 , WINDOW_SIZE[0]/48] for i in range(9) ]

        
        rotation_direction = pg.mouse.get_rel()[0]
        #rotated, weapon_rect  = 
        w1.rotation(rotation_direction)
        w1.org_image = pg.transform.scale(w1.org_image, (int(WINDOW_SIZE[0]/36), int(WINDOW_SIZE[1]/2.5)))

        #print(rotation_direction)
        #print(rotated_weapon)
        screen.fill(WHITE)
        #screen.blit(rotated, weapon_rect)
        

        # draw doors
        for i in range(9):
            door = pg.Rect(WINDOW_SIZE[0]*i/9, 0, WINDOW_SIZE[0]/9, WINDOW_SIZE[0]/9*1.2)
            pg.draw.rect(screen, BLUE, door, 3)
            #if enemies[i].valid:
            #    enemies[i].attack()

        # random time and location
        num = random.randint(0, 8)
        if not enemies[num].valid and random.random()<0.03:
            enemies[num].image = pg.transform.scale(enemies[num].image, (int(WINDOW_SIZE[0]/10), int(WINDOW_SIZE[0]/10)))
            enemies[num].rect = enemies[num].image.get_rect()
            enemies[num].appear(num)
            block_list.add(enemies[num])
            all_sprites.add(enemies[num])
            #enemies[num].attack()
        for each in block_list:
            each.attack()
            # 沒打到
            if each.rect.y > WINDOW_SIZE[1]*9/12 :
                #print(111)
                all_sprites.remove(each)
                block_list.remove(each)
                interface.hp -= 1
                each.valid = False
        # 有打到
        beaten.extend(pg.sprite.spritecollide(w1, block_list, False, pg.sprite.collide_mask))
        #print(beaten)
        for each in beaten:
            if each.valid == True:                
                interface.score += 100
            each.valid = False
            each.back()
            
            if each.rect.y < -20 :
                #print(123)
                all_sprites.remove(each)
                block_list.remove(each)
                beaten.remove(each)

        all_sprites.draw(screen)                             # 全部畫出來
        interface.show()

        pg.draw.circle(screen, (30, 250, 70), pivot, 3)
        pg.draw.rect(screen, (30, 250, 70), w1.rect, 1)  # The rect.
        for i in range(9):
            pg.draw.rect(screen, (30, 250, 70), enemies[i].rect, 1)  # The rect.
        # 正式渲染
        pg.display.update()
        clock.tick(30)

        if interface.hp == 0:
            interface.mode = 0
            return
        #elif event.type == MOUSEBUTTONDOWN:
        

if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('test')                 # 視窗標題
    screen = pg.display.set_mode(WINDOW_SIZE, pg.RESIZABLE, 32)

    block_list = pg.sprite.Group()                 # 碰撞檢測
    all_sprites = pg.sprite.Group()                # 所有角色

    interface = Interface(HEART)
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
            game1(interface)

    quit()   
