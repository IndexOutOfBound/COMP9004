from World import World
from People import People
import numpy as np
import sys
import csv

from WorldExtension import WorldExtension


class Experiment(object):
    def __init__(self, loop : int):
        self.results = []
        self.loop_num = int(loop)
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
            'INHERITANCE_RATE' : 0.8,
            'GENETIC' : 0.8,
            'SUMMER_INTERVAL' : 100,
            'RECLAMATION_INTERVAL' : 100
        }

        self.conf_max = {
            'MAX_VISION' : 15,
            'METABOLISM_MAX' : 25,
            'PERSENT_BEST_LAND' : 25,
            'GRAIN_GROWTH_INTERVAL' : 10,
            'NUM_GRAIN_GROWN' : 10,
            'INHERITANCE_RATE': 1,
            'GENETIC': 1,
            'SUMMER_INTERVAL': 75,
            'RECLAMATION_INTERVAL': 100

        }
        self.conf_min = {
            'MAX_VISION' : 1,
            'METABOLISM_MAX' : 1,
            'PERSENT_BEST_LAND' : 5,
            'GRAIN_GROWTH_INTERVAL' : 1,
            'NUM_GRAIN_GROWN' : 1,
            'INHERITANCE_RATE': 0,
            'GENETIC': 0,
            'SUMMER_INTERVAL': 25,
            'RECLAMATION_INTERVAL': 25
        }
    
    def run(self):
        print('Start Experiment')
        print('Change NUM_GRAIN_GROWN')
        self.__loop('NUM_GRAIN_GROWN')
        self.__reverse_loop('GRAIN_GROWTH_INTERVAL')
        self.__loop('PERSENT_BEST_LAND')
        self.__loop('MAX_VISION')
        self.__reverse_loop('METABOLISM_MAX')
        self.__loop('INHERITANCE_RATE')
        self.__loop('SUMMER_INTERVAL')
        self.__reverse_loop('RECLAMATION_INTERVAL')
        return self.results

    def __loop(self, key: str) -> tuple:
        print(f'\033[33m {key} ------- \033[0m')
        for i in range(self.conf_min[key], self.conf_max[key]+1, 1):
            tmp_gini = []
            for _ in range(self.loop_num):
                self.conf[key] = i
                world = World(self.conf)
                _, gini_results, _, _, _ = world.simulate()
                avg_gini = np.average(gini_results[-200:])
                tmp_gini.append(avg_gini)
            config = list(self.conf.values())
            config.append(np.average(tmp_gini))
            self.results.append(config) 

    def __reverse_loop(self, key: str) -> tuple:
        print(f'\033[33m {key} ------- \033[0m')
        for i in range(self.conf_max[key], 0, -1):
            tmp_gini = []
            for _ in range(self.loop_num):
                self.conf[key] = i
                world = World(self.conf)
                _, gini_results, _, _, _ = world.simulate()
                tmp_gini.append(gini_results[-1])
                print(gini_results[-1])
            config = list(self.conf.values())
            config.append(np.average(tmp_gini))
            self.results.append(config)  

if __name__ == "__main__":
    experimenter = Experiment(sys.argv[1])
    results = experimenter.run()

    with open('experiment_data.csv', 'w') as f:
        csv_writer = csv.writer(f)
        for config in results:
            csv_writer.writerow(config)
