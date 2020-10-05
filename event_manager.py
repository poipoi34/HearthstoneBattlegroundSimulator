import time
import warnings


#dictionary of event_type -> list of listener
listeners = {	"on_enter_arena":[],			#[]
				"on_minion_attack":[],		#[attacker,attacked]
				"after_minion_attack":[],	#[attacker,attacked]
				"on_divine_shield_lost":[],	#[minion]
				"on_minion_death":[],		#[minion,(killer?,type of death?)]
				"after_minion_death":[],	#[minion,(killer?,type of death,owner?)]
				"after_summon":[],
				"on_board_update":[]
	}
battle_manager = None

class Event:

	
	def __init__(o,type = "", param = {}):
		o.type = type
		#o.listener_list = []
		o.param = param
		if o.type not in listeners:
			listeners[o.type] = []
	

	def fire(o):
		if o.type != "on_board_update" and battle_manager != None and battle_manager.displayer != None:
			battle_manager.save_board_state(o)
			Event("on_board_update", {"battle_manager" : battle_manager}).fire()
			

		for listener in listeners[o.type]:
			listener.trigger[o.type](o.param)
		time.sleep(0.1)

		
	def __repr__(o):
		return o.type

	def __str__(o):
		return "event " + o.type + " with param : " + str(o.param)
	
def add_listener(listener, event_type, effect):
	#o.listener_list.append(listener)
	if event_type not in listeners:
		warnings.warn(event_type + " not declared")
		return
	listeners[event_type].append(listener)
	listener.trigger[event_type] = effect




# interface listener - implements trigger dictionnary event_name -> (list of ?)subroutine to execute
class Event_listener:
	def __init__(o):
		o.trigger = {}



def find_event(event_type):
	if not event_type in Event.listeners:
		warnings.warn("no event named " + event_type)
		return None
	return Event.listeners[event_type]


event1 = Event("enter arena")
