class Usable:
    def __init__(self, obj_name):
        self.obj_name = obj_name
        from engine import engine
        engine.usables.append(self)

    def breakdown(self):
        from engine import engine
        engine.usables.remove(self)

    def on(self, other, distance):
        print("Base on function called")
