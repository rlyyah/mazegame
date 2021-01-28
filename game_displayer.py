from model import Point
from helpers import clear_screen

class handle_client_map():
    def __init__(self, walls, options):
        self.walls = walls
        self.s_pos = options['start']
        self.f_pos = options['finish']
        self.player_info = options['player-options']
        self.map_info = options['map-options']
        self.displayer_dict = {
            'player': '# ',
            'exit' : 'E ',
            'wall': 'O ',
            'empty': '  ',
            'new-line': '\n',
            'map': 'M '}
        self.handle_options()
        self.listen_to_input = True

    def handle_options(self):
        self.map_width = self.map_info['width']
        self.map_height = self.map_info['height']
        self.start_position = Point(self.s_pos['x'], self.s_pos['y'])
        self.player_position = self.start_position
        self.player_vision = self.player_info['player-vision']
        self.exit_position = Point(self.f_pos['x'], self.f_pos['y'])

    def update_position(self, new_position):
        self.player_position = Point(new_position['x'], new_position['y'])

    def handle_player_vision(self):
        if self.player_position == self.start_position:
            self.draw_whole_map()
        elif self.player_position == self.exit_position:
            self.listen_to_input = False
        else:
            self.draw_map()
        self.display_for_player()
    
    def draw_whole_map(self):
        self.player_vision_dp = ''
        for row in range(self.map_height + 1, -2, -1):
            for col in range(-1, self.map_width + 1):
                checked_position = Point(col, row)
                if checked_position == self.player_position:
                    self.player_vision_dp += self.displayer_dict['player']
                elif checked_position == self.exit_position:
                    self.player_vision_dp += self.displayer_dict['exit']
                elif checked_position in self.walls:
                    self.player_vision_dp += self.displayer_dict['wall']
                elif checked_position == self.start_position:
                    self.player_vision_dp += self.displayer_dict['map']
                else:
                    self.player_vision_dp += self.displayer_dict['empty']
            self.player_vision_dp += self.displayer_dict['new-line']

    def draw_map(self):
        self.player_vision_dp = ''
        for row in range(self.player_position.y + self.player_vision, self.player_position.y-self.player_vision, -1):
            for col in range(self.player_position.x-self.player_vision, self.player_position.x + self.player_vision):
                checked_position = Point(col, row)
                if checked_position == self.player_position:
                    self.player_vision_dp += self.displayer_dict['player']
                    # print('X', end='')
                elif checked_position == self.exit_position:
                    self.player_vision_dp += self.displayer_dict['exit']
                    # print('E', end='')
                elif checked_position in self.walls:
                    self.player_vision_dp += self.displayer_dict['wall']
                elif checked_position == self.start_position:
                    self.player_vision_dp += self.displayer_dict['map']
                    # print('O', end='')
                else:
                    self.player_vision_dp += self.displayer_dict['empty']
                    #print(' ', end='')
                #print(end=' ')
            self.player_vision_dp += self.displayer_dict['new-line']
    
    def display_for_player(self):
        clear_screen()
        print(self.player_vision_dp)