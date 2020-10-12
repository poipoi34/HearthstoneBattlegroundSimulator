import m_card

def fct_summon(card, k = 1):
    def effect(source_card):
        for i in range(k):
            source_card.owner.summon(source_card,at=card.owner.army_before_resolution.index(source_card))
    return effect

def deal_aoe_damage(k):
    def effect(source_card):
        players = [source_card.battle_manager.player1,source_card.battle_manager.player1]
        for player in players:
            for card in player.army_before_resolution:
                card.take_damage(k)
    return effect


class Effect:
    def __init__(o, callable_obj, param = {}, instant = True, priorised = False):
        o.callable_obj = callable_obj
        o.param = {}
        o.priorised = priorised
        o.instant = instant
        
    def __call__(o):
        o.callable_obj(o.param)

class E_summon(Effect):
    def __init__(o, card, k = 1,*, callable_obj = None, player_target = None, at = -1, source_card = None):
        Effect.__init__(o, callable_obj)
        o.card = card
        o.k =  k
        o.source_card = source_card
        o.player_target = player_target
        o.at = at


    def __call__(o, source = None):
        if o.player_target == None:
            o.player_target = source.owner

        if o.callable_obj != None:
            o.callable_obj(o.param)

        o.resolve_member(source)
        
        for i in range(o.k):
            if isinstance(o.at, card_definition.Card):
                o.at = o.player_target.army_before_resolution.index(o.at)
            if not isinstance(o.card, card_definition.Card):
                card = o.card()
            o.source.get_player().summon(card, at=o.at)

    def resolve_member(o, source):
        if type(o.k) is not int:
            o.k = o.k(source)
        



