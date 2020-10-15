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

class Player_interface:
	def __init__(o, player):
		o.name = "interface of " + player.name
		o.army = []
		for card in player.army_before_resolution:
			card_interface = Card_interface(card)
			card_interface.owner = o
			o.army.append(card_interface)
