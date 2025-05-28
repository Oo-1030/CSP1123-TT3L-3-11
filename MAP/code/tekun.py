from usable import Usable

tekun_talk_distance = 150

class Tekun(Usable):
    def __init__(self, obj_name):
        super().__init__(obj_name)
        self.gacha_active = False
        self.gacha_system = None
        self.player = None
    
    def open_gacha(self):
        from gacha import gacha
        gacha.on_exit = self.exit_gacha
        gacha.run()

    def on(self, other, distance):
        from player import Player
        player = other.get(Player)

        if distance < tekun_talk_distance:
            if not self.gacha_active:
               self.gacha_active = True
               self.player = player
               self.open_gacha()
            else:
               player.show_message("Gacha is already open!")

    def exit_gacha(self):
        print("Exiting gacha!")  
        self.gacha_active = False
        self.gacha_system = None
        player = self.player
        if player:
            player.show_message("Returned to the main game!")