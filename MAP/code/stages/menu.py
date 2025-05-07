from entity import Entity
from button import Button
from label import Label
from sprite import Sprite

def new_game():
    from engine import engine
    engine.switch_to("Intro")

def quit_game():
    from engine import engine
    engine.running = False

def menu():
    Entity(Sprite("mainMenu.png", is_ui=True))

    new_game_button = Entity(Label("BrunoAce-Regular.ttf", 
                                         "New Game", 80,
                                         (255, 255, 0)))
    quit_game_button = Entity(Label("BrunoAce-Regular.ttf", 
                                         "Quit Game", 80,
                                         (255, 255, 0)))
    
    new_button_size = new_game_button.get(Label).get_bounds()
    quit_button_size = quit_game_button.get(Label).get_bounds()
    
    new_game_button.add(Button(new_game, new_button_size))
    quit_game_button.add(Button(quit_game, quit_button_size))

    from camera import camera
    new_game_button.x = camera.width/2 - new_button_size.width/2
    new_game_button.y = camera.height - 350
    quit_game_button.x = camera.width/2 - quit_button_size.width/2
    quit_game_button.y = camera.height - 200