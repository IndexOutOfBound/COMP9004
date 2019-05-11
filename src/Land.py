class Land(object):
    def __init__(self, capacity):
        '''
        @param
            - capacity: The maximum amount of grain this land can hold.
        '''
        self.capacity = capacity
        self.current_grain = 0      # The current amount of grain this land hold