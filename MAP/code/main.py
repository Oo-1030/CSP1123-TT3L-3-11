from engine import Engine
from stages.menu import menu
from stages.play import play

e = Engine("MMU X Secret")
e.register("Menu", menu)
e.register("Play", play)
e.switch_to("Play")
e.run()