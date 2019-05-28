import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import csv
import getopt
import configparser

from World import World
from People import People
from WorldExtension import WorldExtension

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def simulator(argv):
    save_lorenz_curze_graph = False
    compare_netlogo = False
    compare_extend_world = False
    help_massage = '''
        -h --help \t\t help info
        -c --clock [int]\t running times, default == 1000
        -l --lorenz [int]\t save lorenz graph, The var is the step when store
        -i --id [int]\t\t Load a predefined configuration under <../data/> and compare.
        \t\t\t Otherwise it will load the default.conf
        -e --extend \t\t Compare the result of original and extend model
    '''

    # load default configuration
    conf = load_config()['SETTINGS']

    # read options from command line
    try:
        opts, _ = getopt.getopt(argv, "hl:c:i:e", ["help", "lorenz", "clock", "id", "extend"])
    except getopt.GetoptError:
        print(help_massage)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(help_massage)
            sys.exit()
        elif opt in ('-c', '--clock'):
            conf['MAXIMUM_CLOCK'] = arg
        elif opt in ('-l', '--lorenz'):
            save_lorenz_curze_graph = True
        elif opt in ('-i', '--id'):
            conf = load_config(arg)['SETTINGS']
            netlogo_data = load_netlogo_data(arg)
            compare_netlogo = True
        elif opt in ('-e', '--extend'):
            compare_extend_world = True

    # if compare with the netlogo data, the max ticket depends on the given data
    if compare_netlogo:
        conf['MAXIMUM_CLOCK'] = str(len(netlogo_data['gini'])-1)
    # Originial Model ------------------------------------
    print('Initialize World...')
    world = World(conf)
    print('Initialize Successful!\nStart Simulation...')
    lorenz_result, gini_results, rich, middle, poor = world.simulate()
    print('Simulation Successful!')
    # store result in csv
    store_csv('lorenz_result', *lorenz_result)
    store_csv('result', gini_results, rich, middle, poor)
    original = {
        'clock' : int(conf['MAXIMUM_CLOCK']),
        'num_people' :  int(conf['NUM_PEOPLE']),
        'gini' : gini_results,
        'rich' : rich,
        'middle' : middle,
        'poor' : poor,
        'lorenz_result' : lorenz_result,
        'lorenz' : save_lorenz_curze_graph
    }
    if compare_netlogo:
        save_graph(original, netlogo_data)
    elif compare_extend_world:
        print('Initialize Extend World...')
        extend_world = WorldExtension(conf)
        print('Initialize Successful!\nStart Extend Simulation...')
        extend_lorenz, extend_gini, extend_rich, extend_middle, extend_poor = extend_world.simulate()
        print('Simulation Successful!')
        # store result 
        store_csv('extend_lorenz_result', *extend_lorenz)
        store_csv('extend_result', extend_gini, extend_rich, extend_middle, extend_poor)
        extend = {
            'clock' : int(conf['MAXIMUM_CLOCK']),
            'num_people' :  int(conf['NUM_PEOPLE']),
            'gini' : extend_gini,
            'rich' : extend_rich,
            'middle' : extend_middle,
            'poor' : extend_poor,
            'lorenz_result' : lorenz_result,
            'lorenz' : save_lorenz_curze_graph 
        }
        save_graph(extend, original)
    else:
        save_graph(original)

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
    
    return {
        'gini' : gini,
        'rich' : rich,
        'middle' : middle,
        'poor' : poor
    }

def store_csv(des, *arg):
    folder = os.path.exists(f'{BASE_PATH}/src/result')
    if not folder:
        os.makedirs(f'{BASE_PATH}/src/result')  
    with open(f'{BASE_PATH}/src/result/{des}.csv', 'w') as f:
        csv_writer = csv.writer(f)
        for row in arg:
            csv_writer.writerow(row)

def save_graph(new : dict, old=None):
    print('Saving Graph')

    axis_x = np.arange(new['clock'] + 1)
    # generate Gini Index graph
    plt.plot(axis_x, new['gini'])
    if old is not None:
        plt.plot(axis_x, old['gini'], ':') 
    plt.ylim(0, 1)
    plt.xlabel('Time')
    plt.ylabel('Gini Index')
    plt.savefig(f'{BASE_PATH}/src/result/gini_index.png')
    plt.cla()

    # generate people group graph
    plt.plot(axis_x, new['rich'], color='b')
    plt.plot(axis_x, new['middle'], color='y')
    plt.plot(axis_x, new['poor'], color='r')
    if old is not None:
        plt.plot(axis_x, old['rich'], 'b:')
        plt.plot(axis_x, old['middle'], 'y:') 
        plt.plot(axis_x, old['poor'], 'r:')
    plt.xlabel('Time')
    plt.ylabel('Num of People')
    plt.savefig(f'{BASE_PATH}/src/result/class_plot.png')
    plt.cla()

    # generate Lorenz curve graph
    if new['lorenz']:
        for i in range(0, new['clock'] + 1,100):
            axis_x = np.arange(0, 100.0, 100.0/new['num_people'])
            plt.plot(axis_x, new['lorenz_result'][i], color='red')
            plt.plot(axis_x, axis_x, linestyle='--')
            plt.savefig(f'{BASE_PATH}/src/result/lorenz_{i}.png')
            plt.cla()


if __name__ == "__main__":
    simulator(sys.argv[1:])