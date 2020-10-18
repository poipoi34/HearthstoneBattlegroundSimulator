import pygame as pg
from math import cos,sin,pi,sqrt
import time
from random import*
from sys import exit

pg.init()
win = [1000,1000]

screen = pg.display.set_mode(win)

cardX = 50
cardY = 100

card = pg.Surface([cardX,cardY])

card.fill([130,100,255])

divineShield = pg.Surface([60, 110])
divineShield.fill(pg.Color(255, 255, 0))
divineShield.set_alpha(128)



attack = 6
health = 255


font = pg.font.Font('freesansbold.ttf', 20)
attack_text = font.render(str(attack), True, [0,255,0])
health_text = font.render(str(health), True, [0,255,0])

att_surface = attack_text.get_rect()
hlth_surface = health_text.get_rect()

blitPosA = [0,cardY-att_surface[3]]
blitPosH = [cardX-hlth_surface[2],cardY-hlth_surface[3]]

card.blit(attack_text,blitPosA)
card.blit(health_text,blitPosH)


screen.blit(card,[win[0]/2,win[1]/2])
screen.blit(divineShield, [win[0]/2-5,win[1]/2-5])


pg.display.update()










a = True
while (a):
	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			a = False
			
