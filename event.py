import time

class Event:
	event_subscriber = {"enter arena":[],			#[]
						"on minion attack":[],		#[attacker,attacked]
						"after minion attack":[],	#[attacker,attacked]
						"divine shield lost":[],	#[minion]
						"on minion death":[],		#[minion,(killer?,type of death?)]
						"after minion death":[],	#[minion,(killer?,type of death,owner?)]

		}

	def __init__(s,name = "",param = []):
		s.name = name
		s.param = param[:]

class Observer:
	def __init__(o):
		o.trigger = {}


def add_subscriber(observer, event_name, effect):
	if not event_name in Event.event_subscriber:
		Event.event_subscriber[event_name] = [] 
	Event.event_subscriber[event_name].append(observer)
	observer.trigger[event_name] = effect

def create_event(event):
	if not event.name in Event.event_subscriber:
		Event.event_subscriber[event.name] = []
	for sub in Event.event_subscriber[event.name]:
		sub.trigger[event.name](event)
	time.sleep(0.5)
	
	
