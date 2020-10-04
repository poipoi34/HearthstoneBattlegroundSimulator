
import pygame as pg
from math import cos,sin,pi,sqrt
import time
from random import*
from card import*
from sys import exit

class player():
	
	def __init__(o,*,name = "p"):
		
		#combat attributes
		o.name = name
		o.army = []
		o.army_before_resolution = []
		o.hand = []
		o.attacking_indice = 0

		
	###event methods
	def react(s,event):
		a=0
	
	### recruiting methods
	def add_to_army(o,card,at=-1):
		if (len(o.army) < 7):
			if (at==-1):
				card.owner = o
				o.army.append(card)
			else:
				i = min (len(o.army),at)
				o.army.insert(i,card)
				card.owner = o
		return o
	

	def summon(o, card, at):
		if (o.count_minion_alive() < 7):
			o.army_before_resolution.insert(at, card)
			card.owner = o
			event.create_event(event.Event("after summon",[card]))


	def count_minion_alive(o):
		size = 0
		for minion in o.army_before_resolution:
			if not minion.ghost:
				size +=1
		return size
	
	def update_minion_pos(o):
		pos = 0
		for minion in o.army_before_resolution:
			if not minion.ghost:
				minion.pos = pos
				pos +=1

	


	### combat methods
	def attack(s,player):
		i = s.attacking_indice
		
		while (i < len(s.army) and s.army[i].can_attack == False):
			i += 1
		if (i == len(s.army)):
			s.reset_attacks()
			i = 0
		while (i < len(s.army) and s.army[i].can_attack == False):
			i += 1
			
		if (i < len(s.army)):
			attackedI = randrange(len(player.army))
			s.army[i].fight(player.army[attackedI])
		else:
			raise ValueError("player attack method couldn't find attackant")

		s.attacking_indice = i

	def clear_ghosts(o):
		for minion in o.army_before_resolution:
			if minion.ghost:
				o.army_before_resolution.remove(minion)

		o.army = o.army_before_resolution[:]

	def reset_attacks(s):
		for crea in s.army:
			if crea.attack > 0:
				crea.can_attack = True

	def set_game_manager(o, game_manager):
		for card in o.army:
			card.set_game_manager(game_manager)
		o.game_manager = game_manager


				

class game_manager():
	def __init__(o):
		o.deathrattle_buffer = []

	
	def simulate_fight(o,player1,player2):
		#player 1 starts the fight
		done = False
		winner = None
		player1.set_game_manager(o)
		player2.set_game_manager(o)
		attacking_player = player1
		defending_player = player2
		player1.army_before_resolution = player1.army[:]
		player2.army_before_resolution = player2.army[:]
		event.create_event(event.Event("enter arena",[player1,player2]))

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
			player1.clear_ghosts()
			player2.clear_ghosts()

			attacking_player, defending_player = defending_player, attacking_player
			


		return winner

	###event methods
	def react(s,event):
		a=0
			
"""
for i in range(100):
	voidWalker = Card(1,3,name = "void walker")
	brann = Card(2,4,name = "brann")
	baron = Card(1,7,name = "baron")
	magmaRager = Card(5,1,name = "magma rager")


	player1 = player(name = "p1")
	player2 = player(name = "p2")

	player1.add(voidWalker)
	player1.add(baron)

	player2.add(brann)
	player2.add(magmaRager)

	g_manager = game_manager()
	print(g_manager.simulate_fight(player1,player2) == player1)


"""



























