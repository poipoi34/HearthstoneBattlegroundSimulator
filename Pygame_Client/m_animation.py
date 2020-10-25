from time import time
from m_object import *
import math
from vector_math import *



class Chrono:
	def __init__(o):
		o.elasped_time = None
		o.start_time = None

	def start(o):
		o.start_time = time()

	def elapsed_time(o):
		return time() - o.start_time

	def stop():
		o.elapsed_time = time() - o.start_time

	def resume():
		o.start_time = time() - o.elapsed_time #restart on time en ajoutant le elapsed deja elapsé

	def rewind(ms):
		o.start_time - ms


#une animation est lié à une liste de animated_object et s'occupe de les bouger
#la class Animation est abstraite
class Animation:
	stopping = True
	def get_length(board_state):
		return 1
	def get_id_used (board_state):#static method giving the id of game_object moved, should be overwritten in Animation childs
		return []

	def __init__(o, displayer,board_state = None):
		o.board_state = board_state
		o.displayer = displayer
		o.time_dependant = True
		o.object_to_animate = []
		o.started = False
		o.current_frame = 0
		o.last_frame = type(o).get_length(board_state)
		o.displayer = displayer
		o.board_state = board_state


	def update(o,frame_to_jump = 1):
		finished = False

		"""
		if frame_to_jump > 0:
			o.current_frame += frame_to_jump
			o.update_animation()
		if (o.current_frame >= o.last_frame):
			finished = True
		else: finished = False
		return finished
		"""
		if frame_to_jump > 0:
			o.current_frame += frame_to_jump
			if (o.current_frame >= o.last_frame):
				finished = True
			o.update_animation()
		else: finished = False
		return finished
		

	def place_card(o,card_image, board_state,p_in_army = None):#place card using card place in army using board_state or p_in_army
		card_image.pos = o.get_card_placement(card_image,board_state,p_in_army)
	
	def get_card_placement(o,card_image,board_state,p_in_army = None):
		px,py = 0,0
		m = o.displayer.win[0]
		n_cards = len(card_image.owner.get_army_without_ghost())
		if p_in_army == None:
			p_in_army = card_image.get_pos_in_army(board_state)# <- definitely need board_state as parameter contrary to place_card()
		c = Card_image.card_size[0] + 10
		k = 7 #number of cards in a row

		if (card_image.owner == o.displayer.top_player):
			if n_cards <= k:
				py = o.displayer.win[1]*(1/4+1/8)
			elif n_cards > k:
				py = o.displayer.win[1]*(1/4+(1+p_in_army//k)*1/12)
		elif(card_image.owner == o.displayer.bot_player):
			if n_cards <= k:
				py = o.displayer.win[1]*(2/4+1/8)
			elif n_cards > k:
				py = o.displayer.win[1]*(2/4+(1+p_in_army//k)*1/12)
		else:
			raise Exception("some card_image doesn't have an owner")	
		
		s = n_cards%k if p_in_army//k == n_cards//k else k
		px = m/2 - c*(s-1)/2 + (p_in_army%k)*c
		#px = m/5 + 3*m/5*((p_in_army+1)/(n_cards+1))
		return Vector(px,py)

	def refresh(o,player):
		i = 0
		for card in player.army:
			if not card.ghost:
				card_image = Card_image(card)
				o.displayer.game_object[card.id] = card_image
				o.object_to_animate.append(card_image)
				card_image.pos_in_army = i
				card_image.owner = player
				o.place_card(card_image,None,i)
				i += 1

class on_enter_arena(Animation):
	stopping = True
	def get_length(board_state):
		return 60
	def get_id_used (board_state):#static method giving the id of game_object moved
		id_used = []
		for card_interface in board_state.bottom_player.army:
			id_used.append(card_interface.id)
		for card_interface in board_state.top_player.army:
			id_used.append(card_interface.id)
		return id_used
		
	def __init__(o,displayer,board_state):
		Animation.__init__(o,displayer,board_state)

		displayer.event = board_state.event # ? à quoi ça sert?
		displayer.bot_player = board_state.bottom_player
		displayer.top_player = board_state.top_player

		
			
		o.refresh(board_state.bottom_player)
		o.refresh(board_state.top_player)


	def update_animation(o):

		if o.current_frame <= o.last_frame//2:
			for id_card in o.displayer.game_object:
				card = o.displayer.game_object[id_card]
				card.rotation = 360 * o.current_frame/(o.last_frame//2)

		if o.current_frame > o.last_frame//2:
			for id_card in o.displayer.game_object:
				card = o.displayer.game_object[id_card]
				card.rotation = 0

		t = o.current_frame/o.last_frame
		for id_card in o.displayer.game_object:
			card = o.displayer.game_object[id_card]
			card.scale = -2*t*t+3*t

class refresh_board_state(Animation):# le but de cette animation est de dessiner le board state, en ignorant l'event
	stopping = True
	def get_length(board_state):
		return 10
	def get_id_used (board_state):#static method giving the id of game_object moved
		id_used = []
		for card_interface in board_state.bottom_player.army:
			id_used.append(card_interface.id)
		for card_interface in board_state.top_player.army:
			id_used.append(card_interface.id)
		return id_used

	def __init__(o,displayer,board_state):
		Animation.__init__(o,displayer,board_state)
		

		o.displayer.bot_player = o.board_state.bottom_player
		o.displayer.top_player = o.board_state.top_player
		displayer.game_object = {}
		
		o.refresh(board_state.bottom_player)
		o.refresh(board_state.top_player)


	def update_animation(o):
		pass

class before_minion_attack(Animation):
	stopping = True
	def get_length(board_state):
		return 30

	def get_id_used (board_state):#static method giving the id of game_object moved
		return [board_state.event.param["source_minion"]]

	def __init__(o,displayer,board_state):
		Animation.__init__(o,displayer,board_state)

		o.object_to_animate.append(displayer.game_object[board_state.event.param["source_minion"]])
		

	def update_animation(o):
		k=0
		o.displayer.game_object[o.board_state.event.param["source_minion"]].scale = 1 + o.current_frame/o.last_frame*0.3

class on_minion_attack(Animation):
	stopping = True
	def get_length(board_state):
		return 30
	def get_id_used (board_state):#static method giving the id of game_object moved
		return [board_state.event.param["source_minion"],board_state.event.param["target_minion"]]

	def __init__(o,displayer,board_state):
		Animation.__init__(o,displayer,board_state)
		

		o.object_to_animate.append(displayer.game_object[board_state.event.param["source_minion"]])
		o.object_to_animate.append(displayer.game_object[board_state.event.param["target_minion"]])

		source_minion = o.object_to_animate[0]
		target_minion = o.object_to_animate[1]
		o.u = source_minion.pos

	def update_animation(o):
		t = o.current_frame/o.last_frame
		#f(0) = 0, f(1) = 3/4 et f(t) = at² - t
		#a = 7/4
		#p(t) = (1-f(t))*u + f(t)*v avec u = o.u et v = o.object_to_animate[1].pos
		o.displayer.game_object[o.board_state.event.param["source_minion"]].pos = (1-7/4*t*t+t)*o.u + (7/4*t*t-t)*o.object_to_animate[1].pos

class after_minion_attack(Animation):
	stopping = True
	def get_length(board_state):
		return 30

	def get_id_used (board_state):#static method giving the id of game_object moved
		return [board_state.event.param["source_minion"],board_state.event.param["target_minion"]]

	def __init__(o,displayer,board_state):
		Animation.__init__(o,displayer,board_state)
		

		attacker_id = board_state.event.param["source_minion"]
		attacked_id = board_state.event.param["target_minion"]
		o.attacker_image = displayer.game_object[attacker_id]
		o.target_image = displayer.game_object[attacked_id]

		o.object_to_animate = [o.attacker_image,o.target_image]
		o.back_pos = o.get_card_placement(o.attacker_image,board_state)
		o.starting_pos = o.attacker_image.pos

		o.initial_target_pos = o.target_image.pos

	def update_animation(o):
		t = o.current_frame/o.last_frame
		#pos(t) = t*v + (1-t)*u où u = starting pos et v = ending pos
		u = o.starting_pos
		v = o.back_pos
		o.attacker_image.pos = t*v + (1-t)*u
		t = o.current_frame/o.last_frame
		o.displayer.game_object[o.board_state.event.param["target_minion"]].pos = o.initial_target_pos + (5*math.cos(6*math.pi*t),0)
		
class on_take_damage(Animation):
	stopping = False
	def get_length(board_state):
		return 20

	def get_id_used (board_state):#static method giving the id of game_object moved
		return [board_state.event.param["target_minion"]]

	def __init__(o,displayer,board_state,r=20):
		Animation.__init__(o,displayer,board_state)

		o.bubble_damage = Bubble_damage(board_state.event.param["damage"])
		target_minion = displayer.game_object[board_state.event.param["target_minion"]]

		o.bubble_damage.pos = target_minion.pos
		
		displayer.displayer_object.append(o.bubble_damage)

	def update_animation(o):
		if o.current_frame >= o.last_frame:
			o.displayer.displayer_object.remove(o.bubble_damage)



#création d'une animation: 

"""
class my_anim(Animation):
	stopping = True
	def get_length(board_state):
		return 30
	def get_id_used (board_state):#static method giving the id of game_object moved
		
	def __init__(o,displayer,board_state):
		Animation.__init__(o,displayer,board_state)

	def update_animation(o):
"""




class Event_animation_correspondance:
	dict= {"on_enter_arena" : on_enter_arena,
								  "before_minion_attack" : before_minion_attack,
								  "on_minion_attack" : on_minion_attack,
								  "after_minion_attack" : after_minion_attack,
								  "on_take_damage" : on_take_damage,
								  }
	def __getitem__(o,key):
		if key in o.dict:
			return o.dict[key]
		else:
			return refresh_board_state

event_animation_correspondance = Event_animation_correspondance()

