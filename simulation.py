# This project was a colaboration between Marianna Campbell and Eric Botcher
# All final push code has been shared.

import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    def __init__(self, population_size, vacc_percentage, virus_name, mortality_rate, death_counter,basic_repro_num, initial_infected=1):
        self.population_size = population_size
        self.population = []
        self.total_infected = 0
        self.current_infected = 0
        self.next_person_id = 1
        self.virus_name = virus_name
        self.mortality_rate = mortality_rate
        self.basic_repro_num = basic_repro_num
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            virus_name, population_size, vacc_percentage, initial_infected)
        self.vacc_percentage = vacc_percentage
        self.logger = Logger(self.file_name)
        self.newly_infected = []
        self.population = self._create_population(initial_infected)
        self.death_counter = 0


    def _create_population(self, initial_infected,):
        # Total_infected = initial_infected*self.population_size
        print(f"The initial_infected value is: {initial_infected}")
        self.population = []
        infected_count = 0
        vax_count = 0
        while len(self.population) != self.population_size:
            #Create infected population
            if infected_count !=  initial_infected:
                self.population.append(Person(self.next_person_id,False, self.virus_name))
                print("We created infected people.")
                infected_count += 1
                self.next_person_id += 1
            #Create vax population
            elif vax_count != (self.population_size * self.vacc_percentage):
                self.population.append(Person(self.next_person_id,True, None))
                print("We created vaccinated people.")
                vax_count += 1
                self.next_person_id += 1
            else:
                #Create non-vax non-infected population
                self.population.append(Person(self.next_person_id,False, None))
                print("We created people that are alive.")
                self.next_person_id += 1
            # print(f"Number of people {len(self.population)}")
        return self.population


    def _simulation_should_continue(self):
        # EVERYBODY dead
        for person in self.population:
            # if not alive
            if person.is_alive == False:
                self.death_counter += 1
        if len(self.population) == self.death_counter:
            print("Everyone is dead!")
            return False
        # EVERYBODY vaccinated
        not_infected_counter = 0
        for person in self.population:
            # if person does not have a virus and person is alive
            if person.infection == None:  # and person.is_alive == True: <- you filter out people that are dead
                not_infected_counter += 1
        if len(self.population) ==  not_infected_counter:
            print("No one in the population has the virus!!")
            return False
        # SIMULATION should stop
        print("Simulation will continue to run!!")
        print(f" TOTAL DEATHS: {self.death_counter}")
        # return death_counter
        return True

    def run(self):
        self.logger.write_metadata(self.population_size, self.vacc_percentage, self.virus_name, self.mortality_rate, self.basic_repro_num)
        time_step_counter = 0
        should_continue = self._simulation_should_continue()
        while should_continue:
            self.time_step()          # Increment the counter by 1 each time
            time_step_counter += 1
            # update the logger's log_time_step method by passing in the
            self.logger.log_time_step(time_step_counter)
            # rebind should_continue to another call of self._simulation_should_continue()
            should_continue = self._simulation_should_continue()
        print('The simulation has ended after {} turns.'.format(time_step_counter))
        print(f" A total of {self.death_counter} people died from infection.")
        with open(self.file_name, "a") as file:
            file.write(f" A total of {self.death_counter} died from infection.")
            file.close()

    def time_step(self):
            infected_people = []
            interaction_counter = 0
            # Get infect people from out of the population
            for person in self.population:
                # if person is alive and person has virus
                if person.is_alive == True and person.infection != None:
                    infected_people.append(person)
            # For each infecte person in the population
            for infected_person in infected_people:
                # Repeat for 100 total interactions:
                for _ in range(0, 100):
                    # Grab a random person from the population
                    random_index = random.randint(0, len(self.population)- 1)
                    print("An infected person's random index: {}".format(random_index))
                    random_person = self.population[random_index]
                    print("The random person: {} ".format(random_person))
                    # If the person is dead, continue and grab another new
                    # person from the population.
                    if random_person.is_alive == False:
                        continue
                    else:
                        # Call simulation.interaction(person, random_person)
                        self.interaction(infected_person, random_person)
                        # interaction_counter += 1
                        interaction_counter += 1
            for person in self.population:
                if person.is_alive == True and person.infection != None:
                    # for logger function what this function returns
                    person.did_survive_infection(self.mortality_rate)
                    self.logger.log_infection_survival(person, self.population)
            self._infect_newly_infected()


    def interaction(self, person, random_person):
        assert person.is_alive == True
        assert random_person.is_alive == True
        if random_person.infection == None and random_person.is_vaccinated == False:
            random_num = float(random.randint(0, 100)/100)
            if random_num <= self.basic_repro_num:
                self.newly_infected.append(random_person._id)
        # Comment in when you have coded the logger
        self.logger.log_interaction(person, random_person)
    def _infect_newly_infected(self):
        for newly_infected_person_id in self.newly_infected:
            for person in self.population:
                if person._id == newly_infected_person_id:
                    person.infection = True
        self.newly_infected = []


params = sys.argv[1:]
pop_size = int(params[0])
vacc_percentage = float(params[1])
virus_name = str(params[2])
mortality_rate = float(params[3])
basic_repro_num = float(params[4])
if len(params) == 6:
    initial_infected = int(params[5])
else:
    initial_infected = 1
simulation = Simulation(pop_size, vacc_percentage, virus_name, mortality_rate,
                        basic_repro_num, initial_infected)
simulation.run()
