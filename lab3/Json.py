import lab3.DeserializerJson
from lab3 import SerializerJson


class Json:
    @staticmethod
    def dump(obj, fp, indent=0):
        result = Json.dumps(obj, indent)

        with open(fp, 'w') as file:
            file.write(result)

    @staticmethod
    def dumps(obj, indent=0):
        result = SerializerJson.serialize(obj, indent)

        return result

    @staticmethod
    def load(fp):
        with open(fp, 'r') as file:
            data = file.read()

        result = Json.loads(data)

        return result

    @staticmethod
    def loads(s):
        result = lab3.DeserializerJson.deserialize(s)[0]

        return result
