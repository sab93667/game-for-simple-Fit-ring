# 開始介面 + 連線
# 一般 健身環 mode
import pygame as pg
import simpleServer as ss
import random, socket, time, pymouse, pykeyboard, os, sys, webbrowser
from math import *
from pygame import event
from pygame.locals import K_ESCAPE, KEYDOWN, MOUSEBUTTONDOWN, QUIT
from pygame.math import *
from os import getcwd
from pymouse import *
from pykeyboard import PyKeyboard
from pynput import mouse

pg.font.init()
WINDOW_SIZE = (720, 480)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
preview_color = (124, 252, 0)
HIT = getcwd().replace('\\', '/') + '/hit.wav' 
BG = getcwd().replace('\\', '/') + '/bg.png' 
BG2 = getcwd().replace('\\', '/') + '/bg2.png' 
WEAPON = getcwd().replace('\\', '/') + '/stick3.png'     # (120 * 150)
ENEMY_IMG = [getcwd().replace('\\', '/') + '/book2.png', getcwd().replace('\\', '/') + '/book3.png', getcwd().replace('\\', '/') + '/book4.png',\
             getcwd().replace('\\', '/') + '/book5.png', getcwd().replace('\\', '/') + '/book6.png', getcwd().replace('\\', '/') + '/book7.png',\
             getcwd().replace('\\', '/') + '/book8.png', getcwd().replace('\\', '/') + '/book9.png', getcwd().replace('\\', '/') + '/book10.png']
HEART = getcwd().replace('\\', '/') + '/heart1.png'
score_font = pg.font.SysFont("Broadway", 16)#.font.Font(getcwd().replace('\\', '/') + "/msjhbd.ttc", int(WINDOW_SIZE[0]/36))
title_font = pg.font.Font(getcwd().replace('\\', '/') + "/msjhbd.ttc", int(WINDOW_SIZE[0]/18))
Start_loc = [[WINDOW_SIZE[0]*i/9 , 10] for i in range(9) ]
pivot = (360 , 450)                                      # 軸心
offset = Vector2((0, int(WINDOW_SIZE[0]/8)))                                # 偏移 (武器長度的一半)
opened = False
btn_preview = 1
client = None

Host = '192.168.137.1'
Port = 5438

class Weapon(pg.sprite.Sprite):    
    def __init__(self, img):
        super().__init__()
        self.image = pg.image.load(img).convert_alpha()
        self.org_image = pg.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (WINDOW_SIZE[0]/2, WINDOW_SIZE[1]*7/10)
        self.total_angle = 0
        self.last_angle = 0
        self.offset = 0
        self.ang_v_offset = 0
        self.TR = False
        self.TL = False

    def rotation(self, direc):
        self.total_angle += direc / -3
        if self.total_angle >= 90:
            self.total_angle = 90
        if self.total_angle <= -90:
            self.total_angle = -90
        rotated_weapon = pg.transform.rotate(self.org_image, self.total_angle)
        rotated_offset = offset.rotate(-1*self.total_angle)
        self.rect = rotated_weapon.get_bounding_rect()
        self.rect.center = pivot - rotated_offset
        self.image = rotated_weapon
        #print(self.rect)
        #return rotated_weapon, self.rect

    def rotation2(self, direc):
        self.total_angle = direc
        rotated_weapon = pg.transform.rotate(self.org_image, self.total_angle)
        rotated_offset = offset.rotate(-1*self.total_angle)
        self.rect = rotated_weapon.get_bounding_rect()
        self.rect.center = pivot - rotated_offset
        self.image = rotated_weapon

    def turn_r(self):
        self.total_angle -= (self.total_angle+90)/4.5
        #print(self.total_angle)
        if self.total_angle <= -89:
            self.total_angle = -90
            self.TR = False
        rotated_weapon = pg.transform.rotate(self.org_image, self.total_angle)
        rotated_offset = offset.rotate(-1*self.total_angle)
        self.rect = rotated_weapon.get_bounding_rect()
        self.rect.center = pivot - rotated_offset
        self.image = rotated_weapon       
            
    def turn_l(self):
        #print(333, self.total_angle)
        self.total_angle += (90-self.total_angle)/4.5
        if self.total_angle >= 89:
            self.total_angle = 90
            self.TL = False
        rotated_weapon = pg.transform.rotate(self.org_image, self.total_angle)
        rotated_offset = offset.rotate(-1*self.total_angle)
        self.rect = rotated_weapon.get_bounding_rect()
        self.rect.center = pivot - rotated_offset
        self.image = rotated_weapon
        
    def correction(self, interface):
        if not interface.cli:
            interface.cli = ss.connect(Host, Port, 5)
        #interface.cli.send(b'received!')
        self.offset = 0
        self.ang_v_offset = 0
        test = 10
        while test > 0:
            ring = ss.get(interface.cli)
            if ring:
                ring  = ring.replace("\n", ",").strip().split(",")[-5:-1]
                x_ang = float(ring[0])
                squeeze = float(ring[1])
                ang_v = float(ring[2])
                angle = float(ring[3])
                print(test, x_ang, squeeze, ang_v, angle)
                self.offset += angle
                self.ang_v_offset += ang_v
                test -= 1
        self.offset /= 10
        self.ang_v_offset /=10

    def zoom(self):
        rotated_weapon = pg.transform.rotate(self.org_image, self.total_angle)
        rotated_offset = offset.rotate(-1*self.total_angle)
        self.rect = rotated_weapon.get_bounding_rect()
        self.rect.center = pivot - rotated_offset
        self.image = rotated_weapon

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
        self.rect.x -= cos(theta) * self.speed*5 if theta> 0 else cos(theta) * self.speed * -7
        self.rect.y -= sin(theta) * self.speed*5 if theta> 0 else sin(theta) * self.speed * -7

