from People import People
import numpy as np

class World(object):
    def __init__(self, **kwargs):
        # TODO: set up a config file or input via command
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
        self.people_distribution, self.peoples_matrix = self.__setup_people(**kwargs['people_configuration'])
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

    def __setup_people(self, **kwargs):
        # generate N people
        # peoples = np.zeros((self.population, 4))
        # for id in range(self.population):
        #     new_people = People(id, **kwargs)
        #     data = new_people.data_dict()
        #     peoples[id,:] = [data['id'], data['wealth'], data['age'], data['vision']]

        peoples_matrix = People.generate_peoples(self.population, **kwargs)
        # random locate people in the world
        location_matrix = np.arange(self.population)
        location_matrix = np.pad(
            location_matrix, 
            (self.world_size[0] * self.world_size[1] - self.population,0), 
            mode='constant', constant_values=(-1,-1))
        location_matrix = np.random.permutation(location_matrix).reshape(self.world_size)
        return location_matrix, peoples_matrix

    def update_lorenz_and_gini(self):
        # sort wealth
        # sorted_wealth = sorted(self.peoples_matrix, key=lambda x : x[:,1], reverse=True)
        sorted_wealth = self.peoples_matrix[np.argsort(self.peoples_matrix[:,1])]
        total_wealth = np.sum(self.peoples_matrix[:, 1])
        
        wealth_sum_so_far = 0
        gini_index_reserve = 0
        lorenz_points = []
        for i in range(sorted_wealth.shape[0]):
            wealth_sum_so_far += sorted_wealth[i, 1]
            lorenz_points.append((wealth_sum_so_far/total_wealth)*100)
            gini_index_reserve += (i+1)/self.population - wealth_sum_so_far/total_wealth

        gini_index = gini_index_reserve/(gini_index_reserve + np.sum(lorenz_points))
        print(gini_index)
        return lorenz_points, gini_index_reserve

    def start_simulation(self):
        pass