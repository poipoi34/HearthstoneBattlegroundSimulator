import pygame as pg
import time
import event
import deathrattle

class Card:
	
	####methods
	def __init__(o,attack = 0,health = 1,*,name = ""):
		#event.add_subscriber(s)

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


	### combat methods
	def fight(o,card):
		#print(s.name, " attacked ",card.name) 
		event.on_minion_attack.fire({"source_minion" : o, "target_minion" : card})
		o.take_damage(card)
		card.take_damage(o)
		if (o.health <= 0):
			o.die()
		if (card.health <= 0):
			card.die()
		o.can_attack = False
		event.after_minion_attack.fire({"source_minion" : o, "target_minion" : card})
		
	def take_damage(o, card):
		if (o.divineShield and card.attack > 0):
			o.divineShield = False
			event.on_divine_shield_lost.fire({"source_minion" : o})
			return
		o.health-=card.attack

	def die(o):
		event.on_minion_death.fire({"source_minion" : o})
		o.ghost = True
		if (o.deathrattle_holder != None):
			o.game_manager.deathrattle_buffer.append(o.deathrattle_holder)
		o.owner.army.remove(o)
		event.after_minion_death.fire({"source_minion" : o})
		
	
	def set_game_manager(o, game_manager):
		o.game_manager = game_manager

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





class Bolvar(Card, event.Event_listener):
	def __init__(o):
		Card.__init__(o, 1, 7, name='Bolvar')
		event.Event_listener.__init__(o)

		o.divineShield = True
		def effect(event, param):
			if (param["source_minion"].owner == o.owner):
				o.attack+=2
				
		
		event.find_event("divine shield lost").add_listener(o, effect)


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




	




		








		
