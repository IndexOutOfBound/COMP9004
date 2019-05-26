import numpy as np
import threading


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
        self.__id = args[0]
        self.wealth = args[1]
        self.age = args[2]
        self.__metabolism = args[3]
        self.__life_expectancy = args[4]
        self.__vision = args[5]
        self.axis_x = args[6]
        self.axis_y = args[7]
        self.best_direction = 0

    def turn_towards_grain(self):
        # determin move direction
        best_left = np.sum(self.world.grains_distribution[max(0, self.axis_x-self.__vision):self.axis_x, self.axis_y])
        best_right = np.sum(
            self.world.grains_distribution[ self.axis_x : min(self.__vision+self.axis_x, self.world.WORLD_SIZE_X), self.axis_y]
            )
        best_up = np.sum(
            self.world.grains_distribution[ self.axis_x, min(0, self.axis_y-self.__vision) : self.axis_y] 
        )
        best_down = np.sum(
            self.world.grains_distribution[ self.axis_x, self.axis_y : min(self.world.WORLD_SIZE_Y, self.axis_y+self.__vision)]
        )
        self.best_direction = np.argmax([best_left, best_down, best_right, best_up])

    def move_eat_age_die(self):
        # move
        if self.best_direction == 0:
            self.axis_x = max(0, self.axis_x-1)
        elif self.best_direction == 1:
            self.axis_y = min(self.world.WORLD_SIZE_Y, self.axis_y+1)
        elif self.best_direction == 2:
            self.axis_x = min(self.world.WORLD_SIZE_X, self.axis_x+1)
        else:
            self.axis_y = max(0, self.axis_y-1)
        
        # eat
        self.wealth -= self.__metabolism
        self.age += 1

        if self.wealth < 0 or self.age > self.__life_expectancy:
            self.reborn()

    def reborn(self):
        self.age = 0
        self.__metabolism = self.__metabolism * self.world.GENETIC
        min_life = self.__life_expectancy * self.world.GENETIC
        self.__life_expectancy = min_life + np.random.randint(min_life, self.world.LIFE_EXPECTANCY_MAX+1)
        self.__vision = self.__vision * self.world.GENETIC
        self.wealth = self.__metabolism + self.wealth*self.world.INHERITANCE_RATE