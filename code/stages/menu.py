from entity import Entity
from button import Button
from label import Label
from sprite import Sprite

def play_game():
    from engine import engine
    engine.switch_to("Play")

def quit_game():
    from engine import engine
    engine.running = False

def intro():
    from engine import engine
    engine.switch_to("Intro")

def menu():
    Entity(Sprite("mainMenu.png", is_ui=True))

    play_game_button = Entity(Label("BrunoAce-Regular.ttf", 
                                         "Play", 80,
                                         (255, 255, 0)))
    quit_game_button = Entity(Label("BrunoAce-Regular.ttf", 
                                         "Quit Game", 80,
                                         (255, 255, 0)))
    intro_button = Entity(Label("BrunoAce-Regular.ttf", 
                                         "Intro", 80,
                                         (255, 255, 0)))
    
    play_button_size = play_game_button.get(Label).get_bounds()
    quit_button_size = quit_game_button.get(Label).get_bounds()
    intro_button_size = intro_button.get(Label).get_bounds()
    
    play_game_button.add(Button(play_game, play_button_size))
    quit_game_button.add(Button(quit_game, quit_button_size))
    intro_button.add(Button(intro, quit_button_size))

    from camera import camera
    play_game_button.x = camera.width/2 - play_button_size.width/2
    play_game_button.y = camera.height - 350
    quit_game_button.x = camera.width/2 - quit_button_size.width/2
    quit_game_button.y = camera.height - 100
    intro_button.x = camera.width/2 - intro_button_size.width/2
    intro_button.y = camera.height - 220