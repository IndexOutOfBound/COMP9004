from World import World
from People import People
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import os
import getopt

configuration = {
    'maximum_clock': 100,
    'world_size' : (50, 50), # The world is a matrix, its shape is defined by world_size
    'land_maximum_capacity' : 50,  # maximum amount of grains a land can hold 
    'population' : 200,  # the number of people
    'percent_best_land': 0.1, # the percent of best land, which capcity == maximum_capacity.
    'num_grain_grown': 10, # if a patch does not have it's maximum amount of grain, add num-grain-grown to its grain amount
    'grain_growth_interval': 10,
    'people_configuration': {
        'min_life_expectancy': 1,
        'max_life_expectancy': 80,
        'max_metabolism': 15,
        'max_vision': 5,
    },
}

def simulator(argv, **configuration):
    save_graph_flag = False
    try:
        opts, _ = getopt.getopt(argv, "hgc:", ["help", "graph", "clock"])
    except getopt.GetoptError:
        print('-h --help \t help info')
        print('-c --clock \t running times, default == 100')
        print('-g --graph=\t Generate graph results with this parameter')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('-h --help \t help info')
            print('-c --clock \t running times, default == 100')
            print('-g --graph \t Generate graph results with this parameter')
            sys.exit()
        elif opt in ('-c', '--clock'):
            configuration['maximum_clock'] = int(arg)
        elif opt in ('-g', '--graph'):
            save_graph_flag = True
            folder = os.path.exists('./graph')
            if not folder:
                os.makedirs('./graph')  
                
    # initial
    world = World(**configuration)
    # start simulation
    lorenz_result, gini_results = world.simulate()
    with open('lorenz_result.csv', 'w') as lorenz:
        csv_writer = csv.writer(lorenz)
        for key, value in lorenz_result.items():
            csv_writer.writerow([key, value])

    with open('gini_result.csv', 'w') as gini:
        csv_writer = csv.writer(gini)
        csv_writer.writerow(gini_results)

    if save_graph_flag:
        print('Saving Graph')
        plt.plot(np.arange(configuration['maximum_clock']+1), gini_results)
        plt.ylim(0, 1)
        plt.xlabel('Time')
        plt.ylabel('Gini Index')
        plt.savefig('./graph/gini_index.jpg')
        plt.close()

        for i in range(0, configuration['maximum_clock'],10):
            x = np.arange(0, 100.0, 100.0/configuration['population'])
            plt.plot(x, lorenz_result[i], color='red')
            plt.plot(x, x, linestyle='--')
            plt.savefig(f'./graph/lorenz_{i}.jpg')
            plt.cla()


if __name__ == "__main__":
    simulator(sys.argv[1:], **configuration)