from World import World
from People import People
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import os
import getopt
import configparser

# configuration = {
#     'maximum_clock': 111,
#     'world_size' : (50, 50), # The world is a matrix, its shape is defined by world_size
#     'land_maximum_capacity' : 50,  # maximum amount of grains a land can hold 
#     'population' : 250,  # the number of people
#     'percent_best_land': 0.1, # the percent of best land, which capcity == maximum_capacity.
#     'num_grain_grown': 10, # if a patch does not have it's maximum amount of grain, add num-grain-grown to its grain amount
#     'grain_growth_interval': 1,
#     'people_configuration': {
#         'min_life_expectancy': 1,
#         'max_life_expectancy': 80,
#         'max_metabolism': 15,
#         'max_vision': 5,
#     },
# }

def load_config(id=None):
    cf = configparser.ConfigParser()
    if id is None:
        cf.read("./default.conf")
    else:
        cf.read(f"../data/{id}/config.conf")
    return cf


def simulator(argv):
    save_graph_flag = False
    conf = load_config()['SETTINGS']
    try:
        opts, _ = getopt.getopt(argv, "hgc:i:", ["help", "graph", "clock", "id"])
    except getopt.GetoptError:
        print('-h --help \t help info')
        print('-c --clock [int]\t running times, default == 100')
        print('-g --graph\t Generate graph results with this parameter')
        print('-i --id [int]\t Load a predefined configuration' )
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('-h --help \t help info')
            print('-c --clock [int]\t running times, default == 100')
            print('-g --graph \t Generate graph results with this parameter')
            print('-i --id [int]\t Load a predefined configuration' )
            sys.exit()
        elif opt in ('-c', '--clock'):
            conf['MAXIMUM_CLOCK'] = arg
        elif opt in ('-g', '--graph'):
            save_graph_flag = True
            folder = os.path.exists('./graph')
            if not folder:
                os.makedirs('./graph')  
        elif opt in ('-i', '--id'):
            conf = load_config(arg)['SETTINGS']

    world = World(conf)
    # start simulation
    lorenz_result, gini_results = world.simulate()
    # store lorenz points in csv
    with open('lorenz_result.csv', 'w') as lorenz:
        csv_writer = csv.writer(lorenz)
        for key, value in lorenz_result.items():
            csv_writer.writerow([key, value])
    # store gini result in csv
    with open('gini_result.csv', 'w') as gini:
        csv_writer = csv.writer(gini)
        csv_writer.writerow(gini_results)
    
    # generate graph
    if save_graph_flag:
        print('Saving Graph')

        # generate Gini Index graph
        plt.plot(np.arange(int(conf['MAXIMUM_CLOCK'])+1), gini_results)
        plt.ylim(0, 1)
        plt.xlabel('Time')
        plt.ylabel('Gini Index')
        plt.savefig('./graph/gini_index.jpg')
        plt.close()

        # generate Lorenz curve graph
        for i in range(0, int(conf['MAXIMUM_CLOCK']),10):
            x = np.arange(0, 100.0, 100.0/int(conf['NUM_PEOPLE']))
            plt.plot(x, lorenz_result[i], color='red')
            plt.plot(x, x, linestyle='--')
            plt.savefig(f'./graph/lorenz_{i}.jpg')
            plt.cla()


if __name__ == "__main__":
    simulator(sys.argv[1:])