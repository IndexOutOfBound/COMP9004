import numpy as np
from People import People


class PeopleExtension(People):
    def __init__(self, world, *args):
        super(PeopleExtension, self).__init__(world, *args)

    # The extension model will consider inheritage from last generation
    def rebirth(self):
        self.age = 0
        # The child's metabolism = Genetic% * Parent's_Metabolism + (1 - Genetic%) * Random
        self._metabolism = np.ceil(self._metabolism * self.world.GENETIC + \
            np.random.randint(1, self.world.METABOLISM_MAX) * (1 - self.world.GENETIC)
        )
        self._life_expectancy = np.random.randint(
            self.world.LIFE_EXPECTANCY_MIN, self.world.LIFE_EXPECTANCY_MAX+1
            )
        self._vision = np.random.randint(0, self.world.MAX_VISION)
        # The child's wealth = inheritance% * parent's wealth + (1-inheritance%)*random
        self.wealth = self._metabolism + self.wealth * self.world.INHERITANCE_RATE + \
            np.random.randint(0, 50) * (1 - self.world.INHERITANCE_RATE)