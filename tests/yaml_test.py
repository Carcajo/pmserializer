from unittest import TestCase
from tests.test_things import my_number, my_list, my_dict, fib, hello, Baby, mathematics,Gender
from lab2 import SerializerFactory


class TestFunction(TestCase):
    def setUp(self):
        self.my_parser = SerializerFactory.Serializer.create_serializer('yaml')
        self.file = 'temp.yaml'

    def test_parser_obj(self):
        self.my_parser.Yaml.dump(my_number, self.file)
        result = self.my_parser.Yaml.load(self.file)
        self.assertEqual(result, my_number)

        self.my_parser.Yaml.dump(my_list, self.file)
        result = self.my_parser.Yaml.load(self.file)
        self.assertEqual(result, my_list)

        self.my_parser.Yaml.dump(my_dict, self.file)
        result = self.my_parser.Yaml.load(self.file)
        self.assertEqual(result, my_dict)

    def test_parser_function(self):
        self.my_parser.Yaml.dump(fib, self.file)
        result = self.my_parser.Yaml.load(self.file)
        self.assertEqual(result(10), fib(10))

        data = self.my_parser.Yaml.dumps(hello)
        result = self.my_parser.Yaml.loads(data)
        self.assertEqual(result(), hello())

        self.my_parser.Yaml.dump(mathematics, self.file)
        result = self.my_parser.Yaml.load(self.file)
        self.assertEqual(result(4.2, 2.4), mathematics(4.2, 2.4))

    def test_parser_class(self):
        self.my_parser.Yaml.dump(Baby, self.file)
        data = self.my_parser.Yaml.load(self.file)
        gender = Gender()
        result = data('Maxim', 'Puhov',gender)
        test_result = Baby('Maxim', 'Puhov',gender)
        self.assertEqual(result.get_full_name(), test_result.get_full_name())
        self.assertEqual(result.gender.sex, test_result.gender.sex)

        self.my_parser.Yaml.dump(result, self.file)
        data = self.my_parser.Yaml.load(self.file)
        self.assertEqual(result.get_full_name(), data.get_full_name())
