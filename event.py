import time
import warnings



class Event:
	#dictionary of name of event -> event (useful? -> yes for not creating twice the same event)
	event_dictionary = {}
	battle_manager = None

	def __init__(o,name = ""):
		o.name = name
		o.listener_list = []
		Event.event_dictionary[name] = o
	

	def fire(o, param = {}):
		for listener in o.listener_list:
			listener.trigger[o.name](o, param)
		time.sleep(0.1)

		if o != on_update_displayer and Event.battle_manager != None and Event.battle_manager.displayer != None:
			on_update_displayer.fire()
	
	def add_listener(o, listener, effect):
		o.listener_list.append(listener)
		listener.trigger[o.name] = effect
	

#Creation des events
on_update_displayer =	Event("update displayer")
on_enter_arena =		Event("enter arena")			#[bottom_player, top_player]
on_minion_attack =		Event("on minion attack")		#[attacker,attacked]
after_minion_attack =	Event("after minion attack")	#[attacker,attacked]
on_divine_shield_lost = Event("divine shield lost")		#[minion]
on_minion_death =		Event("on minion death")		#[minion,(killer?,type of death?)]
after_minion_death =	Event("after minion death")		#[minion,(killer?,type of death,owner?)]
after_summon =			Event("after_summon")

# interface listener - implements trigger dictionnary event_name -> (list of ?)subroutine to execute
class Event_listener:
	def __init__(o):
		o.trigger = {}

def find_event(event_name):
	if not event_name in Event.event_dictionary:
		warnings.warn("no event named " + event_name)
		return None
	return Event.event_dictionary[event_name]
