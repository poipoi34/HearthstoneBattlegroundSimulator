from random import*
import copy
from event_manager import *

class Player():
	
	def __init__(o,*,name = "p", battle_manager = None):
		

		###combat attributes
		o.name = name
		o.army = []
		o.army_before_resolution = []
		o.hand = []
		o.attacking_indice = 0
		o.battle_manager = battle_manager
		
		o.max_army = 7
		
	###event methods
	def react(s,event):
		a=0
	
	### recruiting methods
	def add_to_army(o,card,at=-1):
		if (len(o.army) < o.max_army):
			if (at==-1):
				card.owner = o
				o.army.append(card)
			else:
				i = min (len(o.army),at)
				o.army.insert(i,card)
				card.owner = o
		return o
	

	def summon(o, card, at):
		if (o.count_minion_alive() < o.max_army):
			o.army_before_resolution.insert(at, card)
			card.owner = o
			card.battle_manager = o.battle_manager
			o.get_event_manager().fire_one_shot_event("after_summon")


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

	def __str__(o):
		res = o.name + ' : '
		for card in o.army_before_resolution:
			res += card.__str__()
		return res

	def get_taunt_army(o):
		taunt_army = []
		for minion in o.army_before_resolution:
			if not minion.ghost and minion.taunt:
				taunt_army.append(minion)
		return taunt_army

	### combat methods
	def attack(o,opponent):
		i = o.attacking_indice
		
		while (i < len(o.army) and o.army[i].can_attack == False):
			i += 1
		if (i >= len(o.army)):
			o.reset_attacks()
			i = 0
		while (i < len(o.army) and o.army[i].can_attack == False):
			i += 1
			
		if (i < len(o.army)):
			opponent_taunt_army = opponent.get_taunt_army()
			if opponent_taunt_army == []:
				attackedI = randrange(len(opponent.army))
				o.army[i].fight(opponent.army[attackedI])
			else:
				attackedI = randrange(len(opponent_taunt_army))
				o.army[i].fight(opponent_taunt_army[attackedI])
		else:
			raise ValueError("player attack method couldn't find attackant")

		o.attacking_indice = i

	def clear_ghosts(o):
		for minion in o.army_before_resolution:
			if minion.ghost:
				o.army_before_resolution.remove(minion)

		o.army = o.army_before_resolution[:]

	def reset_attacks(s):
		for crea in s.army:
			if crea.attack > 0:
				crea.can_attack = True

	def set_battle_manager(o, battle_manager):
		for card in o.army:
			card.set_battle_manager(battle_manager)
		o.battle_manager = battle_manager

	def get_event_manager(o):
		return o.battle_manager.event_manager

	#copy state of a player to store it in battle history
	def copy_state(o):
		res = Player(name = o.name)
		copied_army = []
		for card in o.army_before_resolution:
			copied_army.append(copy.copy(card))
		res.army_before_resolution = copied_army
		return res
	
	#clone players so that they can battle to the death for our entertainment
	def clone(o):
		clone = Player(name = "clone of " + o.name)
		for card in o.army:
			clone.add_to_army(copy.deepcopy(card))#deepcopy for the deathrattles, can't clone card because of subclasses
		
		clone.attacking_indice = o.attacking_indice
		return clone

	
	def __repr__(o):
		return o.__str__()
	
	def register_listerners(o, event_manager):
		for card in o.army:
			event_manager.add_listener(card)