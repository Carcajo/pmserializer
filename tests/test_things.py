import math
import random

t = 5
my_number = 42
my_list = [True, [False, 228], 'pamagiti', []]
my_dict = {'1': {'2': 'aaaaaaaaaaa'}, '-5': 228, 'fd': [my_list], 'Халява': 'прийди'}
my_list2 = {}


def fib(n):
    if n == 0 or n == 1:
        return 1

    else:
        return fib(n - 1) + fib(n - 2)


def mathematics(a, b):
    print(a + b)
    print(a - b)
    print(a / b)
    print(a * b)
    print(math.sin(my_dict['-5']))


def hello():
    print('hello')

    def world():
        print('world')

    return world()


class Dad:
    def __init__(self, second_name):
        self.second_name = second_name


class Gender:
    def __init__(self):
        temp = random.randrange(0, 2, 1)
        if temp == 0:
            self.sex = 'Men'
        else:
            self.sex = 'Women'


class Baby(Dad):
    def __init__(self, first_name, second_name, gender):
        Dad.__init__(self, second_name)
        self.first_name = first_name
        self.gender = gender

    def get_full_name(self):
        return [self.first_name, self.second_name]
