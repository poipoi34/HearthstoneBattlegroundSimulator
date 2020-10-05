
import pygame as pg
from math import cos,sin,pi,sqrt
import time
import copy
from card import*
from sys import exit



class battle_manager():



	def __init__(o, player1, player2):
		o.deathrattle_buffer = []
		o.battle_data = []
		o.displayer = None
		o.player1 = player1
		o.player2 = player2
		player1.set_game_manager(o)
		player2.set_game_manager(o)
		o.save_board_state()
		


	def attach_displayer(o, displayer):
		o.displayer = displayer

	def simulate_battle(o, save_battle = False):
		
		if save_battle:
			battle_data.append(Battle())
			event.on_update_displayer.battle_manager = o

		done = False
		winner = None
		attacking_player = o.player1
		defending_player = o.player2
		o.player1.army_before_resolution = o.player1.army[:]
		o.player2.army_before_resolution = o.player2.army[:]
		event.on_enter_arena.fire({"bottom_player" : o.player1, "top_player" : o.player2})

		while (done == False):
			
			attacking_player.attack(defending_player)
			attacker_died = len(attacking_player.army) == 0
			defender_died = len(defending_player.army) == 0
			if (attacker_died and defender_died):
				return None
			if (attacker_died):
				return defending_player
			if (defender_died):
				return attacking_player

			
			for deathrattle_holder in o.deathrattle_buffer:
				deathrattle_holder.executeAll()
			o.deathrattle_buffer = []
			o.player1.clear_ghosts()
			o.player2.clear_ghosts()

			attacking_player, defending_player = defending_player, attacking_player
			


		return winner

	
	def save_board_state(o):
		o.battle_data.append(Board_state(o))


class Board_state:
	def __init__(o, battle_manager):
		o.player1 = copy.deepcopy(battle_manager.player1)
		o.player2 = copy.deepcopy(battle_manager.player2)

	def __str__(o):
		return o.player1.__str__() + " | " + o.player2.__str__();

class Battle:
	def __init__(o):
		o.battle_history = []
		

	def push(o, board_state_or_event):
		o.battle_history.append(board_state_or_event)

























