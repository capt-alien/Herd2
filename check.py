##this file is for testing random things. Not needed for the final push



import random, sys
random.seed(42)
from person import Person
from logger import Logger

'''
Main class that will run the herd immunity simulation program.
Expects initialization parameters passed as command line arguments when file is run.
Simulates the spread of a virus through a given population.
The percentage of the population that are vaccinated, the size of the population, and the amount of initially infected people in a population are all variables that can be set when the program is run.
_____Attributes______
- logger: Logger object.  The helper object that will be responsible for writing all logs to the simulation.
- population_size: Int.  The size of the population for this simulation.
- population: [Person].  A list of person objects representing all people in the population.
- next_person_id: Int.  The next available id value for all created person objects. Each person should have a unique _id value.
- virus_name: String.  The name of the virus for the simulation.  This will be passed to the Virus object upon instantiation.
- mortality_rate: Float between 0 and 1.  This will be passed to the Virus object upon instantiation.
- infection_rate: Float between 0 and 1. This will be passed to the Virus object upon instantiation.
- vaccination_rate: Float between 0 and 1. Represents the total percentage of population vaccinated for the given simulation.
- currently_infected: Int.  The number of currently people in the population currently infected with the disease in the simulation.
- total_infected: Int.  The running total of people that have been infected since the simulation began, including any people currently infected.
- total_deaths: Int.  The number of people that have died as a result of the infection during this simulation.  Starts at zero.
_____Methods_____
def __init__(population_size, vaccination_rate, virus_name, mortality_rate,
 infection_rate, initial_infected=1):
	- All arguments will be passed as command-line arguments when the file is run.
	- After setting values for attributes, calls self.create_population() in order to create the population array that will be used for this simulation.
def create_population(self, initial_infected):
	- Expects initial_infected as an Int.
	- Should be called only once, at the end of the __init__ method.
	- Stores all newly created Person objects in a local variable, population.
	- Creates all infected person objects first.  Each time a new one is created, increments infected_count variable by 1.
	- Once all infected person objects are created, begins creating healthy person objects.
		- To decide if a person is vaccinated or not, generates a random number between 0 and 1.
		- If that number is smaller than self.vaccination_rate, new person object will be created with vaccinated set to True.  Otherwise, vaccinated will be set to False.
	- Once len(population) is the same as self.population_size, returns population.
'''
class Simulation(object):
	def __init__(self, population_size, vaccination_rate, virus_name, mortality_rate, infection_rate, initial_infected=1, num_interactions=100):
		# number of (living) people at the start of the simulation.
		self.population_size = population_size

		# a list of each newly infected person from this step (living and to be infected)
		self.newly_infected = []

		# an integer that counts the total number of infected persons (alive and unvaccinated).
		self.currently_infected = []

		# an integer that ensures every Person object has a unique identifier.
		self.next_person_id = 1

		# hard percentage of vaccinated persons in population.
		self.vaccination_rate = vaccination_rate

		# hard value of infected persons in population.
		self.initial_infected = initial_infected

		# hard value of interactions per person
		self.num_interactions = num_interactions

		# The Name of the Virus
		self.virus_name = virus_name

		# The Deadliness of the Virus
		self.mortality_rate = mortality_rate

		# The Contamination of the Virus
		self.infected_rate = infection_rate

		# a list of every person in the entire population (living or dead).
		self.population = self.create_population()

		# an integer that counts the total number of infected persons (alive or dead, vaccinated or unvaccinated).
		self.total_infected = self.count_deaths()

		# an integer that counts the total number of infected persons (alive or dead, vaccinated or unvaccinated).
		self.total_deaths = self.count_infections()

		# the FileName output file
		self.file_name = f"{virus_name}_simulation_pop_{population_size}_vp_{vaccination_rate}_infected_{initial_infected}.txt"

		# creates the log in the output file
		self.logger = Logger(self.file_name)
		'''
		TODO: Create a Logger object and bind it to self.logger.
		You should use this logger object to log all events of any importance during the simulation.
		Don't forget to call these logger methods in the corresponding parts of the simulation!
		This attribute will be used to keep track of all the people that catch the infection during a given time step.
		We'll store each newly infected person's .ID attribute in here.
		At the end of each time step, we'll call self.contagiousify() and then reset .newly_infected back to an empty list.
		'''


	'''
	TODO: Call self.create_population() and pass in the correct parameters.
	Store the array that this method will return in the self.population attribute.
	'''
	def create_population(self):
		'''
		TODO: Finish this method!
		This method should be called when the simulation begins, to create the population that will be used.
		This method should return an array filled with Person objects that matches the specifications of the simulation (correct number of people in the population, correct percentage of people vaccinated, correct number of initially infected people).
		'''
		self.population = []
		infected_count = 0
		while len(self.population) != self.population_size:
			if infected_count != self.initial_infected:
				'''
				TODO: Create all the infected people first, and then worry about the rest.
				Don't forget to increment infected_count every time you create a new infected person!
				'''
				sick_person = Person(self.next_person_id, False, self.virus_name)
				self.population.append(sick_person)
				self.currently_infected.append(sick_person)
				infected_count += 1
			else:
				'''
				Now create all the rest of the people.
				Every time a new person will be created, generate a random number between 0 and 1.
				If this number is smaller than vaccination_rate, this person should be created as a vaccinated person.
				If not, the person should be created as an unvaccinated person.
				'''
				vaccinated = False
				vaccination_rand = random.random()
				if vaccination_rand < self.vaccination_rate:
					vaccinated = True
				self.population.append(Person(self.next_person_id, vaccinated))
			self.next_person_id += 1
			'''
			TODO: After any Person object is created, whether sick or healthy, you will need to increment self.next_person_id by 1.
			Each Person object's ID has to be unique!
			'''
		return self.population

	'''
	TODO: Complete this method!  This method should return True if the simulation should continue, or False if it should not.
	The simulation should end under any of the following circumstances:
		- The entire population is dead. (if one alive)
		- There are no alive and infected people left in the population. (if one infected alive)
	In all other instances, the simulation should continue.
	'''
	def simulation_should_continue(self):
		print()
		print("checking if simulation should continue...")
		end_death = None # simulation ends with everyone dead
		end_alive = None # simulation ends with no alive infected

		# this for loop really is the important piece of this function.
		# it determines if the end is neigh, for better or worse.
		# if the end isn't neigh, the program will continue (return True)
		for person in self.population:
			if person.alive:
				end_death = False # person is alive (not everyone dead)
				if person.infected != None and person.vaccinated == False:
					print("person # " + str(person.identity) + " is alive")
					print("   ...and sick, and unvaccinated")
					end_alive = False # person is alive, vaccinated, and infected (infection continues)
			if end_alive == False: # found a sick person. no need to continue the loop anymore.
				print("breaking loop...")
				break

		# although not necessary, this determines if the end was everyone dead or everyone not sick.
		if end_death != False:
			print("loop managed to finish...")
			print("   ...everyone is dead...")
			end_death = True

		if end_alive != False:
			print("loop managed to finish...")
			print("   ...no-one is infected...")
			end_alive = True

		# is the end neigh?
		if end_alive or end_death:
			print("   ...ending program.")
			print("end alive: " + str(end_alive))
			print("end death: " + str(end_death))
			return False # the end is neigh
		else:
			print("   ...continuing program.")
			return True # the end isn't neigh

	'''
	TODO: Finish this method. This method should run the simulation until everyone in the simulation is dead, or the disease no longer exists in the population.
	To simplify the logic here, we will use the helper method simulation_should_continue() to tell us whether or not we should continue the simulation and run at least 1 more time_step.
	This method should keep track of the number of time steps that have passed using the time_step_counter variable.
	Make sure you remember to the logger's log_time_step() method at the end of each time step, pass in the
	'''
	def run(self):
		Logger.write_metadata(self, self.population_size, self.vaccination_rate, self.virus_name, self.mortality_rate, self.infected_rate, self.initial_infected, self.num_interactions)
		time_step_counter = 0
		# TODO: Remember to set should_continue to an intial call of self.simulation_should_continue()!
		should_continue = self.simulation_should_continue()
		while should_continue:
			# do the time step
			Logger.log_time_step(self,time_step_counter)
			self.time_step()
			time_step_counter += 1
			print("TURN COUNTER: " + str(time_step_counter))
			# Ensure the simulation should continue.
			should_continue = self.simulation_should_continue()
			# TODO: for every iteration of this loop, call self.time_step() to compute another round of this simulation.
			# At the end of each iteration of this loop, remember to rebind should_continue to another call of self.simulation_should_continue()!
		self.total_deaths = self.count_deaths()
		self.total_infected = self.count_infections()
		Logger.log_results(self, time_step_counter, self.total_infected, self.total_deaths, self.population_size, self.population)
		print(f'The simulation has ended after {time_step_counter} turns.')

	# random_people() generates a list of random people.
	# The number of interactions determines how many people.
	def random_people(self, individual):
		random_people = []
		unchosen = self.population.copy()
		# while the number of random people is less then interaction number
		# and while length of unchosen population is not nothing
		while (len(random_people) < self.num_interactions) and (len(unchosen) > 0):
			random_select = random.randint(0,len(unchosen)-1)
			random_person = unchosen.pop(random_select)
			if (random_person.alive) and (random_person != individual):
				random_people.append(random_person)
		return random_people

	'''
	TODO: Finish this method! This method should contain all the basic logic for computing one time step in the simulation.  This includes:
		- For each infected person in the population:
				- Repeat for 100 total interactions:
					- Grab a random person from the population.
						- If the person is dead:
							- continue and grab another new person from the population.
							- Since we don't interact with dead people, this does not count as an interaction.
						- Else:
							- Call simulation.interaction(person, random_person)
							- Increment interaction counter by 1.
	'''
	def time_step(self):
		count_deaths = 0
		count_infection = 0
		for individual in self.population:
			if individual.infected == True:
				count_infection += 1
			if individual.alive == False:
				count_deaths += 1
			self.total_deaths
			if individual.infected != None and individual.alive == True and individual.vaccinated == False:
				Logger.log_person(self, individual)
				random_people = self.random_people(individual)
				for person in random_people:
					self.interaction(individual, person)
					self.currently_infected
			else:
				continue
		self.contagiousify()

	# TODO: Finish this method! This method should be called any time two living people are selected for an interaction.  That means that only living people should be passed into this method.  Assert statements are included to make sure that this doesn't happen.
	'''
	Pass an object (person1=chosen person2=random) into log_interaction instead of individual attributes
	The possible cases you'll need to cover are listed below:
		- random_person is vaccinated:
			Nothing happens to random person.
		- random_person is already infected:
			Nothing happens to random person.
		- random_person is healthy, but unvaccinated:
			- Generate a random number between 0 and 1.
			- If that number is smaller than infection_rate, random_person's ID should be appended to Simulation object's newly_infected array, so that their .infected attribute can be changed to True at the end of the time step.
	TODO: Remember to call self.logger.log_interaction() during this method!
	'''
	def interaction(self, individual, random_person):
		did_infect = None
		assert individual.alive == True
		assert random_person.alive == True
		for person in self.newly_infected:
			if person.identity == random_person.identity:
				did_infect = False
				break
		if did_infect == None:
			if (random_person.vaccinated == True or random_person.infected != None):
				did_infect = False
			else:
				infection_rand = random.random()
				if infection_rand < infection_rate:
					did_infect = True
				else:
					did_infect = False
			if did_infect:
				self.newly_infected.append(random_person)
		Logger.log_interaction(self, individual, random_person, self.newly_infected, did_infect)

	'''
	TODO: Finish this method! This method should be called at the end of every time step.
	This method should iterate through the list stored in self.newly_infected, which should be filled with the IDs of every person created.
	Iterate though this list.åå
	For every person id in self.newly_infected:
		- Find the Person object in self.population that has this corresponding ID.
		- Set this Person's .infected attribute to True.
	NOTE: Once you have iterated through the entire list of self.newly_infected, remember to reset self.newly_infected back to an empty list!
	'''

	def contagiousify(self):
		Logger.log_infection_kickoff(self)
		for person in self.currently_infected:
			Logger.log_infection_survival(self, person, person.resolve_infection(self.mortality_rate))
		for person in self.newly_infected:
			person.infected = self.virus_name
		self.currently_infected = self.newly_infected.copy()
		self.newly_infected = []

	def count_infections(self):
		counter = 0
		for person in self.population:
			if person.infected != None:
				counter += 1
		return counter

	def count_deaths(self):
		counter = 0
		for person in self.population:
			if person.alive == False:
				counter += 1
		return counter

