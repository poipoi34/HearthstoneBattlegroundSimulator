class Deathrattle():
	def __init__(o, effect,*, owner = None, battle_manager = None, param = {}):
		o.effect = effect
		o.param = param
		o.owner = owner
		o.battle_manager = battle_manager
		

	def __call__(o):
		o.effect(o.owner)

	def get_player(o):
		return o.owner.owner

	def set_battle_manager(o,battle_manager):
		o.battle_manager = battle_manager