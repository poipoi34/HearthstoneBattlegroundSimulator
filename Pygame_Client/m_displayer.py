import pygame as pg
from math import cos,sin,pi,sqrt
from time import time
from random import*

from sys import exit
from inspect import signature
from m_object import *
import m_animation

card_width = 75
card_height = 150
divine_shield_margin = 5



class Displayer:
	
	def __init__(o, battle_manager):
		pg.init()
		o.win = [1000,1000]
		o.screen = pg.display.set_mode(o.win)
		o.battle_manager = battle_manager

		o.game_object = {}
		o.displayer_object = []


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
		for id_card in o.game_object:
			card = o.game_object[id_card]
			o.screen.blit(card.get_transformed_image(),card.get_draw_pos())
		o.screen.blit(o.arena,[0,0])
		for display_object in o.displayer_object:
			o.screen.blit(display_object.get_transformed_image(),display_object.get_draw_pos())
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
		if event_type == "on_take_damage":
			return m_animation.on_take_damage(o,board_state)
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
	

	









		