class Interface(pg.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.mode = 0
        self.score = 0
        self.hp = 3
        self.cli = None
        self.image = pg.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
    
    def show(self):
        for i in range(self.hp):
            self.rect.x = WINDOW_SIZE[0]*(0.8 + 0.05*i)
            self.rect.y = WINDOW_SIZE[1]*0.1
            screen.blit(self.image, self.rect)
        text_surface = score_font.render('Score : '+ str(self.score), True, (0, 0, 0))
        screen.blit(text_surface, (WINDOW_SIZE[0]*0.05, WINDOW_SIZE[1]*0.1))    

    def pause(self):
        pass 

def start(interface, client = None):
    # 建立畫布bg
    global screen, WINDOW_SIZE, run, score_font, title_font, opened, btn_preview
    bg1 = pg.image.load(BG).convert_alpha()
    
    #bg1 = pg.Surface(screen.get_size())
    bg1 = pg.transform.scale(bg1, WINDOW_SIZE)
    #bg1 = bg1.convert()
    #bg1.fill(WHITE)
    #bg1.set_alpha(5)
    screen.blit(bg1, (0,0))
    pg.display.update()
    
    while run:
        #bg1 = pg.Surface(screen.get_size())
        #bg1 = bg1.convert()
        #bg1.fill(WHITE)
        #bg1 = pg.transform.scale(bg1, WINDOW_SIZE)
        #screen.blit(bg1, (0,0))
        BTN_mode1 = pg.Rect(WINDOW_SIZE[0]/5, WINDOW_SIZE[1]/2.5, WINDOW_SIZE[0]*3/5, WINDOW_SIZE[1]/8)                 # 健身環MODE
        BTN_mode2 = pg.Rect(WINDOW_SIZE[0]/5, WINDOW_SIZE[1]/1.8, WINDOW_SIZE[0]*3/5, WINDOW_SIZE[1]/8)                # 一般MODE
        BTN_mode3 = pg.Rect(WINDOW_SIZE[0]/5, WINDOW_SIZE[1]/1.4, WINDOW_SIZE[0]*3/5, WINDOW_SIZE[1]/8)                # 恐龍 MODE
        pg.draw.rect(bg1, BLUE, BTN_mode1, 4)
        pg.draw.rect(bg1, BLUE, BTN_mode2, 4)
        pg.draw.rect(bg1, BLUE, BTN_mode3, 4)
        screen.blit(bg1, (0,0))
        game_name = title_font.render('健身環大冒險(暫)', True, (0, 0, 0))  # 大小需要調整
        text_mode1 = title_font.render('健身環模式', True, (0, 0, 0))
        text_mode2 = title_font.render('一般模式', True, (0, 0, 0))
        text_mode3 = title_font.render('小恐龍', True, (0, 0, 0))
        screen.blit(game_name, (WINDOW_SIZE[0]/3.5, WINDOW_SIZE[1]/4))
        screen.blit(text_mode1, (WINDOW_SIZE[0]/2.7, WINDOW_SIZE[1]/2.5))
        screen.blit(text_mode2, (WINDOW_SIZE[0]/2.5, WINDOW_SIZE[1]/1.8))
        screen.blit(text_mode3, (WINDOW_SIZE[0]/2.3, WINDOW_SIZE[1]/1.4))
        if btn_preview == 1:
            pg.draw.rect(screen, preview_color, BTN_mode1, 10)
        elif btn_preview == 2:
            pg.draw.rect(screen, preview_color, BTN_mode2, 10)
        elif btn_preview == 3:
            pg.draw.rect(screen, preview_color, BTN_mode3, 10)
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
                    print("Mode 1")
                    return
                elif event.button == 1 and BTN_mode2.collidepoint(event.pos):
                    interface.mode = 2
                    print("Mode 2")
                    return
                elif event.button == 1 and BTN_mode3.collidepoint(event.pos):
                    interface.mode = 3
                    opened = True
                    print("Mode 3")
                    return
            elif event.type == pg.VIDEORESIZE:
                WINDOW_SIZE = event.size
                score_font = pg.font.SysFont("Broadway", int(WINDOW_SIZE[0]/30))
                #score_font = pg.font.Font(getcwd().replace('\\', '/') + "/msjhbd.ttc", int(WINDOW_SIZE[0]/36))
                title_font = pg.font.Font(getcwd().replace('\\', '/') + "/msjhbd.ttc", int(WINDOW_SIZE[0]/18))
                screen = pg.display.set_mode(WINDOW_SIZE, pg.RESIZABLE, 32)
                bg1 = pg.transform.scale(bg1, WINDOW_SIZE)

        if not client:
            #print("connecting", client)
            try:
                client = ss.connect(Host, Port, 5)
            except:
                pass
        else:
            #print("connected")
            ring = ss.get(client)
            if ring:
                ring  = ring.replace("\n", ",").strip().split(",")[-5:-1]
                x_ang = float(ring[0])
                squeeze = float(ring[1])
                ang_v = float(ring[2])
                angle = float(ring[3])
                print(x_ang, squeeze, ang_v, angle)
                if x_ang < -30 and btn_preview > 1:
                    print("up")
                    btn_preview -= 1
                elif x_ang > 50 and btn_preview < 3:
                    print("down")
                    btn_preview += 1
                # 上下選
                if squeeze > 3300:
                    interface.mode = btn_preview
                    print("Mode", interface.mode)
                    #client.close()
                    #client = None
                    return client
        pg.display.update()
        

def dino(interface, client):
    k = PyKeyboard()
    #interface.mode = 0
    while run:
        ring = ss.get(client)
        if ring:
            ring  = ring.replace("\n", ",").strip().split(",")[-5:-1]
            x_ang = float(ring[0])
            squeeze = float(ring[1])
            ang_v = float(ring[2])
            angle = float(ring[3])
            if squeeze > 3250:
                k.press_key(k.up_key) 
                k.release_key(k.up_key)
            if x_ang > 60 or x_ang < -50:
                interface.mode = 0
                return client 
    

def game1(interface, cli):  # 已知問題  開始縮放有問題 速度隨分數增加
    # 遊戲bg
    global run, screen, WINDOW_SIZE, pivot, offset, Start_loc, all_sprites, block_list, score_font, title_font, opened
    bg2 = pg.image.load(BG2).convert_alpha()
    bg2 = pg.transform.scale(bg2, WINDOW_SIZE)
    hit = pg.mixer.Sound(HIT)
    hit.set_volume(1)
    #bg2 = pg.Surface(screen.get_size())
    #bg2 = bg2.convert()
    #bg2.fill(WHITE)
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
    Left = True
    #print(interface.mode)
    if interface.mode == 1:
        bg3 = pg.Surface(screen.get_size())
        bg3 = bg3.convert()
        bg3.fill(WHITE)
        screen.blit(bg3, (0,0))
        pg.display.update()
        text_con = title_font.render('校正中 請將健身環平舉至胸前', True, (255, 0, 0))
        screen.blit(text_con, (WINDOW_SIZE[0]/8, WINDOW_SIZE[1]/5))
        pg.display.update()
        interface.cli = cli
        w1.correction(interface)
        text_con = title_font.render('校正完成!!', True, (0, 0, 255))
        screen.blit(text_con, (WINDOW_SIZE[0]/3, WINDOW_SIZE[1]/2))
        pg.display.update()
        pg.time.wait(1000)

    while run and (interface.mode == 1 or interface.mode == 2):
        for event in pg.event.get():
            if event.type == KEYDOWN:           # 觸發關閉視窗
                if event.key == K_ESCAPE:
                    run = False
            elif event.type == QUIT:
                run = False
            elif event.type == pg.VIDEORESIZE:
                WINDOW_SIZE = event.size
                score_font = pg.font.SysFont("Broadway", int(WINDOW_SIZE[0]/30))
                #score_font = pg.font.Font(getcwd().replace('\\', '/') + "/msjhbd.ttc", int(WINDOW_SIZE[0]/36))
                title_font = pg.font.Font(getcwd().replace('\\', '/') + "/msjhbd.ttc", int(WINDOW_SIZE[0]/18))
                screen = pg.display.set_mode(WINDOW_SIZE, pg.RESIZABLE, 32)
                bg2 = pg.transform.scale(bg2, WINDOW_SIZE)
        
        w1.org_image = pg.transform.scale(w1.org_image, (int(WINDOW_SIZE[0]/36), int(WINDOW_SIZE[1]/2.5)))
        w1.zoom()
        pivot = (int(WINDOW_SIZE[0]/2) , int(WINDOW_SIZE[1]*15/16))           # 軸心
        offset = Vector2((0, int(WINDOW_SIZE[0]/8)))                           # 偏移 (武器長度的一半)
        Start_loc = [[WINDOW_SIZE[0]*i/9 , WINDOW_SIZE[0]/48] for i in range(9) ]
        # y z x_ang_v x_ang
        if interface.mode == 1:    
            ring = ss.get(interface.cli)
            if ring:
                ring  = ring.replace("\n", ",").strip().split(",")[-5:-1]
                x_ang = float(ring[0])
                squeeze = float(ring[1])
                ang_v = float(ring[2])
                angle = float(ring[3])
                print(x_ang, squeeze, ang_v, angle)
                if ang_v - w1.ang_v_offset > 100 and w1.TL == False and w1.TR == False:
                    hit.play()
                    w1.TR = True
                if ang_v - w1.ang_v_offset < -100  and w1.TR == False and w1.TL == False:
                    hit.play()
                    w1.TL = True
                #print(w1.TL, w1.TR)
                '''
                if angle - w1.offset > 9 and w1.TL == False:
                    hit.play()
                    w1.TR = True
                if angle - w1.offset < -9 and w1.TR == False:
                    hit.play()
                    w1.TL = True
                #w1.last_angle =  w1.offset - angle 
                '''
            #w1.rotation2(w1.last_angle)
            #w1.rotation(w1.last_angle/-2)
           
        else :
            rotation_direction = pg.mouse.get_rel()[0]
            #print(rotation_direction)
            if rotation_direction > 80 and w1.TL == False:
                hit.play()
                w1.TR = True
            if rotation_direction < -80 and w1.TR == False:
                hit.play()
                w1.TL = True
            #w1.rotation(rotation_direction)
        
        
        if w1.TR:
            w1.turn_r()
        if w1.TL:
            w1.turn_l()

        screen.fill(WHITE)
        screen.blit(bg2, (0,0))
        '''
        # draw doors
        for i in range(9):
            door = pg.Rect(WINDOW_SIZE[0]*i/9, 0, WINDOW_SIZE[0]/9, WINDOW_SIZE[0]/9*1.2)
            pg.draw.rect(screen, BLUE, door, 3)
            #if enemies[i].valid:
            #    enemies[i].attack()
        '''
        # random time and location
        num = random.randint(0, 4) if Left else random.randint(5, 8)
        if not enemies[num].valid and random.random()<0.025:
            enemies[num].image = pg.transform.scale(enemies[num].image, (int(WINDOW_SIZE[0]/10), int(WINDOW_SIZE[0]/11)))
            enemies[num].rect = enemies[num].image.get_rect()
            enemies[num].appear(num)
            block_list.add(enemies[num])
            all_sprites.add(enemies[num])
            Left = False if Left else True
            #enemies[num].attack()

        for each in block_list:
            each.speed = int(WINDOW_SIZE[1] / 48 )
            each.attack()
            # 沒打到
            if each.rect.y > WINDOW_SIZE[1]*9.5/12 :
                all_sprites.remove(each)
                block_list.remove(each)
                interface.hp -= 1
                each.valid = False
        # 有打到
        beaten.extend(pg.sprite.spritecollide(w1, block_list, False, pg.sprite.collide_mask))
        #print(beaten)
        sc = str(100*len(beaten)) if beaten else 0
        for each in beaten:
            if each.valid == True:                
                interface.score += 100
            each.valid = False
            each.back()

            # 超出畫面
            if each.rect.y < -20 :
                #print(123)
                all_sprites.remove(each)
                block_list.remove(each)
                beaten.remove(each)
        if sc:
            add_score = score_font.render('+'+sc, True, (255, 0, 0))
            screen.blit(add_score, (WINDOW_SIZE[0]*0.3, WINDOW_SIZE[1]*0.85))
        all_sprites.draw(screen)                             # 全部畫出來
        interface.show()
        
        '''
        pg.draw.circle(screen, (30, 250, 70), pivot, 3)
        pg.draw.rect(screen, (30, 250, 70), w1.rect, 1)  # The rect.
        for i in range(9):
            pg.draw.rect(screen, (30, 250, 70), enemies[i].rect, 1)  # The rect.
        '''
        # 正式渲染
        pg.display.update()
        clock.tick(30)

        if interface.hp == 0:
            interface.mode = 0
            text = title_font.render('Game Over', True, (255, 0, 0))
            screen.blit(text, (WINDOW_SIZE[0]*0.3, WINDOW_SIZE[1]*0.3))
            pg.display.update()
            pg.time.wait(500)
            text = title_font.render('Your Score : '+ str(interface.score), True, (255, 0, 0))
            screen.blit(text, (WINDOW_SIZE[0]*0.3, WINDOW_SIZE[1]*0.6))
            pg.display.update()
            pg.time.wait(1500)
            #if interface.mode == 1:
                #interface.cli.close()
            return interface.cli
        

if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('test')                 # 視窗標題
    screen = pg.display.set_mode(WINDOW_SIZE, pg.RESIZABLE, 32)

    block_list = pg.sprite.Group()                 # 碰撞檢測
    all_sprites = pg.sprite.Group()                # 所有角色

    interface = Interface(HEART)
    C = None
    """
    pg.font.init()
    pg.joystick.init()
    pg.mixer.init()    
    """
    run = True
    while run:
        if interface.mode == 0:
            C = start(interface, C)
        if interface.mode == 1 or interface.mode == 2 :#or interface.mode == 3:
            C = game1(interface, C)
        if interface.mode == 3:
            webbrowser.open_new_tab('https://chromedino.com/')
            C = dino(interface, C)
            opened = False
    quit()   
