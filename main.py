import random

from lab3 import SerializerJson, SerializerFactory, SerializerYaml, DeserializerYaml, DeserializerJson, Json, Toml, Yaml


def hello():
    print('hello')

    def world():
        print('world')

    world()


def fib(n):
    if n == 0 or n == 1:
        return 1

    else:
        return fib(n - 1) + fib(n - 2)


t = 5
my_number = 42
my_list = [True, [False, 228], 'pamagiti', []]
my_dict = {'1': {'2': 'aaaaaaaaaaa'}, '-5': 228, 'fd': [my_list]}
my_list2 = {'Халява': 'прийди'}


def main():
    pass


class My:
    a = 5


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


f = Gender()


class Baby(Dad):
    def __init__(self, first_name, second_name, gender):
        Dad.__init__(self, second_name)
        self.first_name = first_name
        self.gender = gender

    def get_full_name(self):
        return [self.first_name, self.second_name]

st = SerializerFactory.Serializer.create_serializer('toml')
uy = SerializerFactory.Serializer.create_serializer('json')
la = SerializerFactory.Serializer.create_serializer('yaml')
'''c01=uy.Json.dumps(My)
print(c01)'''
'''c11=st.Toml.dumps(fib)
print(c11)
c21=st.Toml.loads(c11)
print(c21(5))
print(c21.__bases__)
#print(Baby.__bases__)
print(c21.__init__.__globals__)'''
c11 = st.Toml.dumps(Baby)
print(c11)
c21 = st.Toml.loads(c11)
my = c21('aaaa', 'aaa', f)
print(111111111111111111111111111111111111111111111111111111111111111111)
print(my.gender.sex)


def add_four(a):
    x = 2

    def add_some():
        print("x = " + str(x))
        return a + x

    return add_some()


def make_multiplier_of(n):
    def multiplier(x):
        return x * n

    return multiplier


c113 = la.Yaml.dumps(make_multiplier_of)

c213 = la.Yaml.loads(c113)
times3 = c213(3)
print(times3(9))
print(make_multiplier_of.__closure__)
'''c113=uy.Json.dumps(my)

c213=uy.Json.loads(c113)'''

'''x=c2
print(x.a)'''
'''c1=uy.Json.dumps(My)
print(c1)
c2=la.Yaml.loads(c1)'''

'''v1=st.Toml.dumps(hello)
print(v1)'''
# c=st.Toml.dumps(my_number)
if __name__ == '__main__':
    main()
