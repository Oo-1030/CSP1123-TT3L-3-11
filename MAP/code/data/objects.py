from entity import Entity
from sprite import Sprite
from physics import Body
from player import Player
from usable import Usable
from npc import NPC

entity_factories = [
    # 0 - Make a player
    lambda args: Entity(Player(), Sprite("character.png", scale=(64, 64)), Body(15, 32, 32, 32)),

    # 1 - Make a cat
    lambda args: Entity(Sprite("cat.png"), Body(0, 0, 32, 32)),

    # 2 - Make NPC 
    lambda args: Entity(Sprite(args[1]), NPC(args[0], args[2]), Body(15, 32, 32, 32))
]

def create_entity(id, x, y, data=None, index=None):
    factory = entity_factories[id]
    e =  factory(data)
    e.index = index
    e.x = x*32
    e.y = y*32
    return e

