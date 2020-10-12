import pygame as pg
import copy
import time
from m_event import Listener
from m_deathrattle import Deathrattle
from m_effect import Effect
import m_effect
import m_buff

class Card(Listener):
	
	####methods
	def __init__(o,attack = 0,health = 1,*,name = "", battle_manager = None,taunt = False, divineShield = None):
		
		Listener.__init__(o)
		o.name = name
		
		###combat attributes
		o.attack = attack
		o.health = health
		o.max_attack = attack
		o.max_health = health
		o.can_attack = True
		o.divineShield= False
		o.deathrattle_list = []
		o.buff_list = []
		o.ghost = False

		o.taunt = taunt
		
		###display attributes
		o.image = []

		###debug attributes
		o.name = name

		###others
		o.owner = None

		o.pos = -1

		###references
		
		o.battle_manager = None


	### combat methods
	def fight(o,card):
		#print(s.name, " attacked ",card.name) 
		o.get_event_manager().spread_event("on_minion_attack", {"source_minion" : o, "target_minion" : card})
		o.take_damage(card.attack)
		card.take_damage(o.attack)
		o.get_event_manager().spread_event("after_minion_attack", {"source_minion" : o, "target_minion" : card})

		if (o.health <= 0):
			o.die()
		if (card.health <= 0):
			card.die()
		o.can_attack = False
	
	
		
	def take_damage(o, damage):
		if not o.ghost:
			if (o.divineShield and damage > 0):
				o.divineShield = False
				o.battle_manager.event_manager.fire_one_shot_event("on_divine_shield_lost", {"source_minion" : o})
				return
			o.health-=damage

	def die(o):
		o.get_event_manager().spread_event("on_minion_death", {"source_minion" : o})
		if (o.health <= 0):
			o.ghost = True
		if (o.deathrattle_list != []):
			o.battle_manager.deathrattle_buffer += o.deathrattle_list
		o.owner.army.remove(o)
		o.get_event_manager().fire_one_shot_event("after_minion_death", {"source_minion" : o})
		
	
	def set_battle_manager(o, battle_manager):
		o.battle_manager = battle_manager
		for deathrattle in o.deathrattle_list:
			deathrattle.set_battle_manager(battle_manager)

	def get_event_manager(o):
		return o.battle_manager.event_manager

	def __str__(o):
		return "[" + o.name + "/" + str(o.attack) + "/" + str(o.health) + "]"
	###display methods
	

	def get_position(o,displayer):#where you should draw it
		if o.ghost == True:
			return
		if displayer.display_mode == "arena":
			mZone_length = 3*displayer.win[0]/5
			o.owner.update_minion_pos()
			p_in_army = o.pos
			px = displayer.win[0]/5 + 3*displayer.win[0]/5*p_in_army/o.owner.count_minion_alive()
			py = 0
			if o.owner == displayer.top_player:
				py = displayer.win[1]*1/4
			if o.owner == displayer.bot_player:
				py = displayer.win[1]*2/4
		return [px,py]
				
	def get_center(o,displayer):
		if o.ghost == True:
			return
		[px,py] = o.get_position(displayer)
		return [px+25,py+50]

	def __repr__(o):
		return o.__str__() + str(id(o))

	def get_player(o):
		return o.owner
	
	def buff(o, attack_bonus, health_bonus, name = "unnamed"):
		o.attack += attack_bonus
		o.health += health_bonus
		o.buff_list.append(Buff(attack_bonus, health_bonus, name))
	

	#prend en param un effet et resout toutes les refs
	def add_deathrattle(o, effect, param = {}):
		deathrattle = Deathrattle(effect, owner = o, battle_manager = o.battle_manager, param = param)
		if (isinstance(effect, Effect)):
			effect.source = deathrattle
		o.deathrattle_list.append(deathrattle)

	
		
	
	
	



class Bolvar(Card):
	def __init__(o):
		Card.__init__(o, 1, 7, name='Bolvar')
		o.divineShield = True

	
		o.listen_to("on_divine_shield_lost", lambda o,p : o.buff(2,0))


class Roi_des_rats(Card):
	def __init__(o):
		Card.__init__(o, 3, 2, name = 'roi des rats')
		effect = m_effect.E_summon(lambda : Rat(), lambda o : 10, at = o)
		
		o.add_deathrattle(effect)
		o.add_deathrattle(lambda o : o.buff(0,2))
		
		#o.listen_to("on_minion_attack", lambda param : param["source_minion"].buff(0,2))
		#o.listen_to("on_minion_attack", lambda param : param["target_minion"].buff(0,2))
		o.listen_to("on_minion_death", lambda o,param : param["source_minion"].buff(2,2))
	 
	def buff2(o):
		o.buff(2,0)
	

	def set_summon_number(o, param):
		param["effect"].k = o.attack


class Rat(Card):
	def __init__(o):
		Card.__init__(o,1,1,name = 'rat')

class Ghoul(Card):
	def __init__(o):
		Card.__init__(o, 2, 1, name = 'Ghoul')
		o.add_deathrattle(Deathrattle(effect_type.deal_aoe_damage(1)))

class Scallywag(Card):
	def __init__(o):
		Card.__init__(o, 2, 1, name = 'Scallywag')
		o.add_deathrattle(m_effect.E_summon(Pirate()))

class Pirate(Card):
	def __init__(o):
		Card.__init__(o, 1, 1, name = 'Pirate')
		o.listen_to("after_summon", lambda o, param : o.owner.command_attack(o) if param["summoned_minion"] == o else None, priorised = True)

	

