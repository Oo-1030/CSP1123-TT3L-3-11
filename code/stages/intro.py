from entity import Entity
from button import Button
from label import Label
from sprite import Sprite

def start_game():
    from engine import engine
    engine.switch_to("Play")

def intro():
    Entity(Sprite("intro.png", is_ui=True))

    start_game_button = Entity(Label("BrunoAce-Regular.ttf", 
                                         "Start", 50,
                                         (7, 231, 242)))
    
    start_button_size = start_game_button.get(Label).get_bounds()
    
    start_game_button.add(Button(start_game, start_button_size))

    from camera import camera
    start_game_button.x = camera.width/2 - start_button_size.width/2
    start_game_button.y = camera.height - 250