from webbrowser import get
import pygame
from pygame.locals import *
from mutagen.id3 import ID3
from io import BytesIO
from PIL import Image
import vlc
import sys
import os
import random
import time

#関数
def enimg(img_path,mode = 0):
    if img_path == "":
        return ""
    else:
        if mode == 0:
            return pygame.image.load(img_path)
        else:
            return pygame.image.load(img_path).convert()

mp = vlc.MediaPlayer() 
def update():
    # pygame.mixer.music.stop()
    mp.set_mrl("../" + data[num][2])
    tags = ID3("../" + data[num][2])
    mp.play()
    while True:
        if mp.get_length() != 0:
            length = mp.get_length()/1000
            break
    img = tags.get("APIC:")
    if img is not None:
        cover_img = Image.open(BytesIO(img.data))
        cover_img.save("images/stock_image.png")
        bg = pygame.transform.scale(enimg("images/stock_image.png"), (500, 500))
    else:
        bg = icon
    return tags, bg, length

#ファイル名取得
music_path = []
for file in os.listdir("../../music_player"):
    files = os.path.splitext(file)
    if files[1] == '.mp3':
        music_path.append(file)
data = []
for i in music_path:
    tags = ID3("../" + i)
    data.append([str(tags.get("TIT2")),str(tags.get("TPE1")),i])

pygame.init()

# 画面の生成
screen = pygame.display.set_mode((500,400))
pygame.display.set_icon(enimg("images/icon.png"))
pygame.display.set_caption("Music Player")

#画像生成
pause = pygame.transform.scale(enimg("images/pause.png"), (48, 48))
replay = pygame.transform.scale(enimg("images/replay.png"), (48, 48))
play = pygame.transform.scale(enimg("images/play.png"), (48, 48))
next = pygame.transform.scale(enimg("images/skip_next.png"), (48, 48))
pre = pygame.transform.scale(enimg("images/skip_previous.png"), (48, 48))
top = pygame.transform.scale(enimg("images/skip_top.png"), (48, 48))
repeat_off = pygame.transform.scale(enimg("images/repeat_off.png"), (48, 48))
repeat = pygame.transform.scale(enimg("images/repeat.png"), (48, 48))
repeat_one = pygame.transform.scale(enimg("images/repeat_one.png"), (48, 48))
shuffle_off = pygame.transform.scale(enimg("images/shuffle_off.png"), (24, 24))
shuffle = pygame.transform.scale(enimg("images/shuffle.png"), (24, 24))
sort_off = pygame.transform.scale(enimg("images/sort_off.png"), (24, 24))
sort = pygame.transform.scale(enimg("images/shufflea.png"), (24, 24))
drag = pygame.transform.scale(enimg("images/drag.png"), (36, 36))
drag_light = pygame.transform.scale(enimg("images/drag_light.png"), (36, 36))
icon = pygame.transform.scale(enimg("images/icon.png"), (500, 500))
blackfilter = pygame.Surface((500, 400),flags=pygame.SRCALPHA)
blackfilter.fill((0,0,0,200))

#フォント
font1 = pygame.font.SysFont('yugothicuisemibold', 40)
font2 = pygame.font.SysFont('yugothic', 25)
font3 = pygame.font.SysFont('yugothicuisemibold', 25)
font4 = pygame.font.SysFont('yugothicuisemibold', 25)
font5 = pygame.font.SysFont('yugothic', 20)

# 音源
# pygame.mixer.init(frequency = 44100)
# pygame.mixer.music.load("../" + music_path[0])
# # pygame.mixer.music.play(1)

# bgm_volume = setting_data[11]/100
# pygame.mixer.music.set_volume(bgm_volume)
# pygame.mixer.music.play(-1)

#ボタン生成
play_button = pygame.Rect(225, 310, 48, 48)
next_button = pygame.Rect(317, 310, 48, 48)
pre_button = pygame.Rect(132, 310, 48, 48)
top_button = pygame.Rect(40, 310, 48, 48)
repeat_button = pygame.Rect(410, 310, 48, 48)
list_button = pygame.Rect(20, 190, 10, 20)
shuffle_button = pygame.Rect(13, 260, 24, 24)
sort_button = pygame.Rect(13, 320, 24, 24)
speedup_button = pygame.Rect(465, 60, 10, 20)
speeddown_button = pygame.Rect(375, 60, 10, 20)

