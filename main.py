import threading
import pygame as pg
from math import cos,sin,pi,sqrt
from m_player import Player

import time
from random import*
from m_card import *
from sys import exit
from m_battle import battle_manager
import m_event
from m_displayer import Displayer

def pygame_loop():
	while True:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				displayer.quit()
				a = False


voidWalker = Card(2,8,name = "void walker",taunt = True)
voidWalker.divineShield = True
brann = Card(2,4,name = "brann")
baron = Card(2,7,name = "baron")
magmaRager = Card(5,1,name = "magma rager")
bolvar1 = Bolvar()
bolvar2 = Bolvar()

cards = [voidWalker,brann,baron,magmaRager, bolvar1, bolvar2]


player1 = Player(name = "p1")
player2 = Player(name = "p2")

player1.add_to_army(Scallywag()).add_to_army(Scallywag())
#player1.add_to_army(baron).add_to_army(bolvar2)

#player2.add_to_army(brann)
#player2.add_to_army(magmaRager).add_to_army(Roi_des_rats()).add_to_army(bolvar1)
player2.add_to_army(Roi_des_rats()).add_to_army(Roi_des_rats())


battle = battle_manager(player1, player2)
#battle2 = battle_manager(player1, player2)


displayer = Displayer(battle)

battle.attach_displayer(displayer)

#for i in [1,2,3,4,5,6,7,8,9,10]:
#threading.Thread(target = battle.simulate_battle).start()
winner = battle.simulate_battle()
#winner2 = battle2.simulate_battle()
print()
print("battle_data:")
for i in battle.battle_data:
	print(str(i))

displayer.play(battle.battle_data)



#threading.Thread(target = pygame_loop).start()


pygame_loop()
if winner != None:
	print("winner is : " + str(winner))
else: print("draw")








