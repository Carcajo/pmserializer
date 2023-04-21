from unittest import TestCase
from tests.test_things import hello, Baby, my_list2, my_number, my_list, fib, mathematics,my_dict,Gender
from lab3 import SerializerFactory


class TestFunction(TestCase):
    def setUp(self):
        self.my_parser = SerializerFactory.Serializer.create_serializer('toml')
        self.file = 'temp.toml'

    def test_parser_function(self):
        self.my_parser.Toml.dump(fib, self.file)
        result = self.my_parser.Toml.load(self.file)
        self.assertEqual(result(10), fib(10))

        data = self.my_parser.Toml.dumps(hello)
        result = self.my_parser.Toml.loads(data)
        self.assertEqual(result(), hello())

        self.my_parser.Toml.dump(mathematics, self.file)
        result = self.my_parser.Toml.load(self.file)
        self.assertEqual(result(4.2, 2.4), mathematics(4.2, 2.4))

    def test_parser_class(self):
        self.my_parser.Toml.dump(Baby, self.file)
        data = self.my_parser.Toml.load(self.file)
        gender = Gender()
        result = data('Maxim', 'Puhov',gender)
        test_result = Baby('Maxim', 'Puhov',gender)
        self.assertEqual(result.get_full_name(), test_result.get_full_name())
        self.assertEqual(result.gender.sex, test_result.gender.sex)

        self.my_parser.Toml.dump(result, self.file)
        data = self.my_parser.Toml.load(self.file)
        self.assertEqual(result.get_full_name(), data.get_full_name())
