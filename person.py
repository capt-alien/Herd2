import random
# TODO: Import the virus clase

class Person(object):
    def __init__(self, _id, is_vaccinated, infection):
        self._id = _id
        self.is_vaccinated = is_vaccinated
        self.is_alive = True
        self.infection = infection


    def did_survive_infection(self, mortality_rate):
        random_num = random.randint(0, 1)
        if random_num > mortality_rate:
            self.is_vaccinated = True
            self.infection = None
            return True
        else:
            self.is_alive = False
            self.infection = None
            return False
