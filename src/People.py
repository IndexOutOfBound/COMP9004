import numpy as np
import threading
class People(threading.Thread):
    def __init__(self, *args):
        '''
        @param
            - age: how old a people is
            - wealth: the current amount of grain a people hase
            - life_expectancy: maximum age that a people can reach
            - metabolism: how much grain a people eats each time
            - vision: how many lands ahead a turtle can see
        '''
        threading.Thread.__init__(self)
        self.__id = args[0]
        self.wealth = args[1]
        self.age = args[2]
        self.__metabolism = args[3]
        self.__life_expectancy = args[4]
        self.__vision = args[5]

    def __str__(self):
        return f"People[{self.__id}]--age:{self.__age}, wealth:{self.__wealth}, \
                    metabolism:{self.__metabolism}, vision:{self.__vision}"

    def __init_metabolism(self, maximum_metabolism):
        return np.random.randint(1, maximum_metabolism+1)

    def __init_wealth(self):
        return np.random.randint(self.__metabolism, self.__metabolism + 50)

    def __init_life_expectancy(self, maximum_life_expectancy):
        return np.random.randint(1, maximum_life_expectancy+1)

    def __init_vision(self, maximum_vision):
        return np.random.randint(1, maximum_vision+1)

    def data_dict(self):
        return {
            'id': self.__id,
            'age': self.__age,
            'wealth': self.__wealth,
            'vision': self.__vision,
        }

    def run(self):
        print('people run')

    @staticmethod
    def generate_peoples(num, world_size, **kwargs):
        ids = np.arange(num)
        ages = np.zeros(num, dtype=int)
        metabolism = np.random.randint(1, kwargs['maximum_metabolism'], size=num)
        life_expectancy = np.random.randint(1, kwargs['maximum_life_expectancy']+1, size=num)
        vision = np.random.randint(1, kwargs['maximum_vision']+1, size=num) 
        wealth = metabolism + np.random.randint(0, 50, size=num)
        axis_x = np.random.randint(0, world_size[0], size=num)
        axis_y = np.random.randint(0, world_size[1], size=num)
        matrix = np.array((ids, wealth, ages, metabolism, life_expectancy, vision, axis_x, axis_y))
        return matrix.T
       