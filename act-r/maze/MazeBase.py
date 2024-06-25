import queue

class ConnerPoint():
    def __init__(self, no, x, y):
        self.__no = no
        self.__x = x
        self.__y = y

    def __repr__(self):
        return "<Point: [no={}, y={}, x={}]>".format(self.no, self.y, self.x)
    
    @property
    def no(self):
        return self.__no

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

class StateInfo():
    def __init__(self, no, west, north, east, south):
        self.no = no
        self.connected_no = [west, north, east, south]

class State():
    def __init__(self, row=-1, column=-1):
        self.row = row
        self.column = column

    def __repr__(self):
        return "<State: [{}, {}]>".format(self.row, self.column)

    def clone(self):
        return State(self.row, self.column)

    def __hash__(self):
        return hash((self.row, self.column))

    def __eq__(self, other):
        return self.row == other.row and self.column == other.column

class MazeBase():
    START = -1
    PATH = 0
    WALL = 1
    GOAL = 99
    _DEFAULT_REWARD = 0
    _UNCHANGED_REWARD = -1
    _GOAL_REWARD = 10

    def _search_longest_distance_Point(self, start_point, conner_points, state_inf_dic):
        check_visited_no = [False] * (len(conner_points) + 1)
        check_visited_no[start_point.no] = True

        q = queue.Queue()
        q.put(start_point)
        hop_count = 0

        l = [(start_point, hop_count)]
        while not q.empty():
            cp = q.get()
            state_info = state_inf_dic[State(cp.y, cp.x)]
            for connected_no in state_info.connected_no:
                if connected_no is not None and not check_visited_no[connected_no]:
                    hop_count += 1
                    ccp = list(filter(lambda p: p.no == connected_no, conner_points))[0]
                    l.append((ccp, hop_count))
                    q.put(ccp)
                    check_visited_no[connected_no] = True

        return max(l, key=(lambda x: x[1]))

    def create_maze(self, width, height):
        pass

    def load_maze(self, maze_map):
        self.maze_map = maze_map
        self.width = len(maze_map[0])
        self.height = len(maze_map)
        self.search_conner_points()
        self.create_conner_network()
        self._set_start_goal()

    def search_conner_points(self):
        if len(self.maze_map) == 0:
            print('not created maze')
            exit()

        conner_points = []
        conner_no = 1
        for i in range(1, self.height):
            for j in range(1, self.width):
                if self.maze_map[i][j] == MazeBase.PATH or self.maze_map[i][j] == MazeBase.START or self.maze_map[i][j] == MazeBase.GOAL :
                    wall_cnt = 0
                    if self.maze_map[i-1][j] == MazeBase.WALL:
                        wall_cnt += 1
                    if self.maze_map[i+1][j] == MazeBase.WALL:
                        wall_cnt += 1
                    if self.maze_map[i][j-1] == MazeBase.WALL:
                        wall_cnt += 1
                    if self.maze_map[i][j+1] == MazeBase.WALL:
                        wall_cnt += 1

                    #基本的に上下左右に壁が2つあったら通路とする
                    #ただしL字の場合はコーナーとする
                    if (wall_cnt != 2 or 
                    (wall_cnt == 2 and 
                    ((self.maze_map[i-1][j] == MazeBase.PATH and self.maze_map[i][j-1] == MazeBase.PATH) or 
                    (self.maze_map[i-1][j] == MazeBase.PATH and self.maze_map[i][j+1] == MazeBase.PATH) or
                    (self.maze_map[i+1][j] == MazeBase.PATH and self.maze_map[i][j-1] == MazeBase.PATH) or
                    (self.maze_map[i+1][j] == MazeBase.PATH and self.maze_map[i][j+1] == MazeBase.PATH)))):
                        conner_points.append(ConnerPoint(conner_no, j, i))
                        conner_no += 1

        print(conner_points)
        self.conner_points = conner_points

    def create_conner_network(self):
        state_inf_dic = {}
        for conner in self.conner_points:
            base_i = conner.y
            base_j = conner.x
            west = None
            north = None
            east = None
            south = None

            for j in range(base_j-1, 0, -1):
                if self.maze_map[base_i][j] == MazeBase.WALL:
                    break
                
                no = self._exist_pos(j, base_i)
                if no > 0:
                    west = no
                    break

            for i in range(base_i-1, 0, -1):
                if self.maze_map[i][base_j] == MazeBase.WALL:
                    break
                
                no = self._exist_pos(base_j, i)
                if no > 0:
                    north = no
                    break 

            for j in range(base_j+1, self.width):
                if self.maze_map[base_i][j] == MazeBase.WALL:
                    break
                
                no = self._exist_pos(j, base_i)
                if no > 0:
                    east = no
                    break

            for i in range(base_i+1, self.height):
                if self.maze_map[i][base_j] == MazeBase.WALL:
                    break
                
                no = self._exist_pos(base_j, i)
                if no > 0:
                    south = no
                    break
            state_inf_dic[State(conner.y, conner.x)] = StateInfo(conner.no, west, north, east, south)
            print("{} : {}, {}, {}, {}".format(conner.no, west, north, east, south))
        self.state_inf_dic = state_inf_dic

    def _exist_pos(self, x, y):
        for conner in self.conner_points:
            if conner.x == x and conner.y == y:
                return conner.no
        return 0

    def _set_start_goal(self):
        self.start_point = self.conner_points[0]
        self.goal_point = self._search_longest_distance_Point(self.start_point, self.conner_points, self.state_inf_dic)[0]
        self.maze_map[self.start_point.y][self.start_point.x] = MazeBase.START
        self.maze_map[self.goal_point.y][self.goal_point.x] = MazeBase.GOAL

    def print_maze(self):
        for row in self.maze_map:
            for cell in row:
                if cell == MazeBase.PATH:
                    print('   ', end='')
                elif cell == MazeBase.START:
                    print(' S ', end='')
                elif cell == MazeBase.GOAL:
                    print(' G ', end='')
                elif cell == MazeBase.WALL:
                    print('###', end='')
            print()