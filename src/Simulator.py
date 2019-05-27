from World import World
from People import People
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import os
import getopt
import configparser

BASE_PATH = os.getcwd()

'''
load configuration file
'''
def load_config(id=None):
    cf = configparser.ConfigParser()
    if id is None:
        cf.read(f"{BASE_PATH}/src/default.conf")
    else:
        cf.read(f"{BASE_PATH}/data/{id}/config.conf")
    return cf

'''
load pre-exported netlogo data
'''
def load_netlogo_data(id: str):
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
    compare = False
    conf = load_config()['SETTINGS']
    help_massage = '''
        -h --help \t help info
        -c --clock [int]\t running times, default == 1000
        -g --Nograph\t Do not generate graph results with this parameter
        -i --id [int]\t Load a predefined configuration under <../data/> and compare. Otherwise it 
                        will load the default.conf
    '''
    # read options from command line
    try:
        opts, _ = getopt.getopt(argv, "hgc:i:", ["help", "Nograph", "clock", "id"])
    except getopt.GetoptError:
        print(help_massage)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(help_massage)
            sys.exit()
        elif opt in ('-c', '--clock'):
            conf['MAXIMUM_CLOCK'] = arg
        elif opt in ('-g', '--graph'):
            save_graph_flag = False
            folder = os.path.exists(f'{BASE_PATH}/src/graph')
            if not folder:
                os.makedirs(f'{BASE_PATH}/src/graph')  
        elif opt in ('-i', '--id'):
            conf = load_config(arg)['SETTINGS']
            p_gini, p_poor, p_middle, p_rich = load_netlogo_data(arg)
            compare = True
            save_graph_flag = True 

    # Initial world
    if compare:
        conf['MAXIMUM_CLOCK'] = str(len(p_gini)-1)
    
    print('Initialize World...')
    world = World(conf)
    print('Initialize Successful!\nStart Simulation...')
    # start simulation
    lorenz_result, gini_results, rich, middle, poor = world.simulate()
    print('Simulation Successful!')
    # store lorenz points in csv
    with open(f'{BASE_PATH}/src/lorenz_result.csv', 'w') as lorenz:
        csv_writer = csv.writer(lorenz)
        for key, value in lorenz_result.items():
            csv_writer.writerow([key, value])
    # store gini result in csv
    with open(f'{BASE_PATH}/src/result.csv', 'w') as gini:
        csv_writer = csv.writer(gini)
        csv_writer.writerow(gini_results)
        csv_writer.writerow(rich)
        csv_writer.writerow(middle)
        csv_writer.writerow(poor)
    
    # generate graph
    if save_graph_flag:
        print('Saving Graph')
        axis_x = np.arange(int(conf['MAXIMUM_CLOCK'])+1)
        # generate Gini Index graph
        plt.plot(axis_x, gini_results)
        if compare:
            plt.plot(axis_x, p_gini, ':') 
        plt.ylim(0, 1)
        plt.xlabel('Time')
        plt.ylabel('Gini Index')
        plt.savefig(f'{BASE_PATH}/src/graph/gini_index.png')
        plt.cla()

        # generate people group graph
        plt.plot(axis_x, rich, color='b')
        plt.plot(axis_x, middle, color='y')
        plt.plot(axis_x, poor, color='r')
        if compare:
            plt.plot(axis_x, p_rich, 'b:')
            plt.plot(axis_x, p_middle, 'y:') 
            plt.plot(axis_x, p_poor, 'r:')
        plt.xlabel('Time')
        plt.ylabel('Gini Index')
        plt.savefig(f'{BASE_PATH}/src/graph/class_plot.png')
        plt.cla()

        # generate Lorenz curve graph
        for i in range(0, int(conf['MAXIMUM_CLOCK'])+1,100):
            x = np.arange(0, 100.0, 100.0/int(conf['NUM_PEOPLE']))
            plt.plot(x, lorenz_result[i], color='red')
            plt.plot(x, x, linestyle='--')
            plt.savefig(f'{BASE_PATH}/src/graph/lorenz_{i}.png')
            plt.cla()


if __name__ == "__main__":
    simulator(sys.argv[1:])