
import pygame as pg
from math import cos,sin,pi,sqrt
import time
from random import*
from card import*
from sys import exit
from basic_bg import*
import event



class Displayer(event.Observer):

	divineShield = pg.Surface([60, 110])
	divineShield.fill(pg.Color(255, 255, 0))
	divineShield.set_alpha(128)
	
	def __init__(o):
		event.Observer.__init__(o)
		event.add_subscriber(o, "enter arena", o.react_enter_arena)
		event.add_subscriber(o, "on minion attack", o.react_minion_on_attack)
		event.add_subscriber(o, "after minion attack", o.react_minion_after_attack)
		event.add_subscriber(o, "after summon", o.react_after_summon)
		
		pg.init()
		o.win = [1000,1000]
		o.screen = pg.display.set_mode(o.win)

		o.display_mode = "arena"
		###arena
		o.arena = pg.Surface(o.win)
		o.arena.set_colorkey([0,0,0])
		line_color = [255,0,0]
		pg.draw.line(o.arena,line_color,[o.win[0]/5,0],[o.win[0]/5,o.win[1]])
		pg.draw.line(o.arena,line_color,[4*o.win[0]/5,0],[4*o.win[0]/5,o.win[1]])
		for i in range(4):
			pg.draw.line(o.arena,line_color,[0,o.win[1]*i/4],[o.win[0],o.win[1]*i/4])

		###players
		o.att_player = []
		o.def_player = []
		o.bot_player = []
		o.top_player = []


	def get_image(o, card): #create and return an image (maybe store it too? problem, it has to be updated)

		image = pg.Surface([50,100])
		image.fill([130,100,255])

		font = pg.font.Font('freesansbold.ttf', 20)
		attack_text = font.render(str(card.attack), True, [0,255,0])
		h_color = [0,255,0]
		if (card.health < card.max_health):
			h_color = [255,0,0]
		health_text = font.render(str(card.health), True, h_color)

		att_surface = attack_text.get_rect()
		hlth_surface = health_text.get_rect()

		blitPosA = [0, 100 - att_surface[3]]
		blitPosH = [50 - hlth_surface[2], 100 - hlth_surface[3]]

		image.blit(attack_text,blitPosA)
		image.blit(health_text,blitPosH)


		if (card.divineShield):
			o.divineShield.blit(image, [5,5])
			return o.divineShield

		return image

	def draw_card(o,card):
		cardImage = o.get_image(card)
		o.screen.blit(cardImage,card.get_position(o))


	def react_enter_arena(o,event):


		o.bot_player = event.param[0]
		o.top_player = event.param[1]
			
		if (len(o.bot_player.army) < len(o.top_player.army)):
			o.att_player = o.top_player
		if (len(o.bot_player.army) > len(o.top_player.army)):
			o.att_player = o.bot_player
		else:
			if (random() < 0.5):
				o.att_player = o.bot_player
			else:
				o.att_player = o.top_player

		o.update_arena()

	def draw_army(o,player):
		for c in player.army_before_resolution:
			if not c.ghost:
				o.draw_card(c)


	def react_after_summon(o, event):
		o.update_arena()
	
	def update_arena(o):
		o.screen.fill([0,0,0])	
		o.draw_army(o.top_player)
		o.draw_army(o.bot_player)
		o.screen.blit(o.arena,[0,0])
		o.update()

	def react_minion_on_attack(o, event): # minion = card?????
		attacking_minion = event.param[0]
		attacked_minion = event.param[1]
		attacking_minion.get_center(o)			
		pg.draw.line(o.screen,[255,255,255],
						attacking_minion.get_center(o),
						attacked_minion.get_center(o))
		p = attacked_minion.get_center(o)
		pg.draw.rect(o.screen, [200, 200, 200], [p[0]-5,p[1]-5,10, 10])
		o.update()
			
	def react_minion_after_attack(o, event):
		o.update_arena()
			
			
	
	def update(o):
		if (o.display_mode == "arena"):
			pg.display.flip()

	def quit(o):
		pg.quit()
		
		
	
	









		
