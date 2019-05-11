from World import World

configuration = {
    'world_size' : (50, 50), # The world is a matrix, its shape is defined by world_size
    'land_maximum_capacity' : 50,  # maximum amount of grains a land can hold 
    'population' : 250,  # the number of people
    'percent_best_land': 0.5, # the percent of best land, which capcity == maximum_capacity.
}

# set up the model world
world = World(**configuration)
