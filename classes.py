from utils import uniform, desired_child_number


class Person:
    def __init__(self, id, age):
        self.age = age
        self.id = id
        self._is_alive = True
        self.partner = None
        self.childs = 0
        self.looking_for_couple = True
        self.time_alone = 0
        self.desired_childs = self.generate_desired_childs()

    def add_child(self):
        self.childs += 1

    def get_older(self):
        self.age += 1
        self.time_alone = max(0, self.time_alone - 1)

    def get_years(self):
        return self.age // 12

    def get_childs(self):
        return self.childs

    def get_desired_childs(self):
        if self.get_state() == 'in a couple':
            return min(self.desired_childs, self.partner.desired_childs)
        return self.desired_childs

    def is_alive(self):
        return self._is_alive

    def die(self):
        self._is_alive = False

    def add_partner(self, partner):
        self.partner = partner

    def breakup(self):
        self.partner.partner = None
        self.partner = None

    def generate_desired_childs(self):
        max_childs = [(p, n) for n, p in desired_child_number.items()]
        max_childs.sort()
        u = uniform(0, 1)
        for p in max_childs:
            if u <= p[0]:
                return p[1]
        return max_childs[-1][1]

    def get_state(self):
        if not self.looking_for_couple:
            if self.time_alone == 0:
                self.looking_for_couple = True
                return 'single'
            return 'time alone'

        if self.partner is None:
            return 'single'

        if not self.partner.is_alive():
            if self.time_alone == 0:
                self.partner = None
                self.looking_for_couple = True
                return 'single'
            return 'time alone'

        return 'in a couple'

    def start_time_alone(self, time):
        self.looking_for_couple = False
        self.time_alone = time


class Man(Person):
    def __init__(self, id, age):
        Person.__init__(self, id, age)

    def get_sex(self):
        return 'Male'


class Woman(Person):
    def __init__(self, id, age):
        Person.__init__(self, id, age)
        self._is_pregnant = False
        self.pregnant_time = 0

    def get_sex(self):
        return 'Female'

    def is_pregnant(self):
        return self._is_pregnant

    def start_pregnant(self, time):
        self._is_pregnant = True
        self.pregnant_time = time

    def end_pregnant(self):
        self._is_pregnant = False

    def give_birth_time(self, time):
        if not self.is_pregnant():
            return False
        if time - self.pregnant_time >= 9:
            self._is_pregnant = False
            return True
        return False


class Population:
    def __init__(self):
        self.people = []
        self.new_death = []
        self.death = []
        self.person_id = 1

    def generate_population(self, m, w):
        for i in range(m):
            age = uniform(0, 125 * 12) // 1
            self.people.append(Man(self.person_id, age))
            self.person_id += 1

        for i in range(w):
            age = uniform(0, 125 * 12) // 1
            self.people.append(Woman(self.person_id, age))
            self.person_id += 1

    def add_person(self):
        u = uniform(0, 1)
        if u < 0.5:
            self.people.append(Man(self.person_id, 0))
        else:
            self.people.append(Woman(self.person_id, 0))
        self.person_id += 1

    def count(self):
        alive = 0
        for person in self.people:
            alive += 1 if person.is_alive else 0
        return alive

    def __iter__(self):

        self.index = 0
        self.new_death = []
        return self

    def __next__(self):
        while True:
            if self.index == len(self.people):
                for dp in self.new_death[::-1]:
                    self.death.append(self.people.pop(dp))
                raise StopIteration
            p = self.people[self.index]
            if not p.is_alive():
                self.new_death.append(self.index)
            self.index += 1
            if p.is_alive():
                return p
