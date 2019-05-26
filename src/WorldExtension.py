import numpy as np
import threading
import queue
from People import People

class WorldExtension(object):


    def __init__(self, world, conf):
        # load global parmeters
        self.MAXIMUM_CLOCK = world.MAXIMUM_CLOCK
        self.WORLD_SIZE_X = world.WORLD_SIZE_X
        self.WORLD_SIZE_Y = world.WORLD_SIZE_Y
        self.WORLD_SIZE = world.WORLD_SIZE
        self.LAND_MAXIMUM_CAPACITY = world.LAND_MAXIMUM_CAPACITY
        self.NUM_PEOPLE = world.NUM_PEOPLE
        self.MAX_VISION = world.MAX_VISION
        self.METABOLISM_MAX = world.METABOLISM_MAX
        self.LIFE_EXPECTANCY_MIN = world.LIFE_EXPECTANCY_MIN
        self.LIFE_EXPECTANCY_MAX = world.LIFE_EXPECTANCY_MAX
        self.PERSENT_BEST_LAND = world.PERSENT_BEST_LAND
        self.GRAIN_GROWTH_INTERVAL = world.GRAIN_GROWTH_INTERVAL
        self.NUM_GRAIN_GROWN = world.NUM_GRAIN_GROWN
        self.INHERITANCE_RATE = conf['INHERITANCE_RATE']
        self.GENETIC = conf['GENETIC']
        # how many clocks for summer
        self.SUMMER_INTERVAL = conf['SUMMER_INTERVAL']
        # how many clocks for winter
        self.WINTER_INTERVAL = 100 - self.SUMMER_INTERVAL
        self.RECLAMATION_INTERVAL = conf['RECLAMATION_INTERVAL']
        # the grown rate in different season
        self.SUMMER_GROWN_RATE = 1
        self.WINTER_GROWN_RATE = 0.6
        self.clock = 0

        # set up various parts of the world
        # generate the worlds
        # random define each land's maximum capacity
        self.maximum_grains = world.maximum_grains
        # set up the initial grains distribution eaqual to maximum
        self.grains_distribution = world.grains_distribution
        # random ditribute people in the world
        self.peoples = world.peoples
        # Initial lorenz and gini
        self.lorenz_points = world.lorenz_points
        self.gini_index = world.gini_index

        
    '''
        This method will generate a matrix. each value will be the related land's capacity.
    '''





    def __setup_lands__capacity(self):
        # generate best land
        best_land_number = int(self.WORLD_SIZE * self.PERSENT_BEST_LAND)
        land_value_range = np.zeros(self.WORLD_SIZE - best_land_number)
        flatten_wolrd = np.append(land_value_range, [self.LAND_MAXIMUM_CAPACITY] * best_land_number)
        maximum_grains = np.random.permutation(flatten_wolrd).reshape(self.WORLD_SIZE_X, self.WORLD_SIZE_Y)
        tmp = maximum_grains.copy()

        # spread that grain around the window a little and put a little back
        # into the patches that are the "best land" found above
        for _ in range(5):
            for i in range(self.WORLD_SIZE_X):
                for j in range(self.WORLD_SIZE_Y):
                    if maximum_grains[i, j] != 0:
                        tmp[i, j] = maximum_grains[i, j]
                    keep_share = tmp[i, j] * 0.75
                    tmp[i - 1:i + 2, j - 1:j + 2] += tmp[i, j] / 32.0
                    tmp[i, j] = keep_share

        for _ in range(10):
            for i in range(self.WORLD_SIZE_X):
                for j in range(self.WORLD_SIZE_Y):
                    keep_share = tmp[i, j] * 0.75
                    tmp[i - 1:i + 2, j - 1:j + 2] += tmp[i, j] / 32.0
                    tmp[i, j] = keep_share

        return np.floor(tmp)

    '''
        generate N people
    '''
    def __setup_people(self):
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

    def update_lorenz_and_gini(self):
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
            dayInYear = self.clock % (self.SUMMER_INTERVAL + self.WINTER_INTERVAL)
            if dayInYear > self.SUMMER_INTERVAL:
                grownRate = self.SUMMER_GROWN_RATE
            else:
                grownRate = self.WINTER_GROWN_RATE

            self.grains_distribution += self.NUM_GRAIN_GROWN * grownRate
            self.grains_distribution = np.minimum(self.grains_distribution, self.maximum_grains)

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
            people.wealth += self.grains_distribution[people.axis_x, people.axis_y] / location_index[(people.axis_x, people.axis_y)]
            people.move_eat_age_die()
            max_wealth = max(people.wealth, max_wealth)

        self.__grain_grow()
        return self.__group_people(max_wealth)
        
    def simulate(self):
        print('Start Simulation')
        lorenz_results = {}
        gini_results, rich, middle, poor= [], [], [], []
        while self.clock <= self.MAXIMUM_CLOCK:
            r, m, p = self.step()
            rich.append(r)
            middle.append(m)
            poor.append(p)
            # records lorenz & gini index
            lorenz_points, gini_index = self.__update_lorenz_and_gini()
            lorenz_results[self.clock] = lorenz_points
            gini_results.append(gini_index)
            self.clock += 1
            if self.clock > 0 and \
                    self.clock % self.RECLAMATION_INTERVAL == 0:
                self.Reclamation()

        print('Simulation Finished')
        return lorenz_results, gini_results, rich, middle, poor

    '''
            this procedure recomputes the value of gini-index-reserve
            and the points in lorenz-points for the Lorenz and Gini-Index plots
        '''

    def __update_lorenz_and_gini(self):
        # sort wealth
        sorted_wealth = sorted(self.peoples.items(), key=lambda x: x[1].wealth)
        total_wealth = 0
        for id in range(self.NUM_PEOPLE):
            total_wealth += self.peoples[id].wealth

        wealth_sum_so_far = 0
        gini_index_reserve = 0
        lorenz_points = []
        for i, people in enumerate(sorted_wealth):
            wealth_sum_so_far += people[1].wealth
            lorenz_points.append((wealth_sum_so_far / total_wealth) * 100)
            gini_index_reserve += (i + 1) / self.NUM_PEOPLE - wealth_sum_so_far / total_wealth

        # gini_index = gini_index_reserve/(gini_index_reserve + np.sum(lorenz_points))
        gini_index = (gini_index_reserve / self.NUM_PEOPLE) / 0.5
        return lorenz_points, gini_index


    def Reclamation(self):
        indexes = list(np.zeros(len(self.maximum_grains)))
        newMaximum = self.maximum_grains.copy()
        for i in range(0, len(indexes)):
            indexes[i] = i

        while(len(indexes) >= 2):
            #random choice two locations
            index = np.random.randint(0, len(indexes))
            i = indexes[index]
            indexes.remove(i)

            index = np.random.randint(0, len(indexes))
            j = indexes[index]
            indexes.remove(j)

            #swap the maximum number of grains it could grow

            newMaximum[i] = self.maximum_grains[j]
            newMaximum[j] = self.maximum_grains[i]

        self.maximum_grains = newMaximum