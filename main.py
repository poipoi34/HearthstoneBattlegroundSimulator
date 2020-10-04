
import pygame as pg
from math import cos,sin,pi,sqrt
import time
from random import*
from card import*
from sys import exit
from basic_bg import*
import event
import displayer


voidWalker = Card(1,3,name = "void walker")
voidWalker.divineShield = True
brann = Card(2,4,name = "brann")
baron = Card(1,7,name = "baron")
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


g_manager = game_manager()



displayer = displayer.Displayer()



print(g_manager.simulate_fight(player1,player2) == player1)

a = True
while (a):
	for event in pg.event.get():
		if event.type == pg.QUIT:
			displayer.quit()
			a = False


