from time import time
from m_Card_image import Card_image
import math

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
	
	def __init__(o, displayer):
		o.chrono = Chrono()
		o.frame_time = 0.016
		o.displayer = displayer
		o.chrono_started = False
		o.time_dependant = True
		o.current_frame = 0
		o.last_frame = 1
		o.object_to_animate = []

	def update(o):
		finished,changed = False,False
		if o.chrono_started == False:
			o.chrono.start()
			o.chrono_started = True
			o.update_animation()
			changed = True
		if not o.time_dependant:
			frame_to_jump = chrono.elapsed_time() // o.frame_time
			if frame_to_jump != 0:
				o.current_frame = min(o.current_frame + frame_to_jump,o.last_frame)
				o.rewind(frame_to_jump * o.frame_time)
				o.update_animation()
				changed = True
		if o.time_dependant:
			if (o.chrono.elapsed_time() >= o.frame_time):
				o.current_frame = min(o.current_frame + 1,o.last_frame)
				o.chrono.start()
				o.update_animation()
				changed = True
		if (o.current_frame >= o.last_frame):
			finished = True
		else: finished = False
		return finished,changed

	def place_card(o,card_image, board_state,p_in_army = None):#place card using card place using board_state or p_in_army
		px,py = 0,0
		if (card_image.owner == o.displayer.top_player):
			py = o.displayer.win[1]*1/4
		elif(card_image.owner == o.displayer.bot_player):
			py = o.displayer.win[1]*2/4
		else:
			raise Exception("some card_image doesn't have an owner")
		if p_in_army == None:
			p_in_army = card_image.get_pos_in_army(board_state)# <- definitely need board_state as parameter contrary to place_card()
		px = o.displayer.win[0]/5 + 3*o.displayer.win[0]/5*p_in_army/len(card_image.owner.army_before_resolution)
		card_image.pos = [px,py]


class on_enter_arena(Animation):

	def __init__(o,displayer,board_state):
		Animation.__init__(o,displayer)
		displayer.event = board_state.event # ? à quoi ça sert?

		displayer.bot_player = board_state.player1
		displayer.top_player = board_state.player2

		o.board_state = board_state

		o.last_frame = 60
			
		i = 0
		for card in displayer.bot_player.army_before_resolution:
			if not card.ghost:
				card_image = Card_image(card)
				displayer.card_to_draw[id(card)] = card_image
				o.object_to_animate.append(card_image)
				card_image.pos_in_army = i
				card_image.owner = board_state.player1
				card_image.scale = 0
				o.place_card(card_image,None,i)
				i += 1

		i = 0
		for card in displayer.top_player.army_before_resolution:
			if not card.ghost:
				card_image = Card_image(card)
				displayer.card_to_draw[id(card)] = card_image
				o.object_to_animate.append(card_image)
				card_image.pos_in_army = i
				card_image.owner = board_state.player2
				card_image.scale = 0
				o.place_card(card_image,None,i)
				i += 1

	def update_animation(o):

		if o.current_frame >= o.last_frame:
			for id_card in o.displayer.card_to_draw:
				card = o.displayer.card_to_draw[id_card]
				card.rotation = 0
				card.scale = 1

		if o.current_frame >= 0:
			for id_card in o.displayer.card_to_draw:
				card = o.displayer.card_to_draw[id_card]
				card.scale = o.current_frame/o.last_frame
				card.rotation = 360 * o.current_frame/o.last_frame

class refresh_board_state(Animation):# le but de cette animation est de dessiner le board state, en ignorant l'event

	def __init__(o,displayer,board_state):
		Animation.__init__(o,displayer)
		o.last_frame = 30
		o.board_state = board_state
		o.displayer.bot_player = board_state.player1
		o.displayer.top_player = board_state.player2
		displayer.card_to_draw = {}
		i = 0
		for card in board_state.player1.army_before_resolution:
			if not card.ghost:
				card_image = Card_image(card)
				displayer.card_to_draw[id(card)] = card_image
				o.object_to_animate.append(card_image)
				card_image.pos_in_army = i
				card_image.owner = board_state.player1
				o.place_card(card_image,None,i)
				i += 1

		i = 0
		for card in board_state.player2.army_before_resolution:
			if not card.ghost:
				card_image = Card_image(card)
				displayer.card_to_draw[id(card)] = card_image
				o.object_to_animate.append(card_image)
				card_image.pos_in_army = i
				card_image.owner = board_state.player2
				o.place_card(card_image,None,i)
				i += 1
		t=0


	def update_animation(o):
		pass

#class on_minion_attack(Animation):
