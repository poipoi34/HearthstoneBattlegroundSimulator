import time
import warnings

#stocke les listener + gère les events potentiellement
class Event_manager:
	#dictionary of event_type -> list of listener
	def __init__(o, battle_manager = None):
		o.listeners = {	"on_enter_arena":[],		#[]
						"on_minion_attack":[],		#[attacker,attacked]
						"after_minion_attack":[],	#[attacker,attacked]
						"on_divine_shield_lost":[],	#[minion]
						"on_minion_death":[],		#[minion,(killer?,type of death?)]
						"after_minion_death":[],	#[minion,(killer?,type of death,owner?)]
						"after_summon":[],
						"on_board_update":[]
			}
		o.battle_manager = battle_manager
		o.event_buffer = []

	def add_listener(o, listener):
		for event_type in listener.trigger:
			o.listeners

	def buffer_new_event(o, event_type, param = {}):
		event = Event(event_type, param, o)
		o.add_event(event)
		return event
		
	def buffer_event(o, event):
		o.event_buffer.append(event)

	def release_buffer(o):
		for event in o.event_buffer:
			event.fire()
		o.event_buffer = []

	def fire_one_shot_event(o, event_type, param = {}):
		Event(event_type, param, o).fire()


class Event:

	def __init__(o,type = "", param = {}, event_manager = None):
		o.type = type
		#o.listener_list = []
		o.param = param
		o.event_manager = event_manager


		
	
	#event_manager stores listeners
	def fire(o, event_manager = o.event_manager):
		if event_manager == None:
			raise ValueError("No event_manager defined for event : " + o.type)

		if o.type != "on_board_update" and battle_manager != None and battle_manager.displayer != None:
			battle_manager.save_board_state(o)
			Event("on_board_update", {"battle_manager" : battle_manager}).fire()
			

		for listener in o.event_manager.listeners[o.type]:
			listener.trigger[o.type](o.param)
		time.sleep(0.1)

		
	def __repr__(o):
		return o.type

	def __str__(o):
		return "event " + o.type + " with param : " + str(o.param)
	





# interface listener - implements trigger dictionnary event_name -> (list of ?)subroutine to execute
class Listener:
	def __init__(o, event_manager = None):
		o.trigger = {}
		o.event_manager = event_manager

	def listen_to(o, event_type, effect):
		o.trigger[event_type] = effect


