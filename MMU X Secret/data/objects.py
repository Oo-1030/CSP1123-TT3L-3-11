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
                 lambda args: Entity(Player(), Animation("player_sheet1.png", 64, 64, [(0, 0)], 10), Body(18, 48, 16, 16)),
                 ),
    
    # 1 - Make a cat
    EntityFactory('Cat', "cat.png", lambda args: Entity(Sprite("cat.png"), Body(0, 0, 32, 32))),
    
    # 2 - Make NPC 
    EntityFactory('Fat Guy', "fatguy.png", lambda args: Entity(Sprite(args[1]), NPC(args[0], args[2]), Body(10, 32, 32, 64))),

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
    EntityFactory('Haji Boss', "htcboss.png", lambda args: Entity(Sprite(args[1]), NPC(args[0], args[2]), Body(20, 32, 40, 64))),

    # 9 - Table
    EntityFactory('Table', "eatTable.png", lambda args: Entity(Sprite("eatTable.png", scale=(64, 64)), Body(0, 0, 64, 64))),

    # 10 - Fazir 
    EntityFactory('Fazir', "fazir.png", lambda args: Entity(Sprite(args[1]), NPC(args[0], args[2]), Body(20, 32, 40, 64))),

    # 11 - Rane
    EntityFactory('Rane', "rane.png", lambda args: Entity(Sprite(args[1]), NPC(args[0], args[2]), Body(20, 32, 40, 64))),

    # 12 - Edeline
    EntityFactory('Edeline', "edeline.png", lambda args: Entity(Sprite(args[1]), NPC(args[0], args[2]), Body(20, 32, 40, 64))),

    # 13 - Elves
    EntityFactory('Elves', "elves.png", lambda args: Entity(Sprite(args[1]), NPC(args[0], args[2]), Body(20, 32, 40, 64))),

    # 14 - Make hidden teleport
    EntityFactory('TeleportH', "grassH.png", lambda args: Entity(Teleporter(args[0], args[1], args[2]), Sprite("grassH.png"))),

    # 15 - X
    EntityFactory('X', "X.png", lambda args: Entity(Sprite(args[1]), NPC(args[0], args[2]), Body(20, 32, 40, 64))),

    # 16 - Red Table
    EntityFactory('Red Table', "redTable.png", lambda args: Entity(Sprite("redTable.png", scale=(64, 64)), Body(0, 0, 64, 64))),

    # 17 - White Table
    EntityFactory('White Table', "whiteTable.png", lambda args: Entity(Sprite("whiteTable.png", scale=(64, 64)), Body(0, 0, 64, 64))),

    # 18 - Round Seat
    EntityFactory('Round Seat', "roundSeat.png", lambda args: Entity(Sprite("roundSeat.png", scale=(128, 128)), Body(0, 0, 128, 128))),

    # 19 - Coway
    EntityFactory('Coway', "coway.png", lambda args: Entity(Sprite("coway.png", scale=(64, 64)), Body(0, 0, 64, 64))),

    # 20 - Coway LP
    EntityFactory('CowayLP', "cowayLP.png", lambda args: Entity(Sprite("cowayLP.png", scale=(64, 64)), Body(0, 0, 64, 64))),

    # 21 - help
    EntityFactory('Help', "help.png", lambda args: Entity(Sprite("help.png"))),

    # 22 - click
    EntityFactory('click', "click.png", lambda args: Entity(Sprite("click.png"))),

    # 23 - shop
    EntityFactory('shop', "shop.png", lambda args: Entity(Sprite("shop.png"))),

    # 24 - Make a tree
    EntityFactory('Tree', "tree.png", lambda args: Entity(Sprite("tree.png", scale=(128,128)), Body(0, 0, 128, 128))),

]

def create_entity(id, x, y, data=None, index=None):
    factory = entity_factories[id].factory
    e =  factory(data)
    e.index = index
    e.x = x*32
    e.y = y*32
    return e

