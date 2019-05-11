import Land
import numpy as np

class World(object):
    def __init__(self, **kwargs):
        # TODO: set up a config file or input via command
        # Set up global parmeters
        self.land_maximum_capacity = kwargs['land_maximum_capacity']    
        self.world_size = kwargs['world_size']      
        self.population = kwargs['population']  
        self.percent_best_land = kwargs['percent_best_land']   
        self.GINI_Index = 0
        self.Lorenz_points = 0

         # set up various parts of the world
        self.maximum_matrix = self.__setup_lands__capacity()
        self.world = self.maximum_matrix.copy()
   

    '''
        This method will generate a matrix. each value will be the related land's capacity.
    '''
    def __setup_lands__capacity(self):
        # Using The following method, the best land percent may be around the setting number
        # distribution = [self.percent_best_land]
        # distribution.extend([(1-self.percent_best_land)/self.land_maximum_capacity] * self.land_maximum_capacity)
        # matrix = np.random.choice(self.land_maximum_capacity+1, size=self.world_size, p=distribution)
        world_capacity = self.world_size[0] * self.world_size[1]
        best_land_number =  int(world_capacity * self.percent_best_land)
        land_value_range = np.random.randint(0, self.land_maximum_capacity, size=world_capacity-best_land_number)
        flatten_wolrd = np.append(land_value_range, [self.land_maximum_capacity]*best_land_number)
        maximum_matrix = np.random.permutation(flatten_wolrd).reshape(self.world_size)
        return maximum_matrix
        
       



        

    