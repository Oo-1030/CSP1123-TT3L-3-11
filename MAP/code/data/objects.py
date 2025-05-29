from entity import Entity
from sprite import Sprite, Animation
from physics import Body
from player import Player
from usable import Usable
from npc import NPC
from teleporter import Teleporter
from tekun import Tekun

class EntityFactory:
    def __init__(self, name, icon, factory, arg_names=[], defaults=[]):
        self.name = name
        self.icon = icon
        self.factory = factory
        self.arg_names = arg_names
        self.defaults = defaults

entity_factories = [
    # 0 - Make a player
    EntityFactory('Player', 
                  "character.png",
                 lambda args: Entity(Player(), Animation("player_sheet1.png", 64, 64, [(0, 0)], 10), Body(8, 48, 16, 16)),
                 ),
    
    # 1 - Make a cat
    EntityFactory('Cat', "cat.png", lambda args: Entity(Sprite("cat.png"), Body(0, 0, 32, 32))),
    
    # 2 - Make NPC 
    EntityFactory('Fat Guy', "fatguy.png", lambda args: Entity(Sprite(args[1]), NPC(args[0], args[2]), Body(20, 32, 40, 64))),

    # 3 - Make teleport
    EntityFactory('Teleport', "teleport.png", lambda args: Entity(Teleporter(args[0], args[1], args[2]), Sprite("teleport.png"))),

    # 4 - Make a shop
    EntityFactory('Tekun', "tekunStore.png", lambda args: Entity(Tekun("Tekun"),Sprite("tekunStore.png", scale=(450, 250)), Body(0, 0, 450, 250))),

    # 5 - Haji
    EntityFactory('Haji', "haji.png", lambda args: Entity(Sprite("haji.png", scale=(450, 250)), Body(0, 0, 450, 250))),

    # 6 - Learning Point
    EntityFactory('Learning Point', "lp.png", lambda args: Entity(Sprite("lp.png", scale=(350, 652)), Body(0, 0, 350, 652))),

    # 7 - MMU Bus
    EntityFactory('MMU Bus', "bus.png", lambda args: Entity(Sprite("bus.png", scale=(450, 179)), Body(0, 0, 450, 179))),

    # 8 - Haji Boss 
    EntityFactory('Haji Boss', "htcboss.npy", lambda args: Entity(Sprite(args[1]), NPC(args[0], args[2]), Body(20, 32, 40, 64))),

    # 9 - Table
    EntityFactory('Table', "eatTable.png", lambda args: Entity(Sprite("eatTable.png", scale=(64, 64)), Body(0, 0, 64, 64))),
]

def create_entity(id, x, y, data=None, index=None):
    factory = entity_factories[id].factory
    e =  factory(data)
    e.index = index
    e.x = x*32
    e.y = y*32
    return e

