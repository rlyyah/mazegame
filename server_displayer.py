from model import Point


class Displayer():
    def __init__(self, maze):
        self.maze = maze
        self.displayer_dict = {
            'player': '# ',
            'exit' : 'E ',
            'wall': 'O ',
            'empty': '  ',
            'new-line': '\n',
            'start': 'M '}
        
    def prepare_map_string(self):
        self.maze_string = ''
        for row in range(self.maze.map_heigth, -2, -1):
            for col in range(-1, self.maze.map_width+1):
                checked_point = Point(col, row)
                if checked_point in self.maze.players_positions:
                    self.maze_string += self.displayer_dict['player']
                elif checked_point == self.maze.exit_positon:
                    self.maze_string += self.displayer_dict['exit']
                elif checked_point in self.maze.walls_positions:
                    self.maze_string += self.displayer_dict['wall']
                elif checked_point == self.maze.start_position:
                    self.maze_string += self.displayer_dict['start']
                else:
                    self.maze_string += self.displayer_dict['empty']
            self.maze_string += self.displayer_dict['new-line']

    def prepare_player_vision(self, middle, radius):
        self.player_vision = ''
        for row in range(middle.y + radius, middle.y-radius, -1):
            for col in range(middle.x-radius, middle.x + radius):
                wall_position = Point(col, row)
                if wall_position == middle:
                    self.player_vision += self.displayer_dict['player']
                elif wall_position == self.maze.exit_positon:
                    self.player_vision += self.displayer_dict['exit']
                elif wall_position in self.maze.walls_positions:
                    self.player_vision += self.displayer_dict['wall']
                else:
                    self.player_vision += self.displayer_dict['empty']
            self.player_vision += self.displayer_dict['new-line']
        
    def display_string(self):
        print(self.maze_string)

    def display_player(self):
        print(self.player_vision)