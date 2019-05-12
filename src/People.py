import numpy as np
class People(object):
    def __init__(self, id, **kwargs):
        '''
        @param
            - age: how old a people is
            - wealth: the current amount of grain a people hase
            - life_expectancy: maximum age that a people can reach
            - metabolism: how much grain a people eats each time
            - vision: how many lands ahead a turtle can see
        '''
        self.__id = id
        self.__wealth = self.__init_wealth()
        self.__metabolism = self.__init_metabolism(kwargs['maximum_metabolism'])
        self.__age = 0
        self.__life_expectancy = self.__init_life_expectancy(kwargs['maximum_life_expectancy'])
        self.__vision = self.__init_vision(kwargs['maximum_vision'])

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

    def forward(self):
        pass

    def data_dict(self):
        return {
            'id': self.__id,
            'age': self.__age,
            'wealth': self.__wealth,
            'vision': self.__vision,
        }

    @staticmethod
    def generate_peoples(num, **kwargs):
        ids = np.arange(num)
        ages = np.zeros(num, dtype=int)
        metabolism = np.random.randint(1, kwargs['maximum_metabolism'], size=num)
        life_expectancy = np.random.randint(1, kwargs['maximum_life_expectancy']+1, size=num)
        vision = np.random.randint(1, kwargs['maximum_vision']+1, size=num) 
        wealth = metabolism + np.random.randint(0, 50, size=num)
        matrix = np.array((ids, wealth, ages, metabolism, life_expectancy, vision))
        return matrix.T
       