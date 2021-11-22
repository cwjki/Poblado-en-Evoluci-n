import simpy
import time
from sys import argv
from classes import Population
from random import randint, random
from utils import get_older, borns, deaths, pregnants, matchs, breakups


class PopulationEvolution:
    def __init__(self, m, w, years):
        self.years = years
        self.events = [borns, deaths, pregnants, breakups, matchs]
        self.population = Population()
        self.env = simpy.Environment()

        self.population.generate_population(m, w)
        self.env.process(self.run())
        start = time.time()
        self.env.run(until=years * 12)
        self.duration = time.time() - start

    def run(self):
        while True:
            get_older(self.population)
            events = [e for e in self.events]
            while len(events) > 0:
                r = randint(0, len(events) - 1)
                events.pop(r)(self.env, self.population)
            yield self.env.timeout(1)
            print(
                f'Población Actual: {self.population.count()} en el mes {self.env.now}')


if __name__ == '__main__':
    if len(argv) != 3:
        print("Se debe especificar la cantidad de hombres y mujeres iniciales")
        exit()
    p = PopulationEvolution(int(argv[1]), int(argv[2]), 100)
