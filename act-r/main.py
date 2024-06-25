import actr as ar
import numpy as np
import pandas as pd
import time
import os
import math
import maze.MazeWallExtended as mwe
import csv
from agent_base import AgentBase
import maze.MazeBase as mb

class Maze(AgentBase):   
    def __init__(self, prefix):
        self._prefix = prefix
        self.DF_TRIAL_COLUMNS = ['map_no', 'reward','round', 'skill', 'goal_time', 'goal_rate', 'entropy', 'entropy_n', "achivenmt_time", "giveup_time", 'probability', 'path']
        ar.add_command("clear",self.clear_maze,"")
        ar.add_command("visit-points", self.visit_points, "")
        ar.add_command("got-bored", self.got_bored, "")
        ar.add_command("terminate", self.terminate, "")
        ar.add_command("get-current-start", self.get_current_start, "")
        ar.add_command("get-current-goal", self.get_current_goal, "")
        ar.add_command("debug-print", self.debug_print, "")
        ar.add_command("get-reward-value", self.get_reward_value, "")
        ar.add_command("fired-judgement-rule", self.fire_judgement_rule, "")
        ar.stop_output()

    @property
    def save_log_path(self):
        return "{}_{}_{}_{}_{}_{}_{}.csv".format(self._prefix, self._area, self._trial_num, self._reward_min_num, self._additional_reward, self._reward_step, self._limit_time_sec)

    def get_current_start(self):
        return self.start_no
    
    def get_current_goal(self):
        return self.goal_no

    def _init_trial(self):
        ar.reset()
        self.init_rule_num = len(ar.spp())
        self._init_map_environment()
        self.is_fun = True
        self.round = 0
        self.count_map = np.zeros((self.maze_env.height, self.maze_env.width))
        self._trial_paths = []
        self._path = []
        self._reward_value = 0

    def _init_map_environment(self):
        for l in self.actr_env:
            ar.add_dm(l)

    def _init_learn(self):
        self.map_nos = []
        self.rewards = []
        self.rounds = []
        self.skills = []
        self._goal_times = []
        self.goal_rates = []
        self.entropies = []
        self._goal_achivenmt_times = []
        self._giveup_times = []
        self._entropies_n = []
        self._probabilities = []
        self._paths = []

        self.count_map_sum = np.zeros((self.maze_env.height, self.maze_env.width))

    def _save_recoding_trial_log(self):
        df = pd.DataFrame(
            data={
                'map_no': self.map_nos,
                'reward': self.rewards,
                'round': self.rounds,
                'skill' : self.skills,
                'goal_time': self._goal_times,
                'goal_rate': self.goal_rates,
                'entropy': self.entropies,
                'entropy_n': self._entropies_n,
                'achivenmt_time' : self._goal_achivenmt_times,
                'giveup_time' : self._giveup_times,
                'probability' : self._probabilities,
                'path' : self._paths
            },
            columns = self.DF_TRIAL_COLUMNS
        )

        if os.path.exists(self.save_log_path) == True:
            df.to_csv(self.save_log_path, index=False, header=False, mode='a')
        else:
            df.to_csv(self.save_log_path, index=False, header=True, mode='w')
    
    def _record_trial(self, map_no, reward, round, goal_time, goal_rate, entropy, entropy_n, achivenmt_time, giveup_time, probability, trial_paths):
        skill = len(ar.spp()) - self.init_rule_num
        self.map_nos.append(map_no)
        self.rewards.append(reward)
        self.rounds.append(round)
        self.skills.append(skill)
        self._goal_times.append(goal_time)
        self.goal_rates.append(goal_rate)
        self.entropies.append(entropy)
        self._entropies_n.append(entropy_n)
        self._goal_achivenmt_times.append(achivenmt_time)
        self._giveup_times.append(giveup_time)
        self._probabilities.append(probability)
        self._paths.append(trial_paths)

    def _create_actr_map(self, maze_env):
        cnt = 0
        table = []
        for k, v in maze_env.state_inf_dic.items():
            dir = 1
            for to in v.connected_no:
                row = []
                if to is not None:
                    foward_dir = self._get_forward_dir(dir)
                    back_dir = self._get_back_dir(dir)
                    row.append("info-" + str(cnt))
                    row.append("isa")
                    row.append("maze-info")
                    row.append("from")
                    row.append(v.no)
                    row.append("to")
                    row.append(to)
                    row.append("f-west")
                    row.append(foward_dir[0])
                    row.append("f-north")
                    row.append(foward_dir[1])
                    row.append("f-east")
                    row.append(foward_dir[2])
                    row.append("f-south")
                    row.append(foward_dir[3])
                    row.append("b-west")
                    row.append(back_dir[0] if back_dir[0] == 1 else -1)
                    row.append("b-north")
                    row.append(back_dir[1] if back_dir[1] == 1 else -1)
                    row.append("b-east")
                    row.append(back_dir[2] if back_dir[2] == 1 else -1)
                    row.append("b-south")
                    row.append(back_dir[3] if back_dir[3] == 1 else -1)
                    table.append(row)
                    cnt += 1
                dir <<= 1
        return table
    
    def _get_forward_dir(self, dir):
        return (dir & 0b0001, (dir & 0b0010) >> 1, (dir & 0b0100) >> 2, (dir & 0b1000) >> 3)

    def _get_back_dir(self, dir):
        shifted_dir = dir << 2
        shifted_dir = shifted_dir if shifted_dir <= 0b1000 else shifted_dir >> 4
        return (shifted_dir & 0b0001, (shifted_dir & 0b0010) >> 1, (shifted_dir & 0b0100) >> 2, (shifted_dir & 0b1000) >> 3)

    def run(self, area, map_no, maze_env, trial_num, reward_min_num, additional_reward, reward_step, limit_time_sec, limit_total_sec):
        self._area = area
        self._trial_num = trial_num
        self._reward_min_num = reward_min_num
        self._additional_reward = additional_reward
        self._reward_step = reward_step
        self._limit_time_sec = limit_time_sec

        self.map_no = map_no
        self.maze_env = maze_env
        self.actr_env = self._create_actr_map(maze_env)
        print("start:" + str(maze_env.start_point.no))
        print("goal:" + str(maze_env.goal_point.no))
        self.start_no = maze_env.start_point.no
        self.goal_no = maze_env.goal_point.no

        count_maps = []
        for reward in range(reward_min_num, reward_min_num + additional_reward * reward_step, additional_reward):
            self.current_reward = reward
            self._init_learn()
            trial_cnt = 0
            while True:
                self._init_trial()
                self._reward_value = reward
                clear = 0
                achivenmt_times = 0
                giveup_time = 0
                self.round = 0
                self._wait_until_judgment_rule()
                while self.is_fun and abs(giveup_time - limit_total_sec) >= 0.001:
                    run_time = 0
                    self.is_found = False
                    remaining_time = limit_total_sec - giveup_time
                    run_time = ar.run(limit_time_sec if remaining_time > limit_time_sec else remaining_time)[0]
                    print("start round:" + str(self.round + 1) + " " + str(giveup_time) +"(" + str(run_time) + ")" + " " + str(self.is_found))
                    giveup_time += run_time

                    self.round += 1
                    if self.is_found:
                        clear += 1
                        achivenmt_times += run_time
                    ar.goal_focus('stack-goal-limit')
                    self._wait_until_judgment_rule()
                    m = map(str, self._path)
                    self._trial_paths.append(str(self.is_found) + ":".join(m) + " ")
                    self._path.clear()

                if self.round > 0:
                    trial_cnt += 1
                    print("end map-no:%s reword:%s, trial:%s" % (self.map_no, reward, trial_cnt))
                    self._record_trial(
                      map_no,
                      reward,
                      self.round,
                      clear,
                      clear / self.round,
                      self._calc_entropy(self.count_map, maze_env.conner_points),
                      self._calc_entropy(self.count_map, maze_env.conner_points,1.0/math.log(len(maze_env.conner_points))),
                      achivenmt_times / clear if clear > 0 else 0,
                      giveup_time,
                      ":".join(map(str,self._calc_probabilities(self.count_map, maze_env.conner_points))),
                      self._trial_paths)
                    self.count_map_sum += self.count_map
                    if trial_cnt == trial_num:
                        break
            self._save_recoding_trial_log()
            count_maps.append(self.count_map_sum/trial_num)

    def _wait_until_judgment_rule(self):
      self._fired_judgment_rule = False
      ar.goal_focus('stack-goal-limit')
      while not self._fired_judgment_rule:
        ar.run(0.05)

    def _is_valid_path(self, path):
        l = len(path)
        if l < 2:
            return False
        
        i = 1
        while i < len(path):
            if not path[i-1] == path[i]:
                old = list(filter(lambda cp: cp.no == path[i-1], self.maze_env.conner_points))[0]
                old_info = self.maze_env.state_inf_dic[mb.State(old.y, old.x)]
                if not path[i] in old_info.connected_no:
                    print(path[i-1])
                    print(path[i])
                    return False
            i+=1
        return True
    
    def _print_productions(self):
        pnames = ar.all_productions()
        for name in pnames:
            print(ar.pp(name))

    def fire_judgement_rule(self):
      self._fired_judgment_rule = True

    def production_utility_value(self, prod):
        return ar.spp(prod,":utility")[0][0]

    def production_u_value(self, prod):
        return ar.spp(prod,":u")[0][0]

    def clear_maze(self):
        self.is_found = True

    def got_bored(self):
        self.is_fun = False

    def visit_points(self,points, description=""):
        if points is None: return
        for point in points:
          self.__visit__point(point)

    def __visit__point(self,current_num, description=""):
        self._path.append(current_num)
        current_point = list(filter(lambda cp: cp.no == current_num, self.maze_env.conner_points))[0]
        self.count_map[current_point.y, current_point.x] += 1

    def debug_print(self, description):
        pass

    def terminate(self):
        ar.schedule_break_relative(0.01)
        ar.clear_buffer('imaginal')
        ar.clear_buffer('retrieval')
        ar.goal_focus('stack-goal')
    
    def get_reward_value(self):
      return self._reward_value

