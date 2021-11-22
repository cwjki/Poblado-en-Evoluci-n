from math import log
from random import random


# Random Var
def exponential(lmbda):
    return -log(random()) / lmbda


def uniform(a, b):
    return (b - a) * random() + a


# Events
def borns(env, population):
    for person in population:
        if person.get_sex() == 'Male' or not person.is_pregnant() or not person.give_birth_time(env.now):
            continue

        person.end_pregnant()
        u = uniform(0, 1)
        for i in range(number_childs(u)):
            person.add_child()
            population.add_person()


def deaths(env, population):
    for person in population:
        u = uniform(0, 1)
        if u < death_probability(person.get_years(), person.get_sex()):
            if person.get_state() == 'in a couple':
                person.partner.start_time_alone(
                    generate_time_alone(person.partner.get_years()))
                person.die()


def pregnants(env, population):
    pregnant_count = 0
    for person in population:
        if person.get_sex() == 'Male' or person.is_pregnant() or person.get_state() != 'in a couple' or person.get_childs() >= person.get_desired_childs():
            continue
        u = uniform(0, 1)
        if u < pregnant_probility(person.get_years()):
            person.start_pregnant(env.now)
            pregnant_count += 1


def matchs(env, population):
    single_men = [p for p in population if p.get_sex(
    ) == 'Male' and p.get_state() == 'single']
    single_women = [p for p in population if p.get_sex(
    ) == 'Female' and p.get_state() == 'single']

    for man in single_men:
        u = uniform(0, 1)
        if u > looking_for_couple_probability(man.get_years()):
            continue
        for woman in single_women:
            u = uniform(0, 1)
            if u > looking_for_couple_probability(man.get_years()):
                continue
            u = uniform(0, 1)
            if u < couple_probability(man.get_years(), woman.get_years()):
                man.add_partner(woman)
                woman.add_partner(man)
                break


def breakups(env, population):
    for person in population:
        if person.get_state() == 'in a couple':
            u = uniform(0, 1)
            if u < breakups_probability:
                person.partner.start_time_alone(
                    generate_time_alone(person.partner.get_years()))
                person.start_time_alone(
                    generate_time_alone(person.get_years()))
                person.breakup()


def generate_time_alone(age):
    if age < 12:
        return 0
    if age < 15:
        return exponential(1/3)
    if age < 35:
        return exponential(1/6)
    if age < 45:
        return exponential(1/12)
    if age < 60:
        return exponential(1/24)
    return exponential(1/48)


def get_older(population):
    for person in population:
        person.get_older()


# Probabilities
breakups_probability = 0.2


def death_probability(age, sex):
    if age <= 12:
        return 0.25 / (12 * 12)
    if age <= 45:
        return 0.1 / (12 * 33) if sex == 'Male' else 0.15 / (12 * 33)
    if age <= 76:
        return 0.3 / (12 * 31) if sex == 'Male' else 0.35 / (12 * 31)
    if age <= 125:
        return 0.7 / (12 * 49) if sex == 'Male' else 0.65 / (12 * 49)
    return 1


def pregnant_probility(age):
    if age < 12:
        return 0
    if age < 15:
        return 0.2
    if age < 21:
        return 0.45
    if age < 35:
        return 0.8
    if age < 45:
        return 0.4
    if age < 60:
        return 0.2
    if age < 125:
        return 0.05
    return 0


def looking_for_couple_probability(age):
    if age < 12:
        return 0
    if age < 15:
        return 0.6
    if age < 21:
        return 0.65
    if age < 35:
        return 0.8
    if age < 45:
        return 0.6
    if age < 60:
        return 0.5
    if age < 125:
        return 0.2
    return 0


def couple_probability(age1, age2):
    diff = abs(age1-age2)
    if diff < 5:
        return 0.45
    if diff < 10:
        return 0.4
    if diff < 15:
        return 0.35
    if diff < 20:
        return 0.25
    return 0.15


def number_childs(p):
    if p < 0.02:
        return 5
    if p < 0.06:
        return 4
    if p < 0.14:
        return 3
    if p < 0.32:
        return 2
    return 1


desired_child_number = {
    1: 0.6,
    2: 0.75,
    3: 0.35,
    4: 0.2,
    5: 0.1,
    10: 0.05
}
