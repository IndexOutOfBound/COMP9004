import numpy as np
import threading
import queue
from People import People

class World(object):
    def __init__(self, conf):
        # load global parmeters
        self.MAXIMUM_CLOCK = int(conf['MAXIMUM_CLOCK'])
        self.WORLD_SIZE_X = int(conf['WORLD_SIZE_X'])
        self.WORLD_SIZE_Y = int(conf['WORLD_SIZE_Y'])
        self.WORLD_SIZE = self.WORLD_SIZE_X * self.WORLD_SIZE_Y
        self.LAND_MAXIMUM_CAPACITY = int(conf['LAND_MAXIMUM_CAPACITY'])
        self.NUM_PEOPLE = int(conf['NUM_PEOPLE'])
        self.MAX_VISION =int(conf['MAX_VISION']) 
        self.METABOLISM_MAX = int(conf['METABOLISM_MAX'])
        self.LIFE_EXPECTANCY_MIN = int(conf['LIFE_EXPECTANCY_MIN'])
        self.LIFE_EXPECTANCY_MAX = int(conf['LIFE_EXPECTANCY_MAX'])
        self.PERSENT_BEST_LAND = float(conf['PERSENT_BEST_LAND']) / 100
        self.GRAIN_GROWTH_INTERVAL = int(conf['GRAIN_GROWTH_INTERVAL'])
        self.NUM_GRAIN_GROWN = int(conf['NUM_GRAIN_GROWN'])
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
        self.lorenz_points, self.gini_index = self.__update_lorenz_and_gini()

        
    '''
        This method will generate a matrix. each value will be the related land's capacity.
    '''
    def __setup_lands__capacity(self):
        # world_capacity = self.WORLD_SIZE_X * self.WORLD_SIZE_Y
        best_land_number =  int(self.WORLD_SIZE * self.PERSENT_BEST_LAND)
        land_value_range = np.random.randint(0, self.LAND_MAXIMUM_CAPACITY, size=self.WORLD_SIZE-best_land_number)
        flatten_wolrd = np.append(land_value_range, [self.LAND_MAXIMUM_CAPACITY]*best_land_number)
        maximum_grains = np.random.permutation(flatten_wolrd).reshape(self.WORLD_SIZE_X, self.WORLD_SIZE_Y)
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
        ids = np.arange(self.NUM_PEOPLE)
        ages = np.zeros(self.NUM_PEOPLE, dtype=int)
        metabolism = np.random.randint(1, self.METABOLISM_MAX, size=self.NUM_PEOPLE)
        life_expectancy = np.random.randint(self.LIFE_EXPECTANCY_MIN, self.LIFE_EXPECTANCY_MAX+1, size=self.NUM_PEOPLE)
        vision = np.random.randint(1, self.MAX_VISION+1, size=self.NUM_PEOPLE) 
        wealth = metabolism + np.random.randint(0, 50, size=self.NUM_PEOPLE)
        axis_x = np.random.randint(0, self.WORLD_SIZE_X, size=self.NUM_PEOPLE)
        axis_y = np.random.randint(0, self.WORLD_SIZE_Y, size=self.NUM_PEOPLE)
        matrix = np.array((ids, wealth, ages, metabolism, life_expectancy, vision, axis_x, axis_y))
        return matrix.T 

    def __update_lorenz_and_gini(self):
        # sort wealth
        sorted_wealth = sorted(self.peoples.items(), key= lambda x:x[1].wealth)
        total_wealth = 0
        for id in range(self.NUM_PEOPLE):
            total_wealth += self.peoples[id].wealth

        wealth_sum_so_far = 0
        gini_index_reserve = 0
        lorenz_points = []
        for i, people in enumerate(sorted_wealth):
            wealth_sum_so_far += people[1].wealth
            lorenz_points.append((wealth_sum_so_far/total_wealth)*100)
            gini_index_reserve += (i+1)/self.NUM_PEOPLE - wealth_sum_so_far/total_wealth

        # gini_index = gini_index_reserve/(gini_index_reserve + np.sum(lorenz_points))
        gini_index = (gini_index_reserve / self.NUM_PEOPLE) / 0.5
        return lorenz_points, gini_index

    def __grain_grow(self):
        if self.clock % self.GRAIN_GROWTH_INTERVAL == 0:
            self.grains_distribution += self.NUM_GRAIN_GROWN
            self.grains_distribution = np.minimum(self.grains_distribution, self.maximum_grains)

    '''
        Set the class of people
        if a people has less than a third the wealth of the richest people, group it the poor. 
        If between one and two thirds, group it the middle.  
        If over two thirds, group it the rich.
    '''
    def __group_people(self, max_wealth):
        r, m, p = 0, 0, 0
        for people in self.peoples.values():
            if people.wealth <= max_wealth / 3.0:
                p += 1
            elif people.wealth <= max_wealth * 2.0 / 3.0:
                m += 1
            else:
                r += 1
        return r, m, p

    def step(self):
        location_index = {}
        max_wealth = 0
        for people in self.peoples.values():
            people.turn_towards_grain()
            location_index[(people.axis_x, people.axis_y)] = location_index.get((people.axis_x, people.axis_y), 0) + 1
            
        for people in self.peoples.values():
            people.wealth += self.grains_distribution[
                people.axis_x, people.axis_y] / location_index[(people.axis_x, people.axis_y)
                ]
            people.move_eat_age_die()
            max_wealth = max(people.wealth, max_wealth)

        self.__grain_grow()
        return self.__group_people(max_wealth)
        
    def simulate(self):
        print('Start Simulation')
        lorenz_results = {}
        gini_results = []
        rich, middle, poor= [], [], []
        while self.clock <= self.MAXIMUM_CLOCK:
            r, m, p = self.step()
            rich.append(r)
            middle.append(m)
            poor.append(p)
            # records lorenz & gini index
            lorenz_points, gini_index = self.__update_lorenz_and_gini()
            lorenz_results[self.clock] = lorenz_points
            gini_results.append(gini_index)

            # records num of each group
            # r, m, p = self.__group_people()
            self.clock += 1
        print('Simulation Finished')
        return lorenz_results, gini_results, rich, middle, poor

