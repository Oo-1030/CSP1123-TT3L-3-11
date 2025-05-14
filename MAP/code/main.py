from engine import Engine
from stages.menu import menu
from stages.intro import intro
from stages.play import play

e = Engine("MMU X Secret")
e.register("Menu", menu)
e.register("Intro", intro)
e.register("Play", play)
e.switch_to("Menu")
e.run()