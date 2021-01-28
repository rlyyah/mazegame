import time
from helpers import key_pressed, clear_screen
from collections import defaultdict
import random
import sys

MAP_HEIGTH = int(sys.argv[1])
MAP_WIDTH = int(sys.argv[2])
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


class Floor(MapElement):
    def __init__(self, point, map_l):
        super().__init__(point, map_l)

    def __str__(self):
        return "O"


class Wall(MapElement):
    def __init__(self, point, map_l):
        super().__init__(point, map_l)
 
    def __str__(self):
        return 'O'
        # return u'\u2588'
# -------------------------------------------------- MAP


class Map():
    def __init__(self, map_width, map_heigth, start_position, exit_positon):
        self.map_width = map_width
        self.map_heigth = map_heigth
        self.start_position = start_position
        self.exit_positon = exit_positon  
        self.players_positions = defaultdict()
        self.walls_positions = defaultdict()
        self.map_borders = defaultdict()
        
    def change_player_position(self, previous_pos, new_position):
        # check if new position is availble
        player = self.players_positions[previous_pos]
        if self.in_map_range(new_position) and new_position not in self.walls_positions:
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
                
    def populate_borders(self):
        minus_one = -1
        for width in range(-1, self.map_width + 1):
            bottom_border_wall = Wall(Point(width, minus_one), self)
            upper_border_wall = Wall(Point(width, self.map_heigth), self)
            self.walls_positions[bottom_border_wall.position] = bottom_border_wall
            self.walls_positions[upper_border_wall.position] = upper_border_wall
        for height in range(self.map_heigth):
            left_border_wall = Wall(Point(minus_one, height), self)
            right_border_wall = Wall(Point(self.map_width, height), self)
            self.walls_positions[left_border_wall.position] = left_border_wall
            self.walls_positions[right_border_wall.position] = right_border_wall

    
class MazeMap(Map):
    
    def __init__(self, map_width, map_heigth, start_position, exit_positon):
        super().__init__(map_width, map_heigth, start_position, exit_positon)  
        self.populate_walls()
        self.points_round = defaultdict()
        self.points_round = {            
            'up': Point(0, 1),
            'right': Point(1, 0),
            'down': Point(0, -1),
            'left': Point(-1, 0)}
        
    def populate_walls(self):
        for row in range(self.map_heigth):
            for col in range(self.map_width):
                wall = Wall(row, col)
                self.walls_positions[Point(col, row)] = wall

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
        # start from starting_pos
        d = Displayer(self)
        checked_point = self.start_position
        self.walls_positions.pop(self.start_position)
        self.walls_positions.pop(self.exit_positon)
        generating_maze = True
        dead_end_road_position = []
        points_queue = [self.start_position]
        while generating_maze:
            # find available points around this_position (1. in the map area, 2. potential wall must have 3 wall around it)
            available_points = []
            for direction in self.points_round:
                potential_point = checked_point + self.points_round[direction]
                # 1. and 2.
                if self.in_map_range(potential_point) and\
                    self.has_walls_around(potential_point) and\
                    potential_point not in dead_end_road_position:
                    available_points += [potential_point]   
            
            if len(available_points) > 0:
                checked_point = available_points[random.randint(0, len(available_points)-1)]
                points_queue += [checked_point]
                # delete point from walls dict
                if checked_point in self.walls_positions: 
                    self.walls_positions.pop(checked_point)
            else:
                # then next_point will be the last index of points_queue
                if len(points_queue) > 1:
                    dead_end_road_position += [points_queue.pop(-1)]
                    checked_point = points_queue[-1]
                else:
                    # if no elements-> finish
                    generating_maze = False
            clear_screen()
            d.prepare_map_string(checked_point)
            d.display_string()
        self.connect_to_exit(self.exit_positon)

    def connect_to_exit(self, finish_point):
        print('FIXIN EXIT')
        checked_point = finish_point
        first_empty_path_found = False
        already_been_to_points = []
        while not first_empty_path_found:
            available_points = []
            for direction in self.points_round:
                potential_point = checked_point + self.points_round[direction]
                if self.in_map_range(potential_point) and potential_point not in already_been_to_points:
                        available_points += [potential_point]
            for point in available_points:
                if point not in self.walls_positions:
                    first_empty_path_found = True
            if not first_empty_path_found:
                already_been_to_points += [checked_point]
                deleted_point = available_points[random.randint(0, len(available_points)-1)]
                self.walls_positions.pop(deleted_point)
                checked_point = deleted_point


