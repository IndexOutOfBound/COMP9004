class People(object):
    def __init__(self, age : int, wealth : int, life_expectancy : int, metabolism : int, vision : int, **kwargs):
        '''
        @param
            - age: how old a people is
            - wealth: the current amount of grain a people hase
            - life_expectancy: maximum age that a people can reach
            - metabolism: how much grain a people eats each time
            - vision: how many lands ahead a turtle can see
        '''
        self.age = age
        self.wealth = wealth
        self.life_expectancy = life_expectancy
        self.metabolism = metabolism
        self.vision = vision

    def forward(self):
        pass

