from collections import defaultdict

class Point():
    def __init__(self, pos_x, pos_y):
        self.position_x = pos_x
        self.position_y = pos_y

    @property
    def x(self):
        return self.position_x

    @property
    def y(self):
        return self.position_y

    def __add__(self, other):
        return Point(self.x + other.x,
                     self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)
    
    def __str__(self):
        return f'({self.x}, {self.y})'
# -------------------------------------------------- MAP ELEMENTS


class MapElement():
    def __init__(self, point, map_obj):
        self.map = map_obj
        self.position = point


class Player(MapElement):
    def __init__(self, point, map_obj, vision):
        super().__init__(point, map_obj)
        self.moves = defaultdict()
        self.player_vision_length = vision
        self.moves = {
            'w': Point(0, 1),
            'd': Point(1, 0),
            's': Point(0, -1),
            'a': Point(-1, 0)}

    def change_position(self, key):
        new_position = self.position + self.moves[key]
        if self.map.change_player_position(self.position, new_position):
            self.position = new_position
        
    def __str__(self):
        return "X"


class Wall(MapElement):
    def __init__(self, point, map_l):
        super().__init__(point, map_l)
 
    def __str__(self):
        return 'O'