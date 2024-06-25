import random
import os
import csv
import maze.MazeBase as mb

class MazeWallExtended(mb.MazeBase):
    lst_cell_start_make_wall = []

    def create_maze(self, width, height):
        if( (height < mb.MazeBase.MIN_HEIGHT or width < mb.MazeBase.MIN_WIDTH) or
           ((width % 2) == 0) or
           ((height % 2) == 0)):
            print('width and height value is odd value at least 5')
            exit()

        self.maze_map = []
        self.conner_points = []
        self.state_inf_dic = {}
        self.width = width
        self.height = height

        self.__set_inner_wall_point()
        self.__make_maze()

        self.search_conner_points()
        self.create_conner_network() 
        self._set_start_goal()

    def __set_inner_wall_point(self):
        self.maze_map = []
        for x in range(0, self.width):
            row = []
            for y in range(0, self.height):
                if (x == 0 or y == 0 or x == self.width-1 or y == self.height -1):
                    cell = mb.MazeBase.WALL
                else:
                    cell = mb.MazeBase.PATH
                    if (x % 2 == 0 and y % 2 == 0):
                        self.lst_cell_start_make_wall.append([y, x])
                row.append(cell)
            self.maze_map.append(row)

    def __make_maze(self):
        while self.lst_cell_start_make_wall != []:
            y_start, x_start  = self.lst_cell_start_make_wall.pop(random.randrange(0, len(self.lst_cell_start_make_wall)))
            if self.maze_map[y_start][x_start] == mb.MazeBase.PATH:
                self.lst_current_wall = []
                self.__extend_wall(x_start, y_start)
    
    def __extend_wall(self, x, y):
        lst_direction = []
        if self.maze_map[y-1][x] == mb.MazeBase.PATH and [y-2, x] not in self.lst_current_wall:
            lst_direction.append('up')
        if self.maze_map[y][x+1] == mb.MazeBase.PATH and [y, x+2] not in self.lst_current_wall:
            lst_direction.append('right')
        if self.maze_map[y+1][x] == mb.MazeBase.PATH and [y+2, x] not in self.lst_current_wall:
            lst_direction.append('down')
        if self.maze_map[y][x-1] == mb.MazeBase.PATH and [y, x-2] not in self.lst_current_wall:
            lst_direction.append('left')
        if lst_direction != []:
            self.maze_map[y][x] = mb.MazeBase.WALL
            self.lst_current_wall.append([y, x])
            direction = random.choice(lst_direction)
            contineu_make_wall = False
            if direction == 'up':
                contineu_make_wall = (self.maze_map[y-2][x] == mb.MazeBase.PATH)
                self.maze_map[y-1][x] = mb.MazeBase.WALL
                self.maze_map[y-2][x] = mb.MazeBase.WALL
                self.lst_current_wall.append([y-2, x])
                if contineu_make_wall:
                    self.__extend_wall(x, y-2)
            if direction == 'right':
                contineu_make_wall = (self.maze_map[y][x+2] == mb.MazeBase.PATH)
                self.maze_map[y][x+1] = mb.MazeBase.WALL
                self.maze_map[y][x+2] = mb.MazeBase.WALL
                self.lst_current_wall.append([y, x+2])
                if contineu_make_wall:
                    self.__extend_wall(x+2, y)
            if direction == 'down':
                contineu_make_wall = (self.maze_map[y+2][x] == mb.MazeBase.PATH)
                self.maze_map[y+1][x] = mb.MazeBase.WALL
                self.maze_map[y+2][x] = mb.MazeBase.WALL
                self.lst_current_wall.append([y+2, x])
                if contineu_make_wall:
                    self.__extend_wall(x, y+2)
            if direction == 'left':
                contineu_make_wall = (self.maze_map[y][x-2] == mb.MazeBase.PATH)
                self.maze_map[y][x-1] = mb.MazeBase.WALL
                self.maze_map[y][x-2] = mb.MazeBase.WALL
                self.lst_current_wall.append([y, x-2])
                if contineu_make_wall:
                    self.__extend_wall(x-2, y)
        else:
            previous_point_y, previous_point_x = self.lst_current_wall.pop()
            self.__extend_wall(previous_point_x, previous_point_y)

if __name__=='__main__':
    width = 13
    height = 13
    maze_map = MazeWallExtended()
    maze_map.create_maze(width, height)

    dir_name = str(width) + "_" + str(height)
    os.makedirs(dir_name, exist_ok=True)
    for i in range(0, 100):
        maze_map.create_maze(width, height)
        with open("{}\{:03d}.csv".format(dir_name, i),mode='w', newline="") as f:
            writer = csv.writer(f)
            for row in maze_map.maze_map:
                writer.writerow(row)

    cnt = 0
    mazes = []
    print(os.getcwd())
    while True:
        path = "{}\\{}\\{:03d}.csv".format(os.getcwd(), dir_name, cnt)
        if not os.path.exists(path):
            break
        
        m = []
        with open(path, "r") as f:
            reader = csv.reader(f)
            for line in reader:
                m.append([int(n) for n in line])
        
        mazes.append(m)
        cnt+=1
    
    for m in mazes:
        maze_map.load_maze(m)
        maze_map.print_maze()