from model import Point, Player
from map_generator import MazeMap
from server_displayer import Displayer

class Game():
    def __init__(self, width, height, player_vision):
        self.map_width = width
        self.map_heigth = height
        self.start_point = Point(0,0)
        self.finish_point = Point(self.map_width-1, self.map_heigth-1)
        self.player_vision = player_vision
        self.restart_game = False

    @property
    def walls_positons(self):
        return self.prepared_map.walls_positions
      
    def prepare_game(self):
        maze_map = MazeMap(self.map_width, self.map_heigth, self.start_point, self.finish_point)
        maze_map.generate_maze()
        maze_map.populate_borders()

        player = Player(self.start_point, maze_map, self.player_vision)
        maze_map.place_player(player)
        self.prepared_map = maze_map
        self.set_up_player = player
        self.displayer = Displayer(self.prepared_map)
        
    def change_positon(self, char):
        if char in "wsad":
            self.set_up_player.change_position(char)
            if self.read_new_position() == self.finish_point:
                self.restart_game = True
        elif char in "r":
            self.prepared_map.change_player_position(self.read_new_position(),Point(0,0))
            self.set_up_player.position = Point(0,0)

    def read_new_position(self):
        return self.set_up_player.position

    def display_map(self):
        self.displayer.prepare_map_string()
        self.displayer.display_string()