from model import Point
from collections import defaultdict
from model import Wall
import random


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
        self.connect_to_exit(self.exit_positon)

    def connect_to_exit(self, finish_point):
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