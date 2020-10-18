import pygame as pg
from math import cos,sin,pi,sqrt
from time import time
from random import*

from sys import exit
from inspect import signature
from m_card_image import Card_image
import m_animation

card_width = 75
card_height = 150
divine_shield_margin = 5



class Displayer:

	divine_shield = pg.Surface([card_width + divine_shield_margin*2, card_height + divine_shield_margin*2])
	divine_shield.fill(pg.Color(255, 255, 0))
	divine_shield.set_alpha(128)
	
	def __init__(o, battle_manager):
		pg.init()
		o.win = [1000,1000]
		o.screen = pg.display.set_mode(o.win)
		o.battle_manager = battle_manager
		o.object_to_draw = {}


		o.display_mode = "arena"
		###arena
		#o.battle_data = o.battle_manager.battle_data
		o.arena = pg.Surface(o.win)
		o.arena.set_colorkey([0,0,0])
		line_color = [255,0,0]
		pg.draw.line(o.arena,line_color,[o.win[0]/5,0],[o.win[0]/5,o.win[1]])
		pg.draw.line(o.arena,line_color,[4*o.win[0]/5,0],[4*o.win[0]/5,o.win[1]])
		for i in range(4):
			pg.draw.line(o.arena,line_color,[0,o.win[1]*i/4],[o.win[0],o.win[1]*i/4])


	def get_image(o, card): ##################################OBSOLETE TO DELETE

		image = pg.Surface([card_width,card_height])
		image.fill([130,100,255])

		font = pg.font.Font('freesansbold.ttf', 20)
		attack_text = font.render(str(card.attack), True, [0,255,0])
		h_color = [0,255,0]
		if (card.health < card.max_health):
			h_color = [255,0,0]
		health_text = font.render(str(card.health), True, h_color)

		att_surface = attack_text.get_rect()
		hlth_surface = health_text.get_rect()

		blitPosA = [0, card_height - att_surface[3]]
		blitPosH = [card_width - hlth_surface[2], card_height - hlth_surface[3]]

		image.blit(attack_text,blitPosA)
		image.blit(health_text,blitPosH)


		if (card.divine_shield):
			o.divine_shield.blit(image, [5,5])
			return o.divine_shield

		return image

	def draw_card(o,card):
		cardImage = o.get_image(card)
		o.screen.blit(cardImage,card.get_position(o))

	

	def draw_army(o,player):
		for c in player.army_before_resolution:
			if not c.ghost:
				o.draw_card(c)


	def react_after_summon(o, listener, param):
		o.update_arena()
	
	def update_arena(o):
		o.screen.fill([0,0,0])	
		o.draw_army(o.top_player)
		o.draw_army(o.bot_player)
		o.screen.blit(o.arena,[0,0])
		o.update()

	def react_minion_on_attack(o, listener, param): # minion = card?????
		o.update_arena()
		attacking_minion = param["source_minion"]
		attacked_minion = param["target_minion"]
		attacking_minion.get_center(o)			
		pg.draw.line(o.screen,[255,255,255],
						attacking_minion.get_center(o),
						attacked_minion.get_center(o))
		p = attacked_minion.get_center(o)
		pg.draw.rect(o.screen, [200, 200, 200], [p[0]-5,p[1]-5,10, 10])
		o.update()
			
	def react_minion_after_attack(o, listener, param):
		o.update_arena()
			

		
		######## SECOND GENERATION DISPLAYER ########

	def play(o,battle_data):#play a game from a finished written battle_data or a battle_data in writing in a thread
		end_of_battle = False
		i = -1
		while not end_of_battle:
			if i<len(battle_data)-1:
				i+=1
				animation = o.make_animation(battle_data[i]) # switch sur l'event_type pour savoir quel enfant de animation faire
				finished = False
				while not finished :
					finished,changed = animation.update()
					if changed:
						o.draw_everything()
				if battle_data[i].event.type == "end_of_battle":
					end_of_battle = True

			##pygame loop
			for event in pg.event.get():
				if event.type == pg.QUIT:
					displayer.quit()

	def draw_everything(o):
		o.screen.fill([0,0,0])
		for id_card in o.object_to_draw:
			card = o.object_to_draw[id_card]
			pos = []
			o.screen.blit(card.get_image(),[card.pos[0]-card.card_size[0]/2,card.pos[1]-card.card_size[1]/2])
		o.screen.blit(o.arena,[0,0])
		o.update()




	def make_animation(o,board_state):
		event_type = board_state.event.type
		if event_type == "on_enter_arena":
			return m_animation.on_enter_arena(o,board_state) 
		if event_type == "before_minion_attack":
			return m_animation.before_minion_attack(o,board_state) 
		if event_type == "on_minion_attack":
			return m_animation.on_minion_attack(o,board_state) 
		if event_type == "after_minion_attack":
			return m_animation.after_minion_attack(o,board_state) 
		else:
			return m_animation.refresh_board_state(o,board_state)

			
			
	
	def update(o):
		if (o.display_mode == "arena"):
			pg.display.flip()

	def display():
		while True:
			return

	def quit(o):
		pg.quit()
		
	def __repr__(o):
		return "battle displayer"
	

	









		
