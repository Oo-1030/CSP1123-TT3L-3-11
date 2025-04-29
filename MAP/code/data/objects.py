from entity import Entity
from sprite import Sprite
from player import Player
from physics import Body


entity_factories = [
    # 0 - Makes a player
    lambda args: Entity(Player(), Sprite("CSP1123-TT3L-3-11/MAP/images/character.png", scale=(64, 64) ), Body(15, 32, 32, 32)),

    # 1 - Make a cat
    lambda args: Entity(Sprite("CSP1123-TT3L-3-11/MAP/images/cat.png"), Body(0, 0, 32, 32)),
                        

]

def create_entity(id, x, y, data=None):
    factory = entity_factories[id]
    e =  factory(data)
    e.x = x*32
    e.y = y*32
    return e