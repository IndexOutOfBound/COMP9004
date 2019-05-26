from World import World
from People import People
import numpy as np
import sys
import csv

class Experiment(object):
    def __init__(self, loop : int, step : int):
        self.results = []
        self.loop_num = int(loop)
        self.step = int(step)
        self.conf = {
            'MAXIMUM_CLOCK' : 1000,
            'WORLD_SIZE_X' : 51,
            'WORLD_SIZE_Y' : 51,
            'LAND_MAXIMUM_CAPACITY' : 50,
            'NUM_PEOPLE' : 250,
            'LIFE_EXPECTANCY_MIN' : 100,
            'LIFE_EXPECTANCY_MAX' : 100,
            'MAX_VISION' : 1,
            'METABOLISM_MAX' : 25,
            'PERSENT_BEST_LAND' : 5,
            'GRAIN_GROWTH_INTERVAL' : 10,
            'NUM_GRAIN_GROWN' : 1,
        }
        self.conf_end = {
            'MAX_VISION' : 16,
            'METABOLISM_MAX' : 0,
            'PERSENT_BEST_LAND' : 26,
            'GRAIN_GROWTH_INTERVAL' : 0,
            'NUM_GRAIN_GROWN' : 11,
        }
        self.conf_start = {
            'MAX_VISION' : 1,
            'METABOLISM_MAX' : 25,
            'PERSENT_BEST_LAND' : 5,
            'GRAIN_GROWTH_INTERVAL' : 10,
            'NUM_GRAIN_GROWN' : 1
        }
    
    def run(self):
        print('Start Experiment')
        self.__loop('NUM_GRAIN_GROWN')
        self.__loop('GRAIN_GROWTH_INTERVAL')
        self.__loop('PERSENT_BEST_LAND')
        self.__loop('MAX_VISION')
        self.__loop('METABOLISM_MAX')
        return self.results

    def __loop(self, key: str) -> tuple:
        step = self.step
        if self.conf_start[key] > self.conf_end[key]:
            step = -1 * self.step
      
        print(f'\033[33m {key} ------- \033[0m')
        for i in range(self.conf_start[key], self.conf_end[key], step):
            print(f'{key}={i}')
            tmp_gini = []
            for _ in range(self.loop_num):
                self.conf[key] = i
                world = World(self.conf)
                _, gini_results, _, _, _ = world.simulate()
                avg_gini = np.average(gini_results[-200:])
                tmp_gini.append(avg_gini)
                print(avg_gini)
            config = list(self.conf.values())
            config.append(np.average(tmp_gini))
            self.results.append(config) 

    # def __reverse_loop(self, key: str) -> tuple:
    #     print(f'\033[33m {key} ------- \033[0m')
    #     for i in range(self.conf_max[key], 0, -1):
    #         tmp_gini = []
    #         for _ in range(self.loop_num):
    #             self.conf[key] = i
    #             world = World(self.conf)
    #             _, gini_results, _, _, _ = world.simulate()
    #             tmp_gini.append(gini_results[-1])
    #             avg_gini = np.average(gini_results[-200:])
    #             tmp_gini.append(avg_gini)
    #             print(gini_results[-1])
    #         config = list(self.conf.values())
    #         config.append(np.average(tmp_gini))
    #         self.results.append(config)  

if __name__ == "__main__":
    experimenter = Experiment(sys.argv[1], sys.argv[2])
    results = experimenter.run()

    with open('experiment_data.csv', 'w') as f:
        csv_writer = csv.writer(f)
        for config in results:
            csv_writer.writerow(config)
