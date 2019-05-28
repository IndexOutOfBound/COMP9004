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

BASE_PATH = os.getcwd()

def load_config(id=None):
    cf = configparser.ConfigParser()
    if id is None:
        cf.read(f"{BASE_PATH}/src/default.conf")
    else:
        cf.read(f"{BASE_PATH}/data/{id}/config.conf")
    return cf


def load_netlogo_data(id):
    # load gini index
    gini, poor, middle, rich = [], [], [], []
    with open(f"{BASE_PATH}/data/{id}/gini_index.csv") as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            gini.append(float(row[1]))
    # load number of each groups 
    with open(f"{BASE_PATH}/data/{id}/people_num.csv") as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            poor.append(int(row[1]))
            middle.append(int(row[5]))
            rich.append(int(row[9]))
    
    return gini, poor, middle, rich    
    
    
def simulator(argv):
    save_graph_flag = True
    compare_netlog = False
    compare_extend_world = False
    conf = load_config()['SETTINGS']

    # read options from command line
    try:
        opts, _ = getopt.getopt(argv, "hgc:i:e:", ["help", "Nograph", "clock", "id", "extend"])
    except getopt.GetoptError:
        print('-h --help \t help info')
        print('-c --clock [int]\t running times, default == 100')
        print('-g --Nograph\t Do not generate graph results with this parameter')
        print('-i --id [int]\t Load a predefined configuration and compare with netlog result')
        print('-e --extend [int]\t Compare the result of original and extend world based on a predefined configuration.')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('-h --help \t help info')
            print('-c --clock [int]\t running times, default == 100')
            print('-g --graph \t Do not generate graph results with this parameter')
            print('-i --id [int]\t Load a predefined configuration and compare')
            print('-e --extend [int]\t Compare the result of original and extend world based on a predefined configuration.')
            sys.exit()
        elif opt in ('-c', '--clock'):
            conf['MAXIMUM_CLOCK'] = arg
        elif opt in ('-g', '--graph'):
            save_graph_flag = False
            folder = os.path.exists('./graph')
            if not folder:
                os.makedirs('./graph')  
        elif opt in ('-i', '--id'):
            conf = load_config(arg)['SETTINGS']
            p_gini, p_poor, p_middle, p_rich = load_netlogo_data(arg)
            compare_netlog = True
            save_graph_flag = True
            compare_extend_world = False
        elif opt in ('-e', '--extend'):
            conf = load_config(arg)['SETTINGS']
            compare_netlog = False
            save_graph_flag = True
            compare_extend_world = True


    # Initial world
    if compare_netlog or compare_extend_world:
        conf['MAXIMUM_CLOCK'] = str(500)

    world = World(conf)

    extensionWorld = WorldExtension(conf)
    # start simulation
    lorenz_result, gini_results, rich, middle, poor = world.simulate()

    extend_lorenz, extend_gini, extend_rich, extend_middle, extend_poor = extensionWorld.simulate()
    store_data(lorenz_result, gini_results, rich, middle, poor, 'lorenz_result.csv', 'result.csv')
    store_data(extend_lorenz, extend_gini, extend_rich, extend_middle, extend_poor, 'extend_lorenz_result.csv', 'extend_result.csv')
    if save_graph_flag:

        extend_result = {}
        extend_result['lorenz'] = extend_lorenz
        extend_result['gini'] = extend_gini
        extend_result['rich'] = extend_rich
        extend_result['middle'] = extend_middle
        extend_result['poor'] = extend_poor


        if compare_netlog:
            netlog_result= {}
            netlog_result['gini'] = p_gini
            netlog_result['poor'] = p_poor
            netlog_result['middle'] = p_middle
            netlog_result['rich'] = p_rich
            generate_graph(conf, extend_result, netlog_result)


        if compare_extend_world:
            original_result = {}
            original_result['gini'] = gini_results
            original_result['poor'] =  poor
            original_result['middle'] = middle
            original_result['rich'] = rich
            generate_graph(conf, extend_result, original_result)

        if (not compare_netlog) and (not compare_extend_world):
            generate_graph_without_compare(conf, extend_result)






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

def generate_graph_without_compare(conf, simulate_result):
    # generate graph
    print('Saving Graph')
    axis_x = np.arange(int(conf['MAXIMUM_CLOCK'])+1)
    # generate Gini Index graph
    plt.plot(axis_x, simulate_result['gini'])
    plt.ylim(0, 1)
    plt.xlabel('Time')
    plt.ylabel('Gini Index')
    plt.savefig(f'{BASE_PATH}/src/graph/gini_index.png')
    plt.cla()

    # generate people group graph
    plt.plot(axis_x, simulate_result['rich'], color='b')
    plt.plot(axis_x, simulate_result['middle'], color='y')
    plt.plot(axis_x, simulate_result['poor'], color='r')
    plt.xlabel('Time')
    plt.ylabel('Gini Index')
    plt.savefig(f'{BASE_PATH}/src/graph/class_plot.png')
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
    plt.savefig(f'{BASE_PATH}/src/graph/gini_index.png')
    plt.cla()

    # generate people group graph
    plt.plot(axis_x, simulate_result['rich'], color='b')
    plt.plot(axis_x, simulate_result['middle'], color='y')
    plt.plot(axis_x, simulate_result['poor'], color='r')
    plt.plot(axis_x, original_result['rich'], 'b:')
    plt.plot(axis_x, original_result['middle'], 'y:')
    plt.plot(axis_x, original_result['poor'], 'r:')
    plt.xlabel('Time')
    plt.ylabel('People')
    plt.savefig(f'{BASE_PATH}/src/graph/class_plot.png')
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