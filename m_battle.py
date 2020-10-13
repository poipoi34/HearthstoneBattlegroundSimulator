from m_event import Event_manager
import pygame as pg
from math import cos,sin,pi,sqrt
import time
import copy
import m_card
from sys import exit
import m_event
import m_interfaces



class battle_manager():



	def __init__(o, player1, player2):
		o.deathrattle_buffer = []
		o.battle_data = []
		o.displayer = None
		o.player1 = player1.clone()
		o.player2 = player2.clone()
		o.player1.opponent = o.player2
		o.player2.opponent = o.player1
		o.player1.set_battle_manager(o)
		o.player2.set_battle_manager(o)
		
		o.event_manager = Event_manager(o)
		o.event_manager.battle_manager = o
		o.player1.register_listerners(o.event_manager)
		o.player2.register_listerners(o.event_manager)


		

	def attach_displayer(o, displayer):
		o.displayer = displayer
		o.displayer.set_event_manager(o.event_manager)
		

	def simulate_battle(o, save_battle = True):

		done = False
		winner = None
		attacking_player = o.player1
		defending_player = o.player2
		o.player1.army_before_resolution = o.player1.army[:]
		o.player2.army_before_resolution = o.player2.army[:]
		if o.displayer != None:
			displayer.replay(o.battle_data)

		o.event_manager.spread_event("on_enter_arena", {"bottom_player" : o.player1, "top_player" : o.player2})
		
		while (done == False):
			
			attacking_player.attack(defending_player)
			while (o.event_manager.action_buffer != [] or o.deathrattle_buffer != []):
				o.event_manager.release_buffer()
				for deathrattle in o.deathrattle_buffer:
					deathrattle()
				o.deathrattle_buffer = []
				o.player1.clear_ghosts()
				o.player2.clear_ghosts()
			o.player1.clear_ghosts()
			o.player2.clear_ghosts()



			attacker_died = len(attacking_player.army) == 0
			defender_died = len(defending_player.army) == 0
			if (attacker_died and defender_died):
				return None
			if (attacker_died):
				return defending_player
			if (defender_died):
				return attacking_player
			attacking_player, defending_player = defending_player, attacking_player
			
		return winner

	
	def save_board_state(o, event):
		o.battle_data.append(Board_state(o, event))
	
	def print_battle_data(o):
		print([str(item) for item in o.battle_data])

	def __repr__(o):
		return "battle between " + o.player1.name + " and " + o.player2.name

class Board_state:
	def __init__(o, battle_manager, event):
		o.player1 = battle_manager.player1.copy_state()
		o.player2 = battle_manager.player2.copy_state()
		o.event = event

	def __str__(o):
		return "-> event : " + o.event.__str__() + "\n|||Board state ::" + o.player1.__str__() + " | " + o.player2.__str__();

