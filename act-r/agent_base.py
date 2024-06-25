import numpy as np
import math

class AgentBase():
    def _calc_entropy(self, count_map, conner_points, k=1):
        total_count = np.sum(count_map)
        entropy = 0
        for conner_point in conner_points:
            p = count_map[conner_point.y, conner_point.x] / total_count
            if p > 0:
                entropy += - p * math.log(p)

        return entropy * k
    
    def _calc_probabilities(self, count_map, conner_points):
        total_count = np.sum(count_map)
        probabilities = []
        for conner_point in conner_points:
            p = count_map[conner_point.y, conner_point.x] / total_count
            probabilities.append(p)

        return probabilities

if __name__ == '__main__':
    pass