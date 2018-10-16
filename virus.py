class Virus(object):

    def __init__(self, name, mortality_rate, reproduction_rate):
        #Initalizes Virus
        self.name = name
        self.mortality_rate = mortality_rate
        self.reproduction_rate = reproduction_rate

#test
# hib = Virus("HIV", .8, .3)
#
# print((hib.mortality_rate * 100))
