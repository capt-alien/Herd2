class Logger(object):

    def __init__(self, file_name):
        self.file_name = file_name

        # https://www.pythonforbeginners.com/cheatsheet/python-file-handling
        # Also got help from Nolen Kovacik for this one:
    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
                       basic_repro_num, ):
        with open(self.file_name, "w") as file:
            file.write("==============METADATA=====================\n")
            file.write(f"{pop_size}\t {vacc_percentage}\t {virus_name}\t {mortality_rate}\t")
            file.write("\n========================================================\n")
            file.write(f"     Population Size: {pop_size}\n")
            file.write(f"    Vaccination Rate: {vacc_percentage}\n")
            file.write(f"          Virus Name: {virus_name}\n" )
            file.write(f"      Mortality Rate: {mortality_rate}\n")
            file.write("\n========================================================\n")
            # file.write(f"   # of interactions: {interactions}\n")
        file.close()


    def log_interaction(self, person1, person2):
        with open(self.file_name, "a") as file:
            # if person1 has the virus then person1 infects person2
            if person1.infection != None:
                file.write(f" {person1._id} infects {person2._id} because already sick. \n")
            # if person2 has the virus then person1 infects person2
            if person2.infection != None:
                file.write(f" {person2._id} infects {person1._id} because already sick. \n")
            if person1.is_vaccinated == True:
                file.write(f" {person1._id} didn't infect {person2._id} because vaccinated. \n")
            if person2.is_vaccinated == True:
                file.write(f" {person2._id} didn't infect {person1._id} because vaccinated. \n")
        file.close()

    def log_infection_survival(self, person, population):
        did_die_from_infection = None
        with open(self.file_name, "a") as file:
            for person in population:
                if person.is_alive == True:
                    did_die_from_infection == False
                    file.write(f" Person ID: {person._id} survived infection and is now immune\n")
            else:
                did_die_from_infection = True
                file.write(f" Person ID: {person._id} died from infection.\n")
            file.close()

    def log_time_step(self, time_step_number):
            next_step = int(time_step_number + 1)
            with open(self.file_name, "a") as file:
                file.write("==============TIME STEP==========================\n")
                file.write("\n ==============================================\n")
                file.write(f"\n Time step {time_step_number} has ended, starting time step {next_step}\n")
                # file.write(f"Total Deaths: {death_counter}")
                file.write("\n ==============================================\n")
                file.close()
