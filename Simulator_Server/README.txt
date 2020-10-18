---Annexe des objets---

Effect (callable) =>	Conteneur g�n�rique d'un callable avec en param�tre la r�f�rence de l'effect o. 
						Des param�tres peuvent �tre d�fini en initialisant des attributs � l'objet effect o. 
						Ces param�tres peuvent �tre ensuite r�cup�r� dans le callable de l'effect (ex : effect.attribut).

Action (callable) =>	Conteneur g�n�rique d'un callable dont les param�tres sont conventionnellement (Listener, event_param)
						Permet de stocker les priorit�s d'appel
						Permet de transformer une fonction/lambda/m�thode en un objet callable
						
Trigger	=>				Couple (event_type, liste d'Action)
						Stock� dans un dictionnaire (liste de couple) du Listener

Event =>				Ev�nement stockable.
						Contient la m�thode spread qui initialise l'event (o) de chaque action de chaque listener 
						�coutant le type de l'event courant (o), et buffer ou execute l'action selon sa priorit�.

Event_manager =>		stock les listener et les buffers.
						release les buffers r�guli�rement.

Listener =>				interface qui associe � chaque type d'event des triggers associ� � ce type d'event
						La class Card impl�mente cette interface.






--- Cr�ation de carte mode d'emploi et conventions ---

construire une card -> construire class h�ritant de Card dont (convention) le nom est le nom de la card
ajouter effet -> cr�er un callable (avec def ou lambda par ex), puis l'associer � un event_type et l'attacher
				 � la card gr�ce � listen_to.
				 /!\ REGLE IMPORTANTE : le callable prend en parametre (listener, param_event) 
										sauf si le polymorphik_call est activ�, auquel cas les param�tres sont optionelles,
										mais param_event doit �tre nomm� param.














