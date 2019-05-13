from People import People
import numpy as np
import threading

class World(threading.Thread):
    def __init__(self, thread_id, **kwargs):
        # TODO: set up a config file or input via command
        threading.Thread.__init__(self)
        # Set up global parmeters
        self.land_maximum_capacity = kwargs['land_maximum_capacity']    
        self.world_size = kwargs['world_size']      
        self.population = kwargs['population']  
        self.percent_best_land = kwargs['percent_best_land']   

        # set up various parts of the world
        # generate the worlds
        # random define each land's maximum capacity
        self.maximum_grains = self.__setup_lands__capacity()
        # set up the initial grains distribution eaqual to maximum
        self.grains_distribution = self.maximum_grains.copy()
        # random ditribute people in the world
        # self.peoples_matrix = self.__setup_people(**kwargs['people_configuration'])
        self.peoples = self.__setup_people(**kwargs['people_configuration'])

        # Initial lorenz and gini
        self.lorenz_points, self.gini_index_reserve = self.update_lorenz_and_gini()
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
    def __setup_people(self, **kwargs):
        peoples = {}
        # peoples_matrix: [[id, wealth, age, metabolism, life_expectancy, vision, axis_x, axis_y],]
        peoples_matrix = People.generate_peoples(self.population, self.world_size, **kwargs)
        for i in range(peoples_matrix.shape[0]):
            peoples[i] = People(*peoples_matrix[i])
        return peoples

    def update_lorenz_and_gini(self):
        # sort wealth
        # sorted_wealth = self.peoples_matrix[np.argsort(self.peoples_matrix[:,1])]
        # total_wealth = np.sum(self.peoples_matrix[:, 1])
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

        gini_index = gini_index_reserve/(gini_index_reserve + np.sum(lorenz_points))
        print(gini_index)
        return lorenz_points, gini_index_reserve

    def run(self):
        print('Start Simulation')
