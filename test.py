import time
from helpers import key_pressed, clear_screen
from collections import defaultdict

MAP_HEIGTH = 15
MAP_WIDTH = 15
FIRST_ELEMENT = 0
# -------------------------------------------------- HELPERS


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
    def __init__(self, point, map_l):
        self.map = map_l
        self.position = point


class Player(MapElement):
    def __init__(self, point, map_l):
        super().__init__(point, map_l)
        self.moves = defaultdict()
        self.moves = {
            'w': Point(0, 1),
            'd': Point(1, 0),
            's': Point(0, -1),
            'a': Point(-1, 0)}


    def change_position(self, key):
        new_position = self.position + self.moves[key]
        if self.map_l.change_player_position(self.position, new_position):
            self.position = new_position
        
        
    def __str__(self):
        return "X"


class Floor(MapElement):
    def __init__(self, point, map_l):
        super().__init__(point, map_l)


    def __str__(self):
        return "O"


class Wall(MapElement):
    def __init__(self, point, map_l):
        super().__init__(point, map_l)

    
    def __str__(self):
        return '1'
        # return u'\u2588'
# -------------------------------------------------- MAP


class Map():
    def __init__(self, map_width, map_heigth):
        self.map_width = map_width
        self.map_heigth = map_heigth
        self.players_positions = defaultdict()
        
    
    def change_player_position(self, previous_pos, new_position):
        # check if new position is availble
        player = self.players_positions[previous_pos]
        if self.in_map_range(new_position):
            self.players_positions[new_position] = player
            self.players_positions.pop(previous_pos)
            return True
        return False


    def place_player(self, player):
        if self.in_map_range(player.position):
            self.players_positions[player.position] = player
            return True
        return False


    def in_map_range(self, point):
        if point.y in range(self.map_heigth) and point.x in range(self.map_width):
            return True
        return False


    def display_map(self):
        for row in range(self.map_heigth-1, -1, -1):
            for col in range(self.map_width):
                if Point(col, row) in self.players_positions:
                    print(self.players_positions[Point(col, row)], end=' ')
                else:
                    print("O", end=' ')
            print()


class MazeMap(Map):
    
    def __init__(self, map_width, map_heigth, start_position, exit_positon):
        super().__init__(map_width, map_heigth)
        self.start_position = start_position
        self.exit_positon = exit_positon    
        self.populate_walls()
        self.points_round = defaultdict()
        self.points_round = {            
            'up': Point(0, 1),
            'right': Point(1, 0),
            'down': Point(0, -1),
            'left': Point(-1, 0)}


    def populate_walls(self):
        self.walls_positions = defaultdict()
        for row in range(self.map_heigth):
            for col in range(self.map_width):
                wall = Wall(row, col)
                self.walls_positions[Point(col, row)] = wall


    def display_map(self):
        for row in range(self.map_heigth-1, -1, -1):
            for col in range(self.map_width):
                checked_point = Point(col, row)
                if checked_point in self.players_positions:
                    print(self.players_positions[checked_point], end=' ')
                elif checked_point in self.walls_positions:
                    print(self.walls_positions[checked_point], end=' ')
                else:
                    print(" ", end=' ')
            print()

    def has_walls_around(self, point, walls_count=3):
        count_walls = 0
        for direction in self.points_round:
            checked_point = point + self.points_round[direction]
            if not self.in_map_range(checked_point):
                count_walls += 1
            if checked_point in self.walls_positions:
                count_walls += 1
        if count_walls >= walls_count:
            return True
        return False        


    def generate_maze(self):
        import random
        # start from starting_pos
        checked_point = self.start_position
        self.walls_positions.pop(self.start_position)
        self.walls_positions.pop(self.exit_positon)
        generating_maze = True
        do_not_visit_list = []
        points_queue = [self.start_position]
        loop = 0
        while generating_maze:
            print(checked_point)
            # find available points around this_position (1. in the map area, 2. potential wall must have 3 wall around it)
            available_points = []
            for direction in self.points_round:
                potential_point = checked_point + self.points_round[direction]
                # 1. and 2.
                if self.in_map_range(potential_point) and self.has_walls_around(potential_point) and potential_point not in do_not_visit_list:
                    available_points += [potential_point]   
            
            if len(available_points) > 0:
                print("l: ",available_points[0]) 
                checked_point = available_points[random.randint(0, len(available_points)-1)]
                points_queue += [checked_point]
                # delete point from walls dict
                if checked_point in self.walls_positions: 
                    self.walls_positions.pop(checked_point)
            else:
                # then next_point will be the last index of points_queue
                if len(points_queue) > 1:
                    do_not_visit_list += [points_queue.pop(-1)]
                    checked_point = points_queue[-1]
                else:
                    # if no elements-> finish
                    generating_maze = False
            clear_screen()
            self.display_map()
            time.sleep(0.001)
                        

if __name__ == '__main__':
    '''
    # map setup and configuration
    map1 = Map(MAP_WIDTH, MAP_HEIGTH)
    map1.display_map()

    print()
    # create player and place it on the map
    p1 = Player(Point(0,0), map1)
    map1.place_player(p1)

    map1.display_map()
    
    clear_screen()
    loop_running = True
    while loop_running:
        clear_screen()
        map1.display_map()
        print()
        for key in map1.players_positions:
            print("key: ", key)
        print()
        print(p1.position)
        print()
        print("Press any key to display a key, and 0 to quit")
        key = key_pressed()
        if key == '0':
            loop_running = False
        elif key in 'wdsa':
            p1.change_position(key)
        print(key)
    '''
    
    # maze map
    map2 = MazeMap(MAP_WIDTH, MAP_HEIGTH, Point(0,0), Point(14,14))
    map2.display_map()
    map2.generate_maze()
    # map2.display_map()
    