# Including exterior walls
# Actual sizes are 5x5, 7x7, 9x9
maze_difficulties = [(7,7),(9,9),(11,11)]

def generate_env(num):
    maze = mwe.MazeWallExtended()
    for d in maze_difficulties:
        width = d[0]
        height = d[1]
        dir_name = str(width) + "_" + str(height)
        if os.path.isdir(dir_name):
            continue

        os.makedirs(dir_name, exist_ok=True)
        for i in range(0, num):
            maze.create_maze(width, height)
            with open("{}\{:03d}.csv".format(dir_name, i),mode='w', newline="") as f:
                writer = csv.writer(f)
                for row in maze.maze_map:
                    writer.writerow(row)

# random model: random.lisp
# DFS model: backtrack.lisp
# DFS+IBL model: instance-base.lisp
def load_model(model_path = "ACT-R:model;instance-base.lisp"):
    ar.load_act_r_model (model_path)

def train(prefix):
    trial_num = 1
    reward_min_num = 2
    additional_reward = 4
    reward_step = 5
    limit_time_sec = 180
    limit_total_sec = 3600

    maze_table = []
    maze_env = mwe.MazeWallExtended()
    for d in maze_difficulties:
        width = d[0]
        height = d[1]
        dir_name = str(width) + "_" + str(height)
        cnt = 0
        mazes = []
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
        maze_table.append(mazes)

    env = Maze(prefix)
    load_model()
    for ms in maze_table:
        cnt = 0
        for m in ms:
            maze_env.load_maze(m)
            env.run(str(maze_env.width) + "_" + str(maze_env.height), cnt, maze_env, trial_num, reward_min_num, additional_reward, reward_step, limit_time_sec, limit_total_sec)
            cnt += 1

if __name__ == '__main__':
    start = time.time()
    train('random') #Log name
    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")