import math
from vector_math import *
import pygame

class Drawable():
	def __init__(o,image = None):
		o.__draw_pos = Vector([0,0])
		o.pos = Vector([0,0]) #center
		o.image = []
		o.transformed_image = [] # after rotation + scale
		#storing both image and transformed_image because transform of pygame change quality of image
		o.rotation = 0
		o.scale = 0

	def get_draw_pos(o):
		a = Vector(o.transformed_image.get_size())
		b = 0

		return o.pos - 0.5*Vector(o.transformed_image.get_size())



class Card_image(Drawable):
		
	colorkey = [123,21,51]

	def __init__(o, card_interface, displayer = None):
		Drawable.__init__(o)
		o.data = card_interface
		
		o.image = []#potentialy store image data, for now get_image() always calculate it
		o.displayer = displayer

		o.pos = [0,0] #pixel pos of center
		o.draw_pos = [0,0] #weird thing just to draw the rotated surf at good position
		o.card_size = [75,150] #width,height
		o.scale = 1
		o.rotation = 0

		o.divine_shield_surf = None

	def get_pos_in_army(o, battle_data):
		i = 0
		for card_from_game in battle_data.bottom_player.army:
			if o.data.id == card_from_game.id:
				return i
			if card_from_game.ghost == False:
				i += 1
		i = 0
		for card_from_game in battle_data.top_player.army:
			if o.data.id == card_from_game.id:
				return i
			if card_from_game.ghost == False:
				i += 1
		raise Exception("didn't find the card in army")

	def get_image(o): #create and return an image
		
		s = o.scale

		#o.image = pygame.Surface([int(o.card.size[0]*s), int(o.card.size[1]*s) ])
		o.image = pygame.Surface(o.card_size)
		o.image.fill([130,100,255])
		o.image.set_colorkey(o.colorkey)
		font = pygame.font.Font('freesansbold.ttf', 20)
		attack_text = font.render(str(o.data.attack), True, [0,255,0])
		h_color = [0,255,0]
		if (o.data.health < o.data.max_health):
			h_color = [255,0,0]
		health_text = font.render(str(o.data.health), True, h_color)

		att_surface = attack_text.get_rect()
		hlth_surface = health_text.get_rect()

		blitPosA = [0, o.card_size[1] - att_surface[3]]
		blitPosH = [o.card_size[0] - hlth_surface[2], o.card_size[1] - hlth_surface[3]]

		o.image.blit(attack_text,blitPosA)
		o.image.blit(health_text,blitPosH)

		o.transformed_image = o.image #should copy
		if (o.data.divine_shield):
			if (o.divine_shield_surf == None):
				card_width,card_height = o.card_size[0],o.card_size[1]
				o.divine_shield_margin = 5
				o.divine_shield_surf = pygame.Surface([card_width + o.divine_shield_margin*2, card_height + o.divine_shield_margin*2])
				o.divine_shield_surf.fill([255, 255, 0])
				o.divine_shield_surf.set_colorkey(o.colorkey)
				o.divine_shield_surf.set_alpha(128)
			o.divine_shield_surf.blit(o.image,[o.divine_shield_margin, o.divine_shield_margin])
			o.transformed_image = o.divine_shield_surf #should copy


		o.transformed_image = o.rotate(o.scaled(o.transformed_image,o.scale),o.rotation,o.pos)
		return o.transformed_image



	def rotate(o, angle):# you can also set the rotation directly throught attribut rotation
		o.rotation += angle

	def draw(o,displayer):
		displayer.screen.blit(o.get_image(),o.draw_pos)




	def scaled(o,surf,scale):
		dim = surf.get_size()
		dim = [int(dim[0]*scale),int(dim[1]*scale)]
		return pygame.transform.smoothscale(surf,dim)

	def rotate(o,surf,angle,pos):#rotate a surface and return the shift to apply (translation) to make the turn centered at center of surface
		size = surf.get_size()[:]
		return pygame.transform.rotate(surf,angle)







