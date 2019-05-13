from World import World
from People import People
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    configuration = {
        'world_size' : (50, 50), # The world is a matrix, its shape is defined by world_size
        'land_maximum_capacity' : 50,  # maximum amount of grains a land can hold 
        'population' : 250,  # the number of people
        'percent_best_land': 0.5, # the percent of best land, which capcity == maximum_capacity.
        'num_grain_grown': 10, # if a patch does not have it's maximum amount of grain, add num-grain-grown to its grain amount
        'people_configuration': {
            'maximum_life_expectancy': 80,
            'maximum_metabolism': 15,
            'maximum_vision': 10,
        },
    }
    # threads pool
    threads = []

    # initial thread
    world = World('world', **configuration)
    peoples = world.peoples
    # start thread
    world.start()
    for people in peoples.values():
        people.start()

    # add threads into threads_pool
    threads.append(world)
    threads.extend(peoples.values())

    for thread in threads:
        thread.join()

    x = world.lorenz_points
    plt.plot(range(len(x)),x)
    plt.show()

