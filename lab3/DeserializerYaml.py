import types


def deserialize(obj):
    if isinstance(obj, (int, float, bool)):
        return obj
    if isinstance(obj, str):
        if str == 'None':
            return None
        else:
            return obj
    elif isinstance(obj, list):
        return deserialize_list(obj)
    elif isinstance(obj, tuple):
        return deserialize_tuple(obj)
    elif isinstance(obj, dict):
        if 'function_type' in obj:
            return deserialize_function(obj)
        elif 'type_code' in obj:
            return deserialize_code(obj)
        elif 'class_type' in obj:
            return deserialize_class(obj)
        elif 'instance_type' in obj:
            return deserialize_instance(obj)
        else:
            return deserialize_dict(obj)
    else:
        raise TypeError


def deserialize_class(cls):
    if cls['class_type']['__name__'] == 'object':
        return object

    else:
        x = deserialize(cls['class_type']["__bases__"])
        y = deserialize(cls['class_type']["__code__"])
        result = type(cls['class_type']["__name__"], tuple(deserialize(cls['class_type']["__bases__"])),
                      deserialize(cls['class_type']["__code__"]))

        return result


def deserialize_dict(obj):
    result = {}

    for key in obj:
        if obj[key] == "None":
            result[key] = None
        else:
            result[key] = deserialize(obj[key])

    return result


def deserialize_instance(obj):
    def __init__(self):
        pass

    cls = obj['instance_type']['class']
    temp = cls.__init__
    cls.__init__ = __init__
    result = obj['instance_type']['class']()
    result.__dict__ = obj['instance_type']['dict']
    result.__init__ = temp
    result.__class__.__init__ = temp
    return result


def get_code(obj):
    result = (obj['co_argcount'],
              obj['co_posonlyargcount'],
              obj['co_kwonlyargcount'],
              obj['co_nlocals'],
              obj['co_stacksize'],
              obj['co_flags'],
              bytes(obj['co_code']),
              deserialize(tuple(obj['co_consts'])),
              tuple(obj['co_names']),
              tuple(obj['co_varnames']),
              obj['co_filename'],
              obj['co_name'],
              obj['co_firstlineno'],
              bytes(obj['co_lnotab']),
              tuple(obj['co_freevars']),
              tuple(obj['co_cellvars']))

    return result


def deserialize_code(obj: dict):
    result = types.CodeType(*get_code(obj['type_code']))

    return result


def deserialize_function(obj: dict):
    my_code = get_code(obj['function_type']['__code__']['code_type'])
    result = types.FunctionType(types.CodeType(*my_code), deserialize(obj['function_type']['__globals__']),
                                obj['function_type']['__name__'])

    for key in obj['function_type']['__globals__']:

        try:
            result.__globals__[key] = __import__(obj['function_type']['__globals__'][key])
        except:
            pass

    result.__globals__.update({result.__name__: result})
    result.__globals__["__builtins__"] = __import__("builtins")

    return result


def deserialize_list(obj):
    result = []

    for el in obj:
        if el == "None":
            result.append(None)
        else:
            result.append(deserialize(el))

    return result


def deserialize_tuple(obj):
    result = tuple(deserialize_list(obj))

    return result


def deserialize_instance(obj):
    obj['instance_type']['__class__'] = deserialize(obj['instance_type']['__class__'])

    def __init__(self):
        pass

    cls = obj['instance_type']['__class__']
    temp = cls.__init__
    cls.__init__ = __init__
    result = obj['instance_type']['__class__']()
    result.__dict__ = obj['instance_type']['__dict__']
    result.__init__ = temp
    result.__class__.__init__ = temp
    return result
