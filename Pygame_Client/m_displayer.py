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
		o.time_line = []
		o.event_sequence = [] # no real use, it's a debugging feature
		o.running_animation = []
		o.current_frame = 0
		o.chrono = m_animation.Chrono()
		o.frame_by_frame = True
		o.frame_time = 0.016


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
		o.make_time_line(battle_data)

		i = 0
		o.chrono.start()

		while not end_of_battle or o.running_animation != []:

			frame_to_jump = 0
			if not o.frame_by_frame:
				frame_to_jump = o.chrono.elapsed_time() // o.frame_time
				if frame_to_jump != 0:
					o.current_frame = o.current_frame + frame_to_jump
					o.rewind(frame_to_jump * o.frame_time)
			if o.frame_by_frame:
				if (o.chrono.elapsed_time() >= o.frame_time):
					o.current_frame += 1
					frame_to_jump = 1
					o.chrono.start()

			if i<len(battle_data)-1:
				
				while i<len(battle_data)-1 and o.current_frame >= o.time_line[i]:
					o.buffer_animation(battle_data[i])
					if battle_data[i].event.type == "end_of_battle":
						end_of_battle = True
					i+=1

			for anim in o.running_animation:
				finished = anim.update(frame_to_jump)
				if finished:
					o.running_animation.remove(anim)

			o.draw_everything()

				

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

	def make_time_line(o,battle_data):
		frame_cursor = 0
		i = 0
		while i < len(battle_data):
			stop = False
			max_length = 0
			id_used = []
			while not stop and i<len(battle_data):
				animation_type = m_animation.event_animation_correspondance[battle_data[i].event.type]
				o.time_line.append(frame_cursor)
				max_length = max(max_length,animation_type.get_length(battle_data[i]))
				id_used += animation_type.get_id_used(battle_data[i])
				if i>= len(battle_data)-1:
					break
				next_animation = m_animation.event_animation_correspondance[battle_data[i+1].event.type]
				if animation_type.stopping or o.conflict(id_used,next_animation.get_id_used(battle_data[i+1])):
					stop = True
				else :
					i+=1
					
			frame_cursor += max_length
			i+=1

	def conflict(o,id_used,id_list):
		for id in id_list:
			if id_used.count(id) > 0:
				return True
		return False
		
			


	def buffer_animation(o,board_state):
		event_type = board_state.event.type
		if event_type == "on_enter_arena":
			o.running_animation.append(m_animation.on_enter_arena(o,board_state))
		if event_type == "before_minion_attack":
			o.running_animation.append(m_animation.before_minion_attack(o,board_state))
		if event_type == "on_minion_attack":
			o.running_animation.append(m_animation.on_minion_attack(o,board_state))
		if event_type == "after_minion_attack":
			o.running_animation.append( m_animation.after_minion_attack(o,board_state))
		if event_type == "on_take_damage":
			o.running_animation.append(m_animation.on_take_damage(o,board_state))
		else:
			o.running_animation.append(m_animation.refresh_board_state(o,board_state))

			
			
	
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
	

	









		
