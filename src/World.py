import numpy as np
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
        self.PERSENT_BEST_LAND = float(conf['PERSENT_BEST_LAND']) / 100.0
        self.GRAIN_GROWTH_INTERVAL = int(conf['GRAIN_GROWTH_INTERVAL'])
        self.NUM_GRAIN_GROWN = int(conf['NUM_GRAIN_GROWN'])

        # initial clock
        self.clock = 0

        # generate the world
        self.maximum_grains = self._setup_lands__capacity()
        # set up the initial grains distribution eaqual to maximum
        self.grains_distribution = self.maximum_grains.copy()
        # random ditribute people in the world
        self.peoples = self._setup_people()
        # Initial lorenz and gini
        self.lorenz_points, self.gini_index = self._update_lorenz_and_gini()
        
    '''
        This method will generate a matrix. each value will be the related land's capacity.
    '''
    def _setup_lands__capacity(self):
        # generate best land
        best_land_number =  int(self.WORLD_SIZE * self.PERSENT_BEST_LAND)
        land_value_range = np.zeros(self.WORLD_SIZE-best_land_number)
        flatten_wolrd = np.append(land_value_range, [self.LAND_MAXIMUM_CAPACITY]*best_land_number)
        maximum_grains = np.random.permutation(
            flatten_wolrd).reshape(self.WORLD_SIZE_X, self.WORLD_SIZE_Y
            )
        tmp = maximum_grains.copy()
        # spread that grain around the window a little and put a little back
        # into the patches that are the "best land" found above
        for _ in range(5):
            tmp = np.maximum(tmp, maximum_grains)
            tmp = self._diffuse(tmp, 0.25)
        
        for _ in range(10):
            tmp = self._diffuse(tmp, 0.25)

        return np.floor(tmp)

    '''
        Execute Diffusing process.
        Move the world matrix to each direction once,
        and added with the oringinal world matrix
    '''
    def _diffuse(self, matrix, index):
        matrix_1, matrix_2 = np.zeros(matrix.shape),np.zeros(matrix.shape)
        matrix_3, matrix_4 = np.zeros(matrix.shape),np.zeros(matrix.shape)
        matrix_5, matrix_6 = np.zeros(matrix.shape),np.zeros(matrix.shape)
        matrix_7, matrix_8 = np.zeros(matrix.shape),np.zeros(matrix.shape)

        # matrix move up: the first row move to the last row
        matrix_1[:-1] = matrix[1:]
        matrix_1[-1] = matrix[0]

        # matrix move down: the last row move to the first row
        matrix_2[0] = matrix[-1]
        matrix_2[1:] = matrix[:-1]

        # matrix move left: the first column move to the last col
        matrix_3[:, :-1] = matrix[:, 1:]
        matrix_3[:, -1] = matrix[:, 0]

        # matrix move right : the last col move to the first col
        matrix_4[:, 0] = matrix[:, -1]
        matrix_4[:, 1:] = matrix[:, :-1]

        # matrix move right and down
        matrix_5[0] = matrix_4[-1]
        matrix_5[1:] = matrix_4[:-1]

        # matrix move right and up
        matrix_6[-1] = matrix_4[0]
        matrix_6[:-1] = matrix_4[1:]

        # matrix move left and down
        matrix_7[0] = matrix_3[-1]
        matrix_7[1:] = matrix_3[:-1]

        # matrix move left and up
        matrix_8[-1] = matrix_3[0]
        matrix_8[:-1] = matrix_3[1:] 

        return matrix * (1-index) + (matrix_1 + matrix_2 + matrix_3 + matrix_4 + matrix_5 \
            + matrix_6 + matrix_7 + matrix_8)*index/8.0

    '''
        generate N people
    '''
    def _setup_people(self):
        peoples = {}
        # peoples_matrix: [[id, wealth, age, metabolism, life_expectancy, vision, axis_x, axis_y],]
        peoples_matrix = self._generate_peoples()
        for i in range(peoples_matrix.shape[0]):
            peoples[i] = People(self, *peoples_matrix[i])
        return peoples

    '''
        set up initial values for the people variables 
    '''
    def _generate_peoples(self):
        ids = np.arange(self.NUM_PEOPLE)
        ages = np.zeros(self.NUM_PEOPLE, dtype=int)
        metabolism = np.random.randint(1, self.METABOLISM_MAX+1, size=self.NUM_PEOPLE)
        life_expectancy = np.random.randint(
            self.LIFE_EXPECTANCY_MIN, self.LIFE_EXPECTANCY_MAX+1, size=self.NUM_PEOPLE
            )
        for i in ids:
            ages[i] += np.random.randint(life_expectancy[i])
        vision = np.random.randint(1, self.MAX_VISION+1, size=self.NUM_PEOPLE) 
        wealth = metabolism + np.random.randint(0, 50, size=self.NUM_PEOPLE)
        axis_x = np.random.randint(0, self.WORLD_SIZE_X, size=self.NUM_PEOPLE)
        axis_y = np.random.randint(0, self.WORLD_SIZE_Y, size=self.NUM_PEOPLE)
        matrix = np.array((ids, wealth, ages, metabolism, life_expectancy, vision, axis_x, axis_y))
        return matrix.T 

    '''
        this procedure recomputes the value of gini-index-reserve
        and the points in lorenz-points for the Lorenz and Gini-Index plots
    '''
    def _update_lorenz_and_gini(self):
        # sort wealth
        sorted_wealth = sorted(self.peoples.items(), key= lambda x:x[1].wealth)
        total_wealth = 0.0
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
    
    '''
        patch procedure, if a patch does not have it's maximum amount of grain, add
        Num-grain-grown to its grain amount
    '''
    def _grain_grow(self):
        if self.clock % self.GRAIN_GROWTH_INTERVAL == 0:
            self.grains_distribution += self.NUM_GRAIN_GROWN
            self.grains_distribution = np.minimum(self.grains_distribution, self.maximum_grains)

    '''
        Set the class of people
        if a people has less than a third the wealth of the richest people, group it the poor. 
        If between one and two thirds, group it the middle.  
        If over two thirds, group it the rich.
    '''
    def _group_people(self, max_wealth):
        r, m, p = 0, 0, 0
        for people in self.peoples.values():
            if people.wealth <= max_wealth / 3.0:
                p += 1
            elif people.wealth <= max_wealth * 2.0 / 3.0:
                m += 1
            else:
                r += 1
        return r, m, p

    '''
        The procedure will happen in one clock
    '''
    def _step(self):
        people_here = {}
        max_wealth = 0
        # each people decide direction
        for people in self.peoples.values():
            people.turn_towards_grain()
            people_here[(people.axis_x, people.axis_y)] = \
                people_here.get((people.axis_x, people.axis_y), 0) + 1

        # each people step
        for people in self.peoples.values():
            # harvest
            harvest = float(self.grains_distribution[people.axis_x, people.axis_y])\
                / people_here[(people.axis_x, people.axis_y)] 
            people.wealth += harvest

            # now that the grain has been harvested, have the turtles make the
            # patches which they are on have no grain
            self.grains_distribution[people.axis_x, people.axis_y] -= harvest
            people.move_eat_age_die()
            max_wealth = max(people.wealth, max_wealth)

        self._grain_grow()
        return self._group_people(max_wealth)
        
    def simulate(self):
        lorenz_results = []
        gini_results, rich, middle, poor= [], [], [], []

        while self.clock <= self.MAXIMUM_CLOCK:
            # exectue one step, record the num of rich, middle and poor
            r, m, p = self._step()
            rich.append(r)
            middle.append(m)
            poor.append(p)
            # records lorenz & gini index
            lorenz_points, gini_index = self._update_lorenz_and_gini()
            lorenz_results.append(lorenz_points)
            gini_results.append(gini_index)

            self.clock += 1
        return lorenz_results, gini_results, rich, middle, poor

