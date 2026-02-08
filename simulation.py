import random
from scipy.stats import norm
import logging

class Person:
    def __init__(self, starting_immunity):
        if random.randint(0, 100) < starting_immunity:
            self.immunity = True
        else:
            self.immunity = False
        self.contagiousness = 0
        self.mask = False
        self.contagious_days = 0
        self.friends = int((norm.rvs(size=1, loc=0.5, scale=0.15)[0] * 10).round(0))

    def wear_mask(self):
        self.contagiousness /= 2

class PandemicSimulation:
    def __init__(self, population_size=1000, starting_immunity=1, starting_infecters=1,
                 days_contagious=14, lockdown_day=100, mask_day=100):
        self.population_size = population_size
        self.starting_immunity = starting_immunity
        self.starting_infecters = starting_infecters
        self.days_contagious = days_contagious
        self.lockdown_day = lockdown_day
        self.mask_day = mask_day
        self.people = []
        self._initialize_population()
        self.daily_contagious_count = []

    def _initialize_population(self):
        for _ in range(self.population_size):
            self.people.append(Person(self.starting_immunity))
        
        for _ in range(self.starting_infecters):
            person = self.people[random.randint(0, len(self.people) - 1)]
            person.contagiousness = int((norm.rvs(size=1, loc=0.5, scale=0.15)[0] * 10).round(0) * 10)

    def run_day(self, day, lockdown=False):
        for person in [p for p in self.people if p.contagiousness > 0 and p.friends > 0]:
            people_could_meet = int(person.friends / 2)
            if people_could_meet > 0:
                people_met = random.randint(0, people_could_meet)
            else:
                people_met = 0

            if lockdown:
                people_met = 0

            for _ in range(people_met):
                # Using random.choice is cleaner but randint is fine for index access
                friend_in_question = self.people[random.randint(0, len(self.people) - 1)]
                if (random.randint(0, 100) < person.contagiousness and 
                        friend_in_question.contagiousness == 0 and 
                        not friend_in_question.immunity):
                    friend_in_question.contagiousness = int((norm.rvs(size=1, loc=0.5, scale=0.15)[0] * 10).round(0) * 10)

        for person in [p for p in self.people if p.contagiousness > 0]:
            person.contagious_days += 1
            if person.contagious_days > self.days_contagious:
                person.immunity = True
                person.contagiousness = 0

    def run_simulation(self, days=100):
        lockdown = False
        print(f"Starting simulation for {days} days...")
        for day in range(days):
            if day == self.lockdown_day:
                lockdown = True
            
            if day == self.mask_day:
                for person in self.people:
                    person.wear_mask()

            self.run_day(day, lockdown)
            
            contagious_count = len([p for p in self.people if p.contagiousness > 0])
            self.daily_contagious_count.append(contagious_count)
            # print(f"DAY {day}: {contagious_count} contagious.")

        return self.daily_contagious_count

if __name__ == "__main__":
    sim = PandemicSimulation(population_size=10000, lockdown_day=20, mask_day=100)
    results = sim.run_simulation()
    print("Simulation finished.")
    print(f"Peak contagious: {max(results)}")
