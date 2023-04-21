from unittest import TestCase
from tests.test_things import my_number, my_list, my_dict, fib, mathematics, hello, Baby, Gender
from lab3 import SerializerFactory


class TestFunction(TestCase):
    def setUp(self):
        self.my_parser = SerializerFactory.Serializer.create_serializer('json')
        self.file = 'temp.json'
    def test_serializer_factory(self):
        with self.assertRaises(ValueError):
            self.my_parser = SerializerFactory.Serializer.create_serializer('abracadabra')

    def test_parser_obj(self):
        self.my_parser.Json.dump(my_number, self.file, indent=2)
        result = self.my_parser.Json.load(self.file)
        self.assertEqual(result, my_number)

        self.my_parser.Json.dump(my_list, self.file, indent=2)
        result = self.my_parser.Json.load(self.file)
        self.assertEqual(result, my_list)

        self.my_parser.Json.dump(my_dict, self.file, indent=2)
        result = self.my_parser.Json.load(self.file)
        self.assertEqual(result, my_dict)

    def test_parser_function(self):
        self.my_parser.Json.dump(fib, self.file, indent=2)
        result = self.my_parser.Json.load(self.file)
        self.assertEqual(result(10), fib(10))

        self.my_parser.Json.dump(mathematics, self.file, indent=2)
        result = self.my_parser.Json.load(self.file)
        self.assertEqual(result(4.2, 2.4), mathematics(4.2, 2.4))

        self.my_parser.Json.dump(hello, self.file, indent=2)
        result = self.my_parser.Json.load(self.file)
        self.assertEqual(result(), hello())

    def test_parser_class(self):
        self.my_parser.Json.dump(Baby, self.file, indent=2)
        data = self.my_parser.Json.load(self.file)
        gender=Gender()
        result = data('Maxim', 'Puhov',gender)
        test_result = Baby('Maxim', 'Puhov',gender)
        self.assertEqual(result.get_full_name(), test_result.get_full_name())
        self.assertEqual(result.gender.sex, test_result.gender.sex)

        self.my_parser.Json.dump(result, self.file, indent=2)
        data = self.my_parser.Json.load(self.file)
        self.assertEqual(result.get_full_name(), data.get_full_name())
