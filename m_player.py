from random import*
import copy


class Player():
	
	def __init__(o,*,name = "p", battle_manager = None):
		

		###combat attributes
		o.name = name
		o.army = []#ne pas appeler
		o.army_before_resolution = []
		o.hand = []
		o.attacking_indice = 0
		o.battle_manager = battle_manager

		o.opponent = None
		
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
			card.set_battle_manager(o.battle_manager)
			card.set_event_manager(o.battle_manager.event_manager)
			o.get_event_manager().spread_event("after_summon", {"summoned_minion" : card})


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

	def get_army(o):
		army = []
		for card in o.army_before_resolution:
			if not card.ghost:
				army.append(card)
		return army

	### combat methods
	def command_attack(o,card,player = None):
		if player == None:
			player = o.opponent
		player_taunt_army = player.get_taunt_army()
		if player_taunt_army == []:
			alive_army = player.get_army()

			attackedI = randrange(len(alive_army))
			card.fight(alive_army[attackedI])
		else:
			attackedI = randrange(len(player_taunt_army))
			card.fight(player_taunt_army[attackedI])


	def attack(o,player = None):
		if player == None:
			player = o.opponent
		i = o.attacking_indice
		
		while (i < len(o.army) and o.army[i].can_attack == False):
			i += 1
		if (i >= len(o.army)):
			o.reset_attacks()
			i = 0
		while (i < len(o.army) and o.army[i].can_attack == False):
			i += 1
		if i==len(o.army):
			raise ValueError("player attack method couldn't find attackant")

		o.command_attack(o.army[i],player)

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
			copied_card = copy.copy(card)
			copied_card.origine = id(card)
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
			card.set_event_manager(event_manager)