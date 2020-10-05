import pygame as pg
import copy
import time
import event_manager
import deathrattle

class Card(event_manager.Event_listener):
	
	####methods
	def __init__(o,attack = 0,health = 1,*,name = ""):
		
		event_manager.Event_listener.__init__(o)
		o.name = name
		
		###combat attributes
		o.attack = attack
		o.health = health
		o.max_attack = attack
		o.max_health = health
		o.can_attack = True
		o.divineShield= False
		o.deathrattle_holder = None
		o.ghost = False
		
		###display attributes
		o.image = []

		###debug attributes
		o.name = name

		###others
		o.owner = None

		o.pos = -1


	### combat methods
	def fight(o,card):
		#print(s.name, " attacked ",card.name) 
		event_manager.Event("on_minion_attack", {"source_minion" : o, "target_minion" : card}).fire()
		o.take_damage(card)
		card.take_damage(o)
		if (o.health <= 0):
			o.die()
		if (card.health <= 0):
			card.die()
		o.can_attack = False
		event_manager.Event("after_minion_attack", {"source_minion" : o, "target_minion" : card}).fire()
		
	def take_damage(o, card):
		if (o.divineShield and card.attack > 0):
			o.divineShield = False
			event_manager.Event("on_divine_shield_lost", {"source_minion" : o}).fire()
			return
		o.health-=card.attack

	def die(o):
		event_manager.Event("on_minion_death", {"source_minion" : o}).fire()
		o.ghost = True
		if (o.deathrattle_holder != None):
			o.battle_manager.deathrattle_buffer.append(o.deathrattle_holder)
		o.owner.army.remove(o)
		event_manager.Event("after_minion_death", {"source_minion" : o}).fire()
		
	
	def set_battle_manager(o, battle_manager):
		o.battle_manager = battle_manager

	def __str__(o):
		return "[" + o.name + "/" + str(o.attack) + "/" + str(o.health) + "]"
	###display methods
	

	def get_position(o,displayer):#where you should draw it
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
				
	def get_center(s,displayer):
		[px,py] = s.get_position(displayer)
		return [px+25,py+50]

	def __repr__(o):
		return o.__str__() + str(id(o))





class Bolvar(Card):
	def __init__(o):
		Card.__init__(o, 1, 7, name='Bolvar')
		o.divineShield = True

		def effect( param):
			if (param["source_minion"].owner == o.owner):
				o.attack+=2
				
		
		event_manager.add_listener(o, "on_divine_shield_lost", effect)


class Roi_des_rats(Card):
	def __init__(o):
		Card.__init__(o, 3, 2, name = 'roi des rats')
		o.deathrattle_holder = deathrattle.Deathrattle(o, [o.deathrattle_effect])
	
	def deathrattle_effect(o): #defining deathrattle
		#if (event.param[0] == o):
		for i in range(o.attack):
			o.owner.summon(Rat(),at=o.owner.army_before_resolution.index(o))

class Rat(Card):
	def __init__(o):
		Card.__init__(o,1,1,name = 'rat')




	




		








		