class SolveMaze():

    def __init__(self, maze, player):
        self.maze = maze
        self.player = player
        self.displayer = Displayer(maze)

    def start_game(self):
        player_reach_exit = False
        #start_counting = False
        while not player_reach_exit:
            clear_screen()
            if self.player.position == self.maze.start_position:
                self.displayer.prepare_map_string(Point(0,0))
                self.displayer.display_string()
            elif self.player.position == self.maze.exit_positon:
                break
            else:
                self.displayer.prepare_player_vision(self.player.position, self.player.player_vision_length)
                self.displayer.display_player()
            key = key_pressed()
            if key == '0':
                # should be changed
                player_reach_exit = True
            elif key in 'wdsa':
                p1.change_position(key)
        self.finish_game()


    def finish_game(self):
        clear_screen()
        print('WP RAT! U DID GOOD JOB :3')


class Displayer():
    def __init__(self, maze):
        self.maze = maze
        self.displayer_dict = {
            'player': '# ',
            'exit' : 'E ',
            'wall': 'O ',
            'empty': '  ',
            'new-line': '\n'}
        
    def prepare_map_string(self, right_here):
        self.maze_string = ''
        for row in range(self.maze.map_heigth, -2, -1):
            for col in range(-1, self.maze.map_width+1):
                checked_point = Point(col, row)
                if checked_point == right_here:
                    self.maze_string += self.displayer_dict['player']
                    # print(self.maze.players_positions[checked_point], end=' ')
                elif checked_point in self.maze.walls_positions:
                    self.maze_string += self.displayer_dict['wall']
                    # print(self.maze.walls_positions[checked_point], end=' ')
                else:
                    self.maze_string += self.displayer_dict['empty']
                    #print(" ", end=' ')
            self.maze_string += self.displayer_dict['new-line']

    def prepare_player_vision(self, middle, radius):
        visible_walls = defaultdict()
        self.player_vision = ''
        for row in range(middle.y + radius, middle.y-radius, -1):
            for col in range(middle.x-radius, middle.x + radius):
                wall_position = Point(col, row)
                if wall_position == middle:
                    self.player_vision += self.displayer_dict['player']
                    # print('X', end='')
                elif wall_position == self.maze.exit_positon:
                    self.player_vision += self.displayer_dict['exit']
                    # print('E', end='')
                elif wall_position in self.maze.walls_positions:
                    self.player_vision += self.displayer_dict['wall']
                    visible_walls[wall_position] = self.maze.walls_positions[wall_position]
                    # print('O', end='')
                else:
                    self.player_vision += self.displayer_dict['empty']
                    #print(' ', end='')
                #print(end=' ')
            self.player_vision += self.displayer_dict['new-line']
        
    def display_string(self):
        print(self.maze_string)

    def display_player(self):
        print(self.player_vision)
        
if __name__ == '__main__':
    
    
    map2 = MazeMap(MAP_WIDTH, MAP_HEIGTH, Point(0,0), Point(MAP_WIDTH-1, MAP_HEIGTH-1))
    map2.generate_maze()
    map2.populate_borders()
    d = Displayer(map2)
    d.prepare_map_string(Point(0,0))
    d.display_string()

    # p1 = Player(Point(0,0), map2)
    #map2.place_player(p1)

    #game1 = SolveMaze(map2, p1)
    #game1.start_game()

        