from random import*
import event_manager

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
			event_manager.Event("after_summon").fire()


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


	### combat methods
	def attack(s,player):
		i = s.attacking_indice
		
		while (i < len(s.army) and s.army[i].can_attack == False):
			i += 1
		if (i >= len(s.army)):
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

	def set_battle_manager(o, battle_manager):
		for card in o.army:
			card.set_battle_manager(battle_manager)
		o.game_manager = battle_manager

	def deepcopy(o):
		res = player(name = o.name)
		res.army_before_resolution = o.army_before_resolution[:]
		return res

	def __repr__(o):
		return o.__str__()
	