active = True
num = 0
repeat_num = 0
pos = []
tags, bg, length = update()

hold = False
hold_pos = 0

cursor_sta = 0

list_switch = False
list_pos = 0
shuffle_switch = False
sort_switch = False

speed = 1.0

while active:
    state = mp.get_state()
    #画面の描写
    #背景
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, -50))
    screen.blit(blackfilter,(0,0))
    #アイコン
    if state == 6 and repeat_num == 0:
        screen.blit(replay, (225, 310))
    else:
        if state == 3:
            screen.blit(pause, (225, 310))
        else:
            screen.blit(play, (225, 310))
    if repeat_num == 2:
        screen.blit(repeat_one, (410, 310))
    elif repeat_num == 1:
        screen.blit(repeat, (410, 310))
    else:
        screen.blit(repeat_off, (410, 310))
    screen.blit(next, (317, 310))
    screen.blit(pre, (132, 310))
    screen.blit(top, (40, 310))
    pygame.draw.polygon(screen, (255,255,255), [(465,60),(465,80),(475,70)], 0)
    pygame.draw.polygon(screen, (255,255,255), [(385,60),(385,80),(375,70)], 0)
    screen.blit(font3.render('x{:.1f}'.format(speed), True, (255,255,255)), (401, 58))
    if list_switch == False:
        pygame.draw.polygon(screen, (255,255,255), [(20,190),(20,210),(30,200)], 0)
    #曲情報
    pos_time = mp.get_time()/1000
    end_time = font3.render(time.strftime("%H:%M:%S",time.gmtime(round(length))), True, (255,255,255))
    screen.blit(end_time, (380, 20))
    # if state == 6 and repeat_num == 0:
    #     pos = font3.render(time.strftime("%H:%M:%S",time.gmtime(round(length))) + " /", True, (255,255,255))
    # else:
    #     pos = font3.render(time.strftime("%H:%M:%S",time.gmtime(round(pos_time))) + " /", True, (255,255,255))
    # screen.blit(pos, (250, 20))
    screen.blit(font3.render(time.strftime("%H:%M:%S",time.gmtime(round(pos_time))) + " /", True, (255,255,255)), (250, 20))
    title = font1.render(str(tags.get("TIT2")), True, (255,255,255))
    screen.blit(title, (10, 10))
    # pygame.draw.line(screen, (255,255,255), (0,50), ((font1.size(str(tags.get("TIT2")))[0]),50),2)
    artist = font2.render(str(tags.get("TPE1")), True, (200,200,200))
    screen.blit(artist, (20, 55))
    pygame.draw.line(screen, (100,100,100), (50,280), (450,280),3)
    if hold == False:
        pygame.draw.circle(screen,(255,255,255),(50+400/length*pos_time,280),8)
        if state == 6 and repeat_num == 0:
            pygame.draw.line(screen, (255,255,255), (50,280), (450,280),3)
        else:
            pygame.draw.line(screen, (255,255,255), (50,280), (50+400/length*pos_time,280),3)
    else:
        pygame.draw.line(screen, (255,255,255), (50,280), (hold_pos,280),3)
        pygame.draw.circle(screen,(255,255,255),(hold_pos,280),8)
    #リスト
    if list_switch == True:
        screen.blit(blackfilter,(0,0))
        pygame.draw.polygon(screen, (255,255,255), [(30,190),(30,210),(20,200)], 0)
        if shuffle_switch == True:
            screen.blit(shuffle, (13, 260))
        else:
            screen.blit(shuffle_off, (13, 260))
        if sort_switch == True:
            screen.blit(sort, (13, 320))
        else:
            screen.blit(sort_off, (13, 320))
        # screen.fill((100,100,100), (0,0,400,400))
        for i in range(len(data)):
            if i == num:
                screen.blit(font4.render(data[i][0], True, (0,255,200)), (60, list_pos + 20 + i*50))
                screen.blit(font5.render(data[i][1], True, (0,255,200)), (90 + (font4.size(data[i][0])[0]), list_pos + 23 + i*50))
                pygame.draw.line(screen, (0,255,200), (60, list_pos + (i+1)*50), (440, list_pos + (i+1)*50),1)
                screen.blit(drag_light, (390, list_pos + (i+1)*50 - 35))
            else:
                screen.blit(font4.render(data[i][0], True, (255,255,255)), (60, list_pos + 20 + i*50))
                screen.blit(font5.render(data[i][1], True, (255,255,255)), (90 + (font4.size(data[i][0])[0]), list_pos + 23 + i*50))
                pygame.draw.line(screen, (255,255,255), (60, list_pos + (i+1)*50), (440, list_pos + (i+1)*50),1)
                screen.blit(drag, (390, list_pos + (i+1)*50 - 35))
            # screen.fill((255,0,0), (250, (list_pos + 30 + (i+1)*50), 300, (list_pos + 35 + (i+1)*50)))





    if state == 6:
        if repeat_num == 1:
            num += 1
        if repeat_num != 0:
            tags, bg, length = update()

    # 画面更新
    pygame.display.update()
    pygame.time.wait(10)

    for e in pygame.event.get():
        if e.type == QUIT:
            active = False
            pygame.quit()
            sys.exit()
        if list_switch == True:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 4:
                    if list_pos <= -20:
                        list_pos += 20
                if e.button == 5:
                    if list_pos >= (len(data)-7)*(-50):
                        list_pos -= 20
                if list_button.collidepoint(e.pos):
                    list_switch = False
                if shuffle_button.collidepoint(e.pos):
                    if shuffle_switch == False:
                        stock_data = data
                        stock_playing = data.pop(num)
                        data = random.sample(data, len(data))
                        data.insert(0, stock_playing)
                        num = 0
                    else:
                        data = stock_data
                    shuffle_switch = not shuffle_switch
                if sort_button.collidepoint(e.pos):
                    sort_switch = not sort_switch

        else:
            if hold == True or ((358 >= pygame.mouse.get_pos()[1] >= 310) and ((273 >= pygame.mouse.get_pos()[0] >= 225) or (365 >= pygame.mouse.get_pos()[0] >= 317) or (180 >= pygame.mouse.get_pos()[0] >= 132) or (88 >= pygame.mouse.get_pos()[0] >= 40) or (458 >= pygame.mouse.get_pos()[0] >= 410))) or ((56+400/length*pos_time >= pygame.mouse.get_pos()[0] >= 44+400/length*pos_time) and (286 >= pygame.mouse.get_pos()[1] >= 270)) or ((450 >= pygame.mouse.get_pos()[0] >= 50) and (282 >= pygame.mouse.get_pos()[1] >= 270)):
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
                cursor_sta = 1
            elif cursor_sta == 1:
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
                cursor_sta = 0
            if e.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(e.pos):
                    if state == 6:
                        tags, bg, length = update()
                    else:
                        mp.pause()
                elif top_button.collidepoint(e.pos):
                    tags, bg, length = update()
                elif repeat_button.collidepoint(e.pos):
                    repeat_num += 1
                    if repeat_num == 3:
                        repeat_num = 0
                elif next_button.collidepoint(e.pos) or pre_button.collidepoint(e.pos):
                    if next_button.collidepoint(e.pos):
                        num += 1
                    elif pre_button.collidepoint(e.pos):
                        num -= 1
                    tags, bg, length = update()
                if list_button.collidepoint(e.pos):
                    list_switch = True
                if speedup_button.collidepoint(e.pos):
                    speed += 0.1
                    mp.set_rate(speed)
                elif speeddown_button.collidepoint(e.pos):
                    speed -= 0.1
                    mp.set_rate(speed)
                if ((56+400/length*pos_time >= e.pos[0] >= 44+400/length*pos_time) and (286 >= e.pos[1] >= 270)) or (50 < e.pos[0] < 450) and (282 >= e.pos[1] >= 270):
                        hold = True
            if hold == True:
                if pygame.mouse.get_pressed()[0]:
                    hold_pos = pygame.mouse.get_pos()[0]
                    if pygame.mouse.get_pos()[0] <= 50:
                        hold_pos = 50
                    elif pygame.mouse.get_pos()[0] >= 450:
                        hold_pos = 450
                else:
                    hold = False
                    if state == 4:
                        mp.pause()
                    mp.set_time(round((hold_pos-50)*2.5*length))
