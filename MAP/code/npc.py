from usable import Usable
from sprite import Sprite

npc_folder_location = "CSP1123-TT3L-3-11/MAP/npcs"
npc_talk_distance = 150

class NPC(Usable):
    def __init__(self, obj_name, npc_file,):
        super().__init__(obj_name)
        self.npc_file = npc_file

    def on(self, other, distance):
        from player import Player
        player = other.get(Player)
        if distance < npc_talk_distance:
        
            file = open(npc_folder_location + "/" + self.npc_file, "r")
            data = file.read()
            file.close()
            lines = data.split('\n')
            
            from ui.dialogue_view import DialogueView
            DialogueView(lines, self, player)
        else:
            player.show_message("I need to get closer")
   