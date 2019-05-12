from World import World
import matplotlib.pyplot as plt
import numpy as np

configuration = {
    'world_size' : (50, 50), # The world is a matrix, its shape is defined by world_size
    'land_maximum_capacity' : 50,  # maximum amount of grains a land can hold 
    'population' : 250,  # the number of people
    'percent_best_land': 0.5, # the percent of best land, which capcity == maximum_capacity.
    'people_configuration': {
        'maximum_life_expectancy': 80,
        'maximum_metabolism': 15,
        'maximum_vision': 10,
    },
}

# set up the model world
world = World(**configuration)
x = world.lorenz_points
plt.plot(range(len(x)),x)
plt.show()

