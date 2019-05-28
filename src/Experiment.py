from World import World
from People import People
import numpy as np

class Experiment(object):
    '''
        This class will experiment the oringinal world
        @para
            - loop : [int] running times for each groups of parameters
            - step : [int] the step when a parameter change
    '''
    def __init__(self, loop : int, step : int):
        self.results = []
        self.loop_num = int(loop)
        self.step = int(step)
        # The initial state of parameters
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
        # The start and end for parameters
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
    
    # start experiment
    def run(self):
        print('Start Experiment')
        self.__loop('NUM_GRAIN_GROWN')
        self.__loop('GRAIN_GROWTH_INTERVAL')
        self.__loop('PERSENT_BEST_LAND')
        self.__loop('MAX_VISION')
        self.__loop('METABOLISM_MAX')
        return self.results

    def __loop(self, key: str):
        '''
            experiment one parameter
            @para:
                - key: [str] the parameter's name
        '''
        step = self.step
        if self.conf_start[key] > self.conf_end[key]:
            step = -1 * self.step
      
        print(f'\033[33m {key} ------- \033[0m')
        for i in range(self.conf_start[key], self.conf_end[key], step):
            print(f'{key}={i}')
            tmp_gini = []
            # each parameter will be executed self.loop_num times
            for _ in range(self.loop_num):
                self.conf[key] = i
                world = World(self.conf)
                _, gini_results, _, _, _ = world.simulate()
                # Using the average of the latest 200 tickets gini index 
                # as a single running's result
                avg_gini = np.average(gini_results[-200:])
                tmp_gini.append(avg_gini)
                print(avg_gini)
            config = list(self.conf.values())
            # use the average gini index as the eventually gini index for 
            # a specific configuration
            config.append(np.average(tmp_gini))
            self.results.append(config) 

if __name__ == "__main__":
    import sys
    import csv
    import getopt

    BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    argv = sys.argv[1:]
    help_message = '''
        -h --help \t\t help message 
        -l --loop [integer] \t running times for each group of parameters, default=1
        -s --step [integer] \t step for change parameter, default=1'''
    try:
        opts, _ = getopt.getopt(argv, "hl:s:", ["help","loop", "step"])
    except getopt.GetoptError:
        print(help_message)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(help_message)
            sys.exit()
        elif opt in ('-l', '--loop'):
            loop = int(arg)
        elif opt in ('-s', '--step'):
            step = int(arg)

    experimenter = Experiment(loop, step)
    results = experimenter.run()

    # Store the experiment result
    with open(f'{BASE_PATH}/src/experiment_data.csv', 'w') as f:
        csv_writer = csv.writer(f)
        for config in results:
            csv_writer.writerow(config)
