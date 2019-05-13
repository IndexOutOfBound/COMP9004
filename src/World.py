import numpy as np
import threading
import queue
from People import People

class World(object):
    def __init__(self, **kwargs):
        # TODO: set up a config file or input via command
        # Set up global parmeters
        self.land_maximum_capacity = kwargs['land_maximum_capacity']    
        self.world_size = kwargs['world_size']      
        self.population = kwargs['population']  
        self.percent_best_land = kwargs['percent_best_land']  
        self.num_grain_grown = kwargs['num_grain_grown'] 
        self.grain_growth_interval = kwargs['grain_growth_interval']
        self.maximum_clock = kwargs['maximum_clock']
        self.people_config = kwargs['people_configuration']
        self.clock = 0
        # set up various parts of the world
        # generate the worlds
        # random define each land's maximum capacity
        self.maximum_grains = self.__setup_lands__capacity()
        # set up the initial grains distribution eaqual to maximum
        self.grains_distribution = self.maximum_grains.copy()
        # random ditribute people in the world
        self.peoples = self.__setup_people()
        # Initial lorenz and gini
        self.lorenz_points, self.gini_index = self.update_lorenz_and_gini()

        
    '''
        This method will generate a matrix. each value will be the related land's capacity.
    '''
    def __setup_lands__capacity(self):
        world_capacity = self.world_size[0] * self.world_size[1]
        best_land_number =  int(world_capacity * self.percent_best_land)
        land_value_range = np.random.randint(0, self.land_maximum_capacity, size=world_capacity-best_land_number)
        flatten_wolrd = np.append(land_value_range, [self.land_maximum_capacity]*best_land_number)
        maximum_grains = np.random.permutation(flatten_wolrd).reshape(self.world_size)
        return maximum_grains

    '''
        generate N people
    '''
    def __setup_people(self, ):
        peoples = {}
        # peoples_matrix: [[id, wealth, age, metabolism, life_expectancy, vision, axis_x, axis_y],]
        peoples_matrix = self.__generate_peoples()
        for i in range(peoples_matrix.shape[0]):
            peoples[i] = People(self, *peoples_matrix[i])
        return peoples

    def __generate_peoples(self):
        ids = np.arange(self.population)
        ages = np.zeros(self.population, dtype=int)
        metabolism = np.random.randint(1, self.people_config['max_metabolism'], size=self.population)
        life_expectancy = np.random.randint(self.people_config['min_life_expectancy'], self.people_config['max_life_expectancy']+1, size=self.population)
        vision = np.random.randint(1, self.people_config['max_vision']+1, size=self.population) 
        wealth = metabolism + np.random.randint(0, 50, size=self.population)
        axis_x = np.random.randint(0, self.world_size[0], size=self.population)
        axis_y = np.random.randint(0, self.world_size[1], size=self.population)
        matrix = np.array((ids, wealth, ages, metabolism, life_expectancy, vision, axis_x, axis_y))
        return matrix.T 

    def update_lorenz_and_gini(self):
        # sort wealth
        sorted_wealth = sorted(self.peoples.items(), key= lambda x:x[1].wealth)
        total_wealth = 0
        for id in range(self.population):
            total_wealth += self.peoples[id].wealth

        wealth_sum_so_far = 0
        gini_index_reserve = 0
        lorenz_points = []
        for i, people in enumerate(sorted_wealth):
            wealth_sum_so_far += people[1].wealth
            lorenz_points.append((wealth_sum_so_far/total_wealth)*100)
            gini_index_reserve += (i+1)/self.population - wealth_sum_so_far/total_wealth

        # gini_index = gini_index_reserve/(gini_index_reserve + np.sum(lorenz_points))
        gini_index = (gini_index_reserve / self.population) / 0.5
        return lorenz_points, gini_index

    def grain_grow(self):
        if self.clock % self.grain_growth_interval == 0:
            self.grains_distribution += self.num_grain_grown
            self.grains_distribution = np.minimum(self.grains_distribution, self.maximum_grains)

    def step(self):
        location_index = {}
        for people in self.peoples.values():
            people.turn_towards_grain()
            # breakpoint()
            location_index[(people.axis_x, people.axis_y)] = location_index.get((people.axis_x, people.axis_y), 0) + 1
            # breakpoint()

            
        for people in self.peoples.values():
            people.wealth += self.grains_distribution[people.axis_x, people.axis_y] / location_index[(people.axis_x, people.axis_y)]
            people.move_eat_age_die()

        self.grain_grow()
        
    def simulate(self):
        print('Start Simulation')
        lorenz_results = {}
        gini_results = []
        while self.clock <= self.maximum_clock:
            self.step()
            lorenz_points, gini_index = self.update_lorenz_and_gini()
            lorenz_results[self.clock] = lorenz_points
            gini_results.append(gini_index)
            self.clock += 1
        print('Simulation Finished')
        return lorenz_results, gini_results

