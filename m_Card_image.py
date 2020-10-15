import pygame

class Card_image:
	

	def __init__(o,card_interface,displayer = None):
		o.copy(card_interface)

		o.image = []#potentialy store image data, for now get_image() always calculate it
		o.displayer = displayer

		o.pos = [0,0] #pixel pos
		o.card_size = [75,150] #width,height
		o.scale = 1
		o.rotation = 0

		o.divine_shield_surf = None

		

	def copy(o,card_interface):
		o.attack = card_interface.attack
		o.health = card_interface.health
		o.max_attack = card_interface.max_attack
		o.max_health = card_interface.max_health

		o.divineShield= card_interface.divineShield
		o.deathrattle_list = card_interface.deathrattle_list[:]
		o.buff_list = card_interface.buff_list[:]
		o.ghost = card_interface.ghost

		o.taunt = card_interface.taunt

		o.name = card_interface.name

		#o.owner = card_interface.owner

		o.id_source = card_interface.id_source


	def get_pos_in_army(o,battle_data):
		i = 0
		for card_from_game in battle_data.player1.army_before_resolution:
			if o.id_source == card_from_game.id_source:
				return i
			if card_from_game.ghost == False:
				i += 1
		i = 0
		for card_from_game in battle_data.player2.army_before_resolution:
			if o.id_source == card_from_game:
				return i
			if card_from_game.ghost == False:
				i += 1
		raise ("didn't find the card in army")

	def get_image(o): #create and return an image
		
		s = o.scale

		#o.image = pygame.Surface([int(o.card.size[0]*s), int(o.card.size[1]*s) ])
		o.image = pygame.Surface(o.card_size)
		o.image.fill([130,100,255])

		font = pygame.font.Font('freesansbold.ttf', 20)
		attack_text = font.render(str(o.attack), True, [0,255,0])
		h_color = [0,255,0]
		if (o.health < o.max_health):
			h_color = [255,0,0]
		health_text = font.render(str(o.health), True, h_color)

		att_surface = attack_text.get_rect()
		hlth_surface = health_text.get_rect()

		blitPosA = [0, o.card_size[1] - att_surface[3]]
		blitPosH = [o.card_size[0] - hlth_surface[2], o.card_size[1] - hlth_surface[3]]

		o.image.blit(attack_text,blitPosA)
		o.image.blit(health_text,blitPosH)


		if (o.divineShield):
			if (o.divine_shield_surf == None):
				card_width,card_height = o.card_size[0],o.card_size[1]
				o.divine_shield_margin = 5
				o.divine_shield_surf = pygame.Surface([card_width + o.divine_shield_margin*2, card_height + o.divine_shield_margin*2])
				o.divine_shield_surf.fill([255, 255, 0])
				o.divine_shield_surf.set_colorkey([123,21,51])
				o.divine_shield_surf.set_alpha(128)
			o.divine_shield_surf.blit(o.image,[o.divine_shield_margin, o.divine_shield_margin])
			return pygame.transform.rotate(scaled(o.divine_shield_surf,o.scale),o.rotation)


		return pygame.transform.rotate(scaled(o.image,o.scale),o.rotation)



	def rotate(angle):# you can also set the rotation directly throught attribut rotation
		o.rotation += angle


	

	def draw(o,displayer):
		displayer.screen.blit(o.get_image(),o.pos)



def scaled(surf,scale):
	dim = surf.get_size()
	dim = [int(dim[0]*scale),int(dim[1]*scale)]
	return pygame.transform.smoothscale(surf,dim)