class Deathrattle:
	def __init__(o, owner, effect_list):
		o.owner = owner
		o.deathrattles = effect_list


	def executeAll(o):
		for effect in o.deathrattles:
			effect()


	
	