if __name__ == "__main__":
	params = sys.argv[1:]
	if len(params) == 0:
		print("No parameters input...")
		print("Please input parameters")
		print()
		print("   type: integer, INPUT ≥ 1")
		population_size = int(input("Enter population size: "))


		print()
		print("   type: string")
		virus_name = input("Enter virus name: ")

		print()
		print("   type: float, 0 ≤ INPUT ≤ 1")
		mortality_rate = float(input("Enter mortality rate: "))

		print()
		print("   type: float, 0 ≤ INPUT ≤ 1")
		infection_rate = float(input("Enter infection rate: "))

		print()
		print("   type: float, 0 ≤ INPUT ≤ 1")
		vaccination_rate = float(input("Enter vaccination rate: "))

		print()
		print("default: 1")
		print("   type: integer, INPUT ≥ 1")
		initial_infected = input("Enter initial infected: ")

		if initial_infected == "":
			initial_infected = 1
		else:
			initial_infected = int(initial_infected)

		print()
		print("default: 100")
		print("   type: integer, INPUT ≥ 1")
		num_interactions = input("Enter number of interactions: ")

		if num_interactions == "":
			num_interactions = 100
		else:
			num_interactions = int(num_interactions)

	else:
		population_size = int(params[0])
		vaccination_rate = float(params[1])
		virus_name = str(params[2])
		mortality_rate = float(params[3])
		infection_rate = float(params[4])

		if len(params) >= 6:
			initial_infected = int(params[5])
		else:
			initial_infected = 1

		if len(params) == 7:
			num_interactions = int(params[6])
		else:
			num_interactions = 100

	simulation = Simulation(population_size, vaccination_rate, virus_name, mortality_rate, infection_rate, initial_infected, num_interactions)
	simulation.run()
