import numpy as np
from World import World
from PeopleExtension import PeopleExtension
import time

class WorldExtension(World):
    def __init__(self, conf):
        super(WorldExtension, self).__init__(conf)
        # how much influence parents have on the next generation
        self.INHERITANCE_RATE = float(conf['INHERITANCE_RATE'])
        self.GENETIC = float(conf['GENETIC'])
        # how many clocks for summer
        self.SUMMER_INTERVAL = int(conf['SUMMER_INTERVAL'])
        # how many clocks for winter
        self.WINTER_INTERVAL = 100 - self.SUMMER_INTERVAL
        self.RECLAMATION_INTERVAL = float(conf['RECLAMATION_INTERVAL'])
        # the grown rate in different season
        self.SUMMER_GROWN_RATE = 1
        self.WINTER_GROWN_RATE = 0.6
    
    '''
        generate N people with extension model
    '''
    def _setup_people(self):
        peoples = {}
        # peoples_matrix: [[id, wealth, age, metabolism, life_expectancy, vision, axis_x, axis_y],]
        peoples_matrix = self._generate_peoples()
        for i in range(peoples_matrix.shape[0]):
            peoples[i] = PeopleExtension(self, *peoples_matrix[i])
        return peoples

    '''
        The extension model have different growth rate in different season.
    '''
    def _grain_grow(self):
        if self.clock % self.GRAIN_GROWTH_INTERVAL == 0:
            dayInYear = self.clock % (self.SUMMER_INTERVAL + self.WINTER_INTERVAL)
            if dayInYear > self.SUMMER_INTERVAL:
                grownRate = self.SUMMER_GROWN_RATE
            else:
                grownRate = self.WINTER_GROWN_RATE

            self.grains_distribution += self.NUM_GRAIN_GROWN * grownRate
            self.grains_distribution = np.minimum(self.grains_distribution, self.maximum_grains)

    '''
        The extension model will randomly swap the land's maximum capcity
    '''
    def _reclamation(self):
        self.maximum_grains = np.random.permutation(
            self.maximum_grains.flatten()
            ).reshape(self.WORLD_SIZE_X, self.WORLD_SIZE_Y)

    def simulate(self):
        lorenz_results = []
        gini_results, rich, middle, poor= [], [], [], []
        while self.clock <= self.MAXIMUM_CLOCK:
            r, m, p = self._step()
            rich.append(r)
            middle.append(m)
            poor.append(p)
            # records lorenz & gini index
            lorenz_points, gini_index = self._update_lorenz_and_gini()
            lorenz_results.append(lorenz_points)
            gini_results.append(gini_index)
            self.clock += 1
            if self.clock % self.RECLAMATION_INTERVAL == 0:
                self._reclamation()
        return lorenz_results, gini_results, rich, middle, poor


