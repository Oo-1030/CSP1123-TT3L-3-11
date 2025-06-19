from map import Map
import os
import sys

area = None
map_folder_location = "maps"

def resource_path(relative_path):
    """获取资源的绝对路径，兼容开发环境和打包后"""
    if hasattr(sys, '_MEIPASS'):  # 打包后的临时目录
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

class Area:
    def __init__(self, area_file, tile_types):
        global area
        area = self
        self.tile_types = tile_types
        self.load_file(area_file)

    def search_for_first(self, kind):
        for e in self.entities:
            c = e.get(kind)
            if c is not None:
                return e
            
    def remove_entity(self, e):
        self.entities.remove(e)
        for c in e.components:
            g = getattr(c, "breakdown", None)
            if callable(g):
                c.breakdown()

    def load_file(self, area_file):
        from data.objects import create_entity
        from engine import engine
        self.area_file = area_file
        if not area_file in engine.persistent_removed:
            engine.persistent_removed[area_file] = []
        
        engine.reset()

        # Read all the data from the file
        file_path = resource_path(os.path.join(map_folder_location, area_file))
        with open(file_path, "r") as file:
            data = file.read()
        self.name = area_file.split(".")[0].title().replace("_", " ")


        # Split up the data by minus signs
        chunks = data.split('-')
        tile_map_data = chunks[0]
        entity_data = chunks[1]

        # Load the map
        self.map = Map(tile_map_data, self.tile_types)

        # Load the entities
        self.entities = []
        entity_lines = entity_data.split('\n')[1:]
        for index, line in enumerate(entity_lines):
            try:
                items = line.split(',')
                id = int(items[0])
                x = int(items[1])
                y = int(items[2])
                self.entities.append(create_entity(id, x, y, items[3:], index=index))
            except Exception as e:
                print(f"Error parsing line: {line}. {e}")
        
        # Remove any entites in persistent
        l = sorted(engine.persistent_removed[area_file])
        l.reverse()
        for index in l:
            self.remove_entity(self.entities[index])
