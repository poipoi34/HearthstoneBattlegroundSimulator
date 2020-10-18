class Card_interface:
	def __init__(o,card):
		o.attack = card.attack
		o.health = card.health
		o.max_attack = card.max_attack
		o.max_health = card.max_health
		o.divineShield= card.divineShield
		o.deathrattle_list = card.deathrattle_list[:]
		o.buff_list = card.buff_list[:]
		o.ghost = card.ghost

		o.taunt = card.taunt

		o.name = card.name

		o.owner = card.owner # ~~~ 

		o.id_source = id(card)

	def __str__(o):
		return "["+ o.name + "/" + str(o.attack) + "/" + str(o.health) + "/" + str(hex(o.id_source))[7:13] + "]"

	def __repr__(o):
		return o.__str__()

	#return dict
	def encode_json(o):
		return {
			"id" : id(o),
			"name" : o.name,
			"attack" : o.attack,
			"health" : o.health,
			"max_attack" : o.max_attack,
			"max_health" : o.max_health,
			"divine_shield" : o.divineShield,
			"ghost" : o.ghost,
			"taunt" : o.taunt,
			"owner" : id(o.owner)
			}
		##todo##
		#ajouter deathrattle list
		#ajouter buff list
		

class Player_interface:
	def __init__(o, player):
		o.name = "interface of " + player.name
		o.army = []
		for card in player.army_before_resolution:
			card_interface = Card_interface(card)
			card_interface.owner = o
			o.army.append(card_interface)

	def encode_json(o):
		return {
			"id" : id(o),
			"name" : o.name,
			"army" : [i_card.encode_json() for i_card in o.army]
			}

	def __str__(o):
		return o.__repr__()

	def __repr__(o):
		str = o.name + ' : '
		for card in o.army:
			str += card.__str__()
		return str

	def get_army_without_ghost(o):
		army_without_ghost = []
		for card in o.army:
			if not card.ghost:
				army_without_ghost.append(card)
		return army_without_ghost
