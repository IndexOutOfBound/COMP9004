import numpy as np

class People(object):
    def __init__(self, world, *args):
        '''
        @param
            - age: how old a people is
            - wealth: the current amount of grain a people hase
            - life_expectancy: maximum age that a people can reach
            - metabolism: how much grain a people eats each time
            - vision: how many lands ahead a turtle can see
        '''
        self.world = world
        self._id = args[0]
        self.wealth = args[1]
        self.age = args[2]
        self._metabolism = args[3]
        self._life_expectancy = args[4]
        self._vision = args[5]
        self.axis_x = args[6]
        self.axis_y = args[7]
        self.best_direction = np.random.randint(0, 4)

    '''
        determin move direction
    '''
    def turn_towards_grain(self):
        # if the vision range which out of the bound will be complete with the opposite edge
        best_left = np.sum(
            self.world.grains_distribution[
                max(0, self.axis_x-self._vision) : self.axis_x, self.axis_y
                ]
        ) + np.sum(
            self.world.grains_distribution[
                min(self.world.WORLD_SIZE_X+self.axis_x-self._vision, self.world.WORLD_SIZE_X):,
                self.axis_y
                ]
        )

        best_right = np.sum(
            self.world.grains_distribution[
                self.axis_x : min(self._vision+self.axis_x, self.world.WORLD_SIZE_X), self.axis_y
                ]
        ) + np.sum(
            self.world.grains_distribution[
                : max(0, self.axis_x + self._vision - self.world.WORLD_SIZE_X), self.axis_y
                ]
        )

        best_up = np.sum(
            self.world.grains_distribution[
                self.axis_x, min(0, self.axis_y-self._vision) : self.axis_y] 
        ) + np.sum(
            self.world.grains_distribution[
                self.axis_x, 
                min(self.world.WORLD_SIZE_Y, self.axis_y-self._vision+self.world.WORLD_SIZE_Y) :
                ]
        )

        best_down = np.sum(
            self.world.grains_distribution[
                self.axis_x, self.axis_y : min(self.world.WORLD_SIZE_Y, self.axis_y+self._vision)
                ]
        ) + np.sum(
            self.world.grains_distribution[
                self.axis_x, : max(0, self.axis_y + self._vision - self.world.WORLD_SIZE_Y)
                ]
        )

        self.best_direction = np.argmax([best_left, best_down, best_right, best_up])

    def move_eat_age_die(self):
        # move left
        if self.best_direction == 0:
            # self.axis_x = max(0,self.axis_x-1)
            self.axis_x -= 1
            if self.axis_x < 0:
                self.axis_x +=  self.world.WORLD_SIZE_X
        # move down
        elif self.best_direction == 1:
            # self.axis_y = min(self.world.WORLD_SIZE_Y, self.axis_y+1)
            self.axis_y += 1
            if self.axis_y >= self.world.WORLD_SIZE_Y:
                self.axis_y -= self.world.WORLD_SIZE_Y
        # move right
        elif self.best_direction == 2:
            # self.axis_x = min(self.world.WORLD_SIZE_X, self.axis_x+1)
            self.axis_x += 1
            if self.axis_x >= self.world.WORLD_SIZE_X:
                self.axis_x -= self.world.WORLD_SIZE_X
        # move up
        else:
            # self.axis_y = max(0, self.axis_y-1)
            self.axis_y -= 1
            if self.axis_y < 0:
                self.axis_y += self.world.WORLD_SIZE_Y
        
        # eat
        self.wealth -= self._metabolism
        # age
        self.age += 1

        if self.wealth < 0 or self.age >= self._life_expectancy:
            self.rebirth()

    '''
        When people die, they will rebirth with random variables
    '''
    def rebirth(self):
        self.age = 0
        self._metabolism = np.random.randint(1, self.world.METABOLISM_MAX+1)
        self._life_expectancy = np.random.randint(
            self.world.LIFE_EXPECTANCY_MIN, self.world.LIFE_EXPECTANCY_MAX+1
            )
        self._vision = np.random.randint(1, self.world.MAX_VISION+1) 
        self.wealth = self._metabolism + np.random.randint(0, 50)


       