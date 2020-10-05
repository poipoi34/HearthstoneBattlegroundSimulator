
import pygame as pg
from math import cos,sin,pi,sqrt
from player import *
import time
from random import*
from card import*
from sys import exit
from battle_manager import*
import event_manager
import displayer


voidWalker = Card(2,3,name = "void walker")
voidWalker.divineShield = True
brann = Card(2,4,name = "brann")
baron = Card(2,7,name = "baron")
magmaRager = Card(5,1,name = "magma rager")
bolvar1 = Bolvar()
bolvar2 = Bolvar()

cards = [voidWalker,brann,baron,magmaRager, bolvar1, bolvar2]


player1 = player(name = "p1")
player2 = player(name = "p2")

player1.add_to_army(voidWalker)
player1.add_to_army(baron).add_to_army(bolvar2)

player2.add_to_army(brann)
player2.add_to_army(magmaRager).add_to_army(Roi_des_rats()).add_to_army(bolvar1)


battle = battle_manager(player1, player2)



displayer = displayer.Displayer(battle)

battle.attach_displayer(displayer)
event_manager.battle_manager = battle

winner = battle.simulate_battle()
if winner != None:
	print("winner is : " + str(winner))
else: print("draw")




a = True
while (a):
	for event in pg.event.get():
		if event.type == pg.QUIT:
			displayer.quit()
			a = False


