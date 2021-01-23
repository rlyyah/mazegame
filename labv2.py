import random
import os


class Point: 
    def __init__(self, x, y, is_wall):
        self.x = x
        self.y = y
        self.is_wall = is_wall

    def __str__(self):
        if self.is_wall == 1:
            return u'\u2588'
        elif self.is_wall == 0:
            return ' '
        else:
            return 'O'

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.labyrinth = []
        self.start_point = Point(0, 0, 0)
        self.end_point = Point(self.width-1, self.height-1, 0)

    def generate_walls(self):
        for h in range(self.height):
            row = []
            for w in range(self.width):
                is_wall = 1
                p = Point(w, h, is_wall)
                row += [p]
            self.labyrinth += [row] 

    def __str__(self):
        display_lab =''
        display_lab += '-' * (self.width + 2)
        display_lab += '\n'
        for h in range(self.height):
            if h != 0:
                display_lab += '|'
            else:
                display_lab += ' '
            for w in range(self.width):
                display_lab += str(self.labyrinth[h][w])
            if h != self.height-1:
                display_lab += '|'
            else: 
                display_lab += ' '
            display_lab += '\n'
        display_lab += '-' * (self.width + 2)
        return display_lab

    def check_if_neigh_exist(self, point):
        if point.x < 0 or point.x >= self.width:
            return False
        if point.y < 0 or point.y >= self.height:
            return False
        return True

    def check_if_neigh_is_empty_field(self, point):
        if self.labyrinth[point.y][point.x].is_wall == 0:
            return True
        return False

    def check_if_path_can_be_placed(self, point):
        if self.check_if_neigh_is_empty_field(point) == False and self.check_number_of_empty_neigh(point) < 2:
            return True
        return False 

    def find_neighbours(self, point):
        neighbours = []
        if self.check_if_neigh_exist(Point(point.x-1, point.y, 0)):
            neighbours += [self.labyrinth[point.y][point.x-1]]
        if self.check_if_neigh_exist(Point(point.x, point.y+1, 0)):
            neighbours += [self.labyrinth[point.y+1][point.x]]
        if self.check_if_neigh_exist(Point(point.x+1, point.y, 0)):
            neighbours += [self.labyrinth[point.y][point.x+1]]
        if self.check_if_neigh_exist(Point(point.x, point.y-1, 0)):
            neighbours += [self.labyrinth[point.y-1][point.x]]
        return neighbours

    def check_number_of_empty_neigh(self, point):
        count_empty = 0 
        for neigh in self.find_neighbours(point):
            if neigh.is_wall == 0:
                count_empty += 1
        return count_empty

    def check_around(self, point):
        possible_points = []
        for neigh in self.find_neighbours(point):
            if self.check_if_path_can_be_placed(neigh):
                possible_points += [neigh]
        return possible_points

    def build_maze(self, should_display):
        point = self.start_point
        points_visited = []
        is_running = True
        while is_running:
            acceptable_fields = self.check_around(point)
            if len(acceptable_fields) > 0:
                next_empty_point = acceptable_fields[random.randint(0, len(self.check_around(point))-1)]
                self.labyrinth[next_empty_point.y][next_empty_point.x].is_wall = 0
                points_visited += [next_empty_point]
                point = next_empty_point
            else:
                if len(points_visited)>1:
                    points_visited.pop()
                    point = points_visited[-1]
                else:
                    is_running = False
            if(should_display):
                os.system('cls')
                print(self.__str__())
        os.system('cls')
        print(self.__str__())
        
if __name__ == '__main__':
    
    Maze1 = Maze(40, 20)
    Maze1.generate_walls()
    Maze1.build_maze(False)

    press_key = input('')
