import numpy as np
import queue
from People import People
from World import World
class WorldExtension(World):
    def __init__(self, conf):
        super(WorldExtension, self).__init__(conf)
        self.INHERITANCE_RATE = conf['INHERITANCE_RATE']
        self.GENETIC = conf['GENETIC']
        # how many clocks for summer
        self.SUMMER_INTERVAL = int(conf['SUMMER_INTERVAL'])
        # how many clocks for winter
        self.WINTER_INTERVAL = 100 - self.SUMMER_INTERVAL
        self.RECLAMATION_INTERVAL = float(conf['RECLAMATION_INTERVAL'])
        # the grown rate in different season
        self.SUMMER_GROWN_RATE = 1
        self.WINTER_GROWN_RATE = 0.6

#         # set up various parts of the world
#         # generate the worlds
#         # random define each land's maximum capacity
#         self.maximum_grains = world.maximum_grains.copy()
#         # set up the initial grains distribution eaqual to maximum
#         self.grains_distribution = self.maximum_grains.copy()
#         # random ditribute people in the world
#         self.peoples = self.__setup_people()
#         # Initial lorenz and gini
#         self.lorenz_points, self.gini_index = self.__update_lorenz_and_gini()


#     '''
#         generate N people
#     '''
#     def __setup_people(self):
#         peoples = {}
#         # peoples_matrix: [[id, wealth, age, metabolism, life_expectancy, vision, axis_x, axis_y],]
#         peoples_matrix = self.__generate_peoples()
#         for i in range(peoples_matrix.shape[0]):
#             peoples[i] = People(self, *peoples_matrix[i])
#         return peoples

#     def __generate_peoples(self):
#         ids = np.arange(self.NUM_PEOPLE)
#         ages = np.zeros(self.NUM_PEOPLE, dtype=int)
#         metabolism = np.random.randint(1, self.METABOLISM_MAX, size=self.NUM_PEOPLE)
#         life_expectancy = np.random.randint(
#             self.LIFE_EXPECTANCY_MIN, self.LIFE_EXPECTANCY_MAX + 1, size=self.NUM_PEOPLE
#         )
#         for i in ids:
#             ages[i] += np.random.randint(life_expectancy[i])
#         vision = np.random.randint(1, self.MAX_VISION+1, size=self.NUM_PEOPLE)
#         wealth = metabolism + np.random.randint(0, 50, size=self.NUM_PEOPLE)
#         axis_x = np.random.randint(0, self.WORLD_SIZE_X, size=self.NUM_PEOPLE)
#         axis_y = np.random.randint(0, self.WORLD_SIZE_Y, size=self.NUM_PEOPLE)
#         matrix = np.array((ids, wealth, ages, metabolism, life_expectancy, vision, axis_x, axis_y))
#         return matrix.T 


    def _grain_grow(self):
        if self.clock % self.GRAIN_GROWTH_INTERVAL == 0:
            dayInYear = self.clock % (self.SUMMER_INTERVAL + self.WINTER_INTERVAL)
            if dayInYear > self.SUMMER_INTERVAL:
                grownRate = self.SUMMER_GROWN_RATE
            else:
                grownRate = self.WINTER_GROWN_RATE

            self.grains_distribution += self.NUM_GRAIN_GROWN * grownRate
            self.grains_distribution = np.minimum(self.grains_distribution, self.maximum_grains)

        
    def simulate(self):
        print('Start Simulation')
        lorenz_results = {}
        gini_results, rich, middle, poor= [], [], [], []
        while self.clock <= self.MAXIMUM_CLOCK:
            r, m, p = self._step()
            rich.append(r)
            middle.append(m)
            poor.append(p)
            # records lorenz & gini index
            lorenz_points, gini_index = self._update_lorenz_and_gini()
            lorenz_results[self.clock] = lorenz_points
            gini_results.append(gini_index)
            self.clock += 1
            if self.clock > 0 and \
                    self.clock % self.RECLAMATION_INTERVAL == 0:
                self.Reclamation()

        print('Simulation Finished')
        return lorenz_results, gini_results, rich, middle, poor

#     '''
#             this procedure recomputes the value of gini-index-reserve
#             and the points in lorenz-points for the Lorenz and Gini-Index plots
#         '''



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