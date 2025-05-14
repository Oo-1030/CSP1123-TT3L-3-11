from usable import Usable

tekun_talk_distance = 150

class Tekun(Usable):
    def __init__(self, obj_name):
        super().__init__(obj_name)
        self.gacha_active = False
        self.gacha_system = None

    def on(self, other, distance):
        from player import Player
        player = other.get(Player)

        if distance < tekun_talk_distance:
            if not self.gacha_active:
                from gacha import GachaSystem, animation
                self.gacha_active = True
                self.gacha_system = GachaSystem()
                self.gacha_system.on_exit = self.exit_gacha  # Set the exit callback
                animation()  # Start the gacha game
            else:
                player.show_message("Gacha is already open!")
        else:
            player.show_message("I need to get closer")

    def exit_gacha(self):
        """Called when Q is pressed or gacha exits"""
        self.gacha_active = False
        self.gacha_system = None
        # Optional: Notify the player
        player = self.get_player_somehow()  # Replace with your player reference
        if player:
            player.show_message("Returned to the main game!")

