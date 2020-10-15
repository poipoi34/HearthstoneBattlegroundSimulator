#

import time
import warnings
from inspect import signature
import m_effect

#stocke les listener + gère les events potentiellement
class Event_manager:
	#dictionary of event_type -> list of listener
	def __init__(o, battle_manager = None):
		o.listeners = {	"on_enter_arena":[],		#param = [bottom_player, top_player]
						"before_minion_attack":[],	#param = [attacker,attacked] (obligé, attacked?)
						"on_minion_attack":[],		#param = [attacker,attacked]
						"after_minion_attack":[],	#param = [attacker,attacked]
						"on_divine_shield_lost":[],	#param = [minion]
						"on_minion_death":[],		#param = [minion,(killer?,type of death?)]
						"after_minion_death":[],	#param = [minion,(killer?,type of death,owner?)]
						"after_summon":[],			#param = [minion]
						"on_board_update":[],		#param = []
						"end_of_battle":[]			#param = []
			}
		o.battle_manager = battle_manager
		o.action_buffer = []


	def add_listener(o, listener):
		for event_type in listener.triggers:
			if event_type not in o.listeners:
				o.listeners[event_type] = []
			o.listeners[event_type].append(listener)

	def add_listeners(o, listeners):
		for listener in listeners:
			o.add_listener(listener)

	def buffer(o, action):
		if effect.priorised == True:
			o.action_buffer[event.type].insert(0, action)
		else : o.action_buffer[event.type].append(action)

		

	def release_buffer(o):
		for action in o.action_buffer:
			action()

	def spread_event(o, event_type, param = {}):
		Event(event_type, param).spread(o)



class Event:

	def __init__(o,type = "", param = {}, event_manager = None):
		o.type = type
		#o.listener_list = []
		o.param = param
		o.event_manager = event_manager


		
	
	#buffers effects
	def spread(o, event_manager = None):
		if event_manager == None:
			if o.event_manager == None:
				raise Exception("No event_manager defined for event : " + o.type)
			else: event_manager = o.event_manager

		for listener in event_manager.listeners[o.type]:
			for action in listener.triggers[o.type]:
				action.event = o
				if action.instant:
					action()
				else : event_manager.buffer(action)
			
		time.sleep(0.0)
		if o.type != "on_board_update" and event_manager.battle_manager != None and event_manager.battle_manager.displayer != None:
			event_manager.battle_manager.save_board_state(o)
			Event("on_board_update", {"battle_manager" : event_manager.battle_manager}).spread(event_manager)
		time.sleep(0.0)

		
	def __repr__(o):
		return o.type

	def __str__(o):
		return "event " + o.type + " with param : " + str(o.param)
	


class Action:
	def __init__(o, listener, event_callable, event = None, instant = True, priorised = False):
		o.event = event
		o.listener = listener
		o.event_callable = event_callable
		o.instant = instant
		o.priorised = priorised

	def __call__(o):
		#polymorphik_call(o, o.listener, event.param)
		a = o.event_callable
		a(o.listener, o.event.param)

# interface listener - implements trigger dictionnary event_type -> list of Trigger
class Listener:
	def __init__(o, event_manager = None):
		o.triggers = {}
		o.event_manager = event_manager

	def listen_to(o, event_type, callable, instant = True, priorised = False):
		if event_type not in o.triggers:
			o.triggers[event_type] = []

		o.triggers[event_type].append(Action(o, callable, priorised = priorised, instant = instant))

		if o.event_manager != None:
			o.event_manager.add_listener(o)

def polymorphik_call(callable, listener, param_event):
	###un peu de bidouillage
	
	inspect_callable_args = signature(callable).parameters
			
	if len(inspect_callable_args) == 1:#si le trigger a 1 argument
		if 'param' in inspect_callable_args:#si param est l'argument
			callable(param_event)
		else : callable(listener)#sinon on suppose que le trigger a besoin du listener (?)
	elif len(inspect_callable_args) == 2:
		callable(listener, param_event)#on suppose que les args sont dans le bon ordre...
	else : callable()
	###fin bidouillage