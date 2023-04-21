import pytomlpp
import lab3.SerializerYaml
import lab3.DeserializerYaml

class Toml:
    @staticmethod
    def dump(obj, f):
        data = lab3.SerializerYaml.serialize(obj)
        with open(f, 'w') as file:
            pytomlpp.dump(data, file)

    @staticmethod
    def dumps(obj):
        data = lab3.SerializerYaml.serialize(obj)
        return pytomlpp.dumps(data)

    @staticmethod
    def load(f):
        with open(f, 'r+') as file:
            data = pytomlpp.load(file)
        return lab3.DeserializerYaml.deserialize(data)

    @staticmethod
    def loads(s):
        data = pytomlpp.loads(s)
        result = lab3.DeserializerYaml.deserialize(data)

        return result
