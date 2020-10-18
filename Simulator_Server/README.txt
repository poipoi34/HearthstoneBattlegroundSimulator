---Annexe des objets---

Effect (callable) =>	Conteneur générique d'un callable avec en paramètre la référence de l'effect o. 
						Des paramètres peuvent être défini en initialisant des attributs à l'objet effect o. 
						Ces paramètres peuvent être ensuite récupéré dans le callable de l'effect (ex : effect.attribut).

Action (callable) =>	Conteneur générique d'un callable dont les paramètres sont conventionnellement (Listener, event_param)
						Permet de stocker les priorités d'appel
						Permet de transformer une fonction/lambda/méthode en un objet callable
						
Trigger	=>				Couple (event_type, liste d'Action)
						Stocké dans un dictionnaire (liste de couple) du Listener

Event =>				Evènement stockable.
						Contient la méthode spread qui initialise l'event (o) de chaque action de chaque listener 
						écoutant le type de l'event courant (o), et buffer ou execute l'action selon sa priorité.

Event_manager =>		stock les listener et les buffers.
						release les buffers régulièrement.

Listener =>				interface qui associe à chaque type d'event des triggers associé à ce type d'event
						La class Card implémente cette interface.






--- Création de carte mode d'emploi et conventions ---

construire une card -> construire class héritant de Card dont (convention) le nom est le nom de la card
ajouter effet -> créer un callable (avec def ou lambda par ex), puis l'associer à un event_type et l'attacher
				 à la card grâce à listen_to.
				 /!\ REGLE IMPORTANTE : le callable prend en parametre (listener, param_event) 
										sauf si le polymorphik_call est activé, auquel cas les paramètres sont optionelles,
										mais param_event doit être nommé param.














