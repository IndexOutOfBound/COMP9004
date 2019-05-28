from World import World
from People import People

import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import os
import getopt
import configparser

from WorldExtension import WorldExtension


def load_config(id=None):
    cf = configparser.ConfigParser()
    if id is None:
        cf.read("./default.conf")
    else:
        cf.read(f"../data/{id}/config.conf")
    return cf


def load_netlogo_data(id):
    # load gini index
    gini, poor, middle, rich = [], [], [], []
    with open(f"../data/{id}/gini_index.csv") as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            gini.append(float(row[1]))
    # load number of each groups 
    with open(f"../data/{id}/people_num.csv") as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            poor.append(int(row[1]))
            middle.append(int(row[5]))
            rich.append(int(row[9]))
    
    return gini, poor, middle, rich    
    
    
def simulator(argv):
    save_graph_flag = True
    compare_netlog = False
    conf = load_config()['SETTINGS']
    save_graph_flag = True
    compare_extend_world = True

    setting = {}
    for h in range(1, 11):
        setting['INHERITANCE_RATE'] = 0.5 + h * 0.05
        for m in range(1, 11):
            setting["GENETIC"] = 0.5 + m * 0.05
            for n in range(0, 100, 10):
                setting['SUMMER_INTERVAL'] = n
                for z in range(10, 100, 10):
                    setting['RECLAMATION_INTERVAL'] = z
                    conf['MAXIMUM_CLOCK'] = 500
                    world = World(conf)
                    extensionWorld = WorldExtension(conf)
                    total_lorenz, total_gini, total_rich, total_middle, total_poor = extensionWorld.simulate()
                    for i in range(0, 99):
                        world = World(conf)
                        extensionWorld = WorldExtension(world, conf)
                        lorenz, gini, rich, middle, poor = extensionWorld.simulate()
                        total_lorenz = [x + y for x, y in zip(total_lorenz, lorenz)]
                        total_gini = [x + y for x, y in zip(total_gini, gini)]
                        total_rich = [x + y for x, y in zip(total_rich, rich)]
                        total_middle = [x + y for x, y in zip(total_middle, middle)]
                        total_poor = [x + y for x, y in zip(total_poor, poor)]
                    lorenz = [c/100 for c in total_lorenz ]
                    gini = [c / 100 for c in total_gini]
                    rich = [c / 100 for c in total_rich]
                    middle = [c / 100 for c in total_middle]
                    poor = [c / 100 for c in total_poor]
                    result = {}
                    result['']
                    generate_graph_without_compare(conf, result)

    # start simulation
    # lorenz_result, gini_results, rich, middle, poor = world.simulate()

    # store_data(lorenz_result, gini_results, rich, middle, poor, 'lorenz_result.csv', 'result.csv')
    store_data(extend_lorenz, extend_gini, extend_rich, extend_middle, extend_poor, 'extend_lorenz_result.csv', 'extend_result.csv')








def store_data(lorenz_result, gini_results, rich, middle, poor, lorenz_path, result_path):
    # store lorenz points in csv
    with open(lorenz_path, 'w') as lorenz:
        csv_writer = csv.writer(lorenz)
        for key, value in lorenz_result.items():
            csv_writer.writerow([key, value])
    # store gini result in csv
    with open(result_path, 'w') as gini:
        csv_writer = csv.writer(gini)
        csv_writer.writerow(gini_results)
        csv_writer.writerow(rich)
        csv_writer.writerow(middle)
        csv_writer.writerow(poor)

def generate_graph_without_compare(conf, simulate_result, ):
    # generate graph
        print('Saving Graph')
        axis_x = np.arange(int(conf['MAXIMUM_CLOCK'])+1)
        # generate Gini Index graph
        plt.plot(axis_x, simulate_result['gini'])
        plt.ylim(0, 1)
        plt.xlabel('Time')
        plt.ylabel('Gini Index')
        plt.savefig('./graph/gini_index.png')
        plt.cla()

        # generate people group graph
        plt.plot(axis_x, simulate_result['rich'], color='b')
        plt.plot(axis_x, simulate_result['middle'], color='y')
        plt.plot(axis_x, simulate_result['poor'], color='r')
        plt.xlabel('Time')
        plt.ylabel('Gini Index')
        plt.savefig('./graph/class_plot.png')
        plt.cla()


def generate_graph(conf, simulate_result, original_result ):
    # generate graph
    print('Saving Graph')
    axis_x = np.arange(int(conf['MAXIMUM_CLOCK']) + 1)
    # generate Gini Index graph
    plt.plot(axis_x, simulate_result['gini'])
    plt.plot(axis_x, original_result['gini'], ':')
    plt.ylim(0, 1)
    plt.xlabel('Time')
    plt.ylabel('Gini Index')
    plt.savefig('./graph/gini_index.png')
    plt.cla()

    # generate people group graph
    plt.plot(axis_x, simulate_result['rich'], color='b')
    plt.plot(axis_x, simulate_result['middle'], color='y')
    plt.plot(axis_x, simulate_result['poor'], color='r')
    plt.plot(axis_x, original_result['rich'], 'b:')
    plt.plot(axis_x, original_result['middle'], 'y:')
    plt.plot(axis_x, original_result['poor'], 'r:')
    plt.xlabel('Time')
    plt.ylabel('Gini Index')
    plt.savefig('./graph/class_plot.png')
    plt.cla()

        # # generate Lorenz curve graph
        # for i in range(0, int(conf['MAXIMUM_CLOCK']),10):
        #     x = np.arange(0, 100.0, 100.0/int(conf['NUM_PEOPLE']))
        #     plt.plot(x, lorenz_result[i], color='red')
        #     plt.plot(x, x, linestyle='--')
        #     plt.savefig(f'./graph/lorenz_{i}.png')
        #     plt.cla()


if __name__ == "__main__":
    # load_netlogo_data('01')

    simulator(sys.argv[1:])