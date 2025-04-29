from map import Map
from data.objects import create_entity

area = None
area_folder_location = "maps"

class Area:
    def __init__(self, area_file, tile_types):
        global area
        area = self
        self.tile_types = tile_types
        self.load_file(area_file)

    def load_file(self, area_file):
        file = open("CSP1123-TT3L-3-11" + "/" + "MAP" + "/" + area_folder_location + "/" + area_file, "r")
        data = file.read()
        file.close()

        chunks = data.split('-')
        tile_map_data = chunks[0]
        entity_data = chunks[1]

        self.map = Map(tile_map_data, self.tile_types)

        self.entities = []
        entity_lines = entity_data.split('\n')[1:]
        for line in entity_lines:
            try:
                items = line.split(',')
                id = int(items[0])
                x = int(items[1])
                y = int(items[2])
                self.entities.append(create_entity(id, x, y, items))
            except:
                print(f"Error parsing line: {line}")