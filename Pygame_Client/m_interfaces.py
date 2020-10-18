import time

class Card_interface:
	def __init__(o, json_dict, env):
		o.attack = json_dict["attack"]
		o.health = json_dict["health"]
		o.max_attack = json_dict["max_attack"]
		o.max_health = json_dict["max_health"]
		o.divine_shield= json_dict["divine_shield"]
		#o.deathrattle_list = [Deathrattle_interface(deathrattle) for deathrattle in json_dict["deathrattle"]]
		#o.buff_list = [Card_interface(card) for card in json_dict["army"]]
		o.ghost = json_dict["ghost"]

		o.taunt = json_dict["taunt"]

		o.name = json_dict["name"]

		o.owner = json_dict["owner"] #

		o.id = json_dict["id"]
		if (o.id not in env):
			env[o.id] = o

	def __str__(o):
		return "["+ o.name + "/" + str(o.attack) + "/" + str(o.health) + "/" + id_to_str(o.id) + "]"

	def __repr__(o):
		return o.__str__()
		

class Player_interface:
	def __init__(o, json_dict, env):
		o.id = json_dict["id"]
		o.name = json_dict["name"]
		o.army = [Card_interface(card, env) for card in json_dict["army"]]
		for card in o.army:
			card.owner = o
		if o.id not in env:
			env[o.id] = o

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



class Event_interface:
	def __init__(o, json_dict, env):
		o.id = json_dict["id"]
		o.type = json_dict["type"]
		o.param = json_dict["param"]
		

	def __repr__(o):
		return o.__str__()
	def __str__(o):
		param_str = {}
		for ref in o.param:
			if o.param[ref] > 10000:#if id...
				param_str[ref] = id_to_str(o.param[ref])
			
		return "event " + o.type + " with param : " + str(param_str)

class Board_interface:
	def __init__(o, json_dict, env):
		o.id = json_dict["id"]
		o.bottom_player = Player_interface(json_dict["bottom_player"], env)
		o.top_player = Player_interface(json_dict["top_player"], env)
		o.event = Event_interface(json_dict["event"], env)

	def __str__(o):
		return "\n-> event : " + o.event.__str__() + "\n|||Board state ::" + o.bottom_player.__str__() + " | " + o.top_player.__str__() + "\n";
	def __repr__(o):
		return o.__str__()


def id_to_str(id):
	res = str(hex(id))
	return '@' + res[len(res)-5:len(res)]

