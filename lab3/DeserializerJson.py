import types
from lab3.constants import NULL, TRUE, FALSE, QUOTATION_MARK, MINUS, EXTRA_CHARACTERS_IN_LIST, \
    EXTRA_CHARACTERS_IN_DICT


def deserialize(s, index=0):
    if s[index:index + 4] == NULL:
        index += 4

        return None, index

    elif s[index:index + 4] == TRUE:
        index += 4

        return True, index

    elif s[index:index + 5] == FALSE:
        index += 5

        return False, index

    elif s[index].isdigit() or s[index] == MINUS:
        result, index = deserialize_number(s, index)

        return result, index

    elif s[index] == QUOTATION_MARK:
        result, index = deserialize_string(s, index + 1)

        return result, index

    elif s[index] == '[':
        result, index = deserialize_list(s, index)

        return result, index

    elif s[index] == '{':
        result, index = deserialize_dict(s, index)

        return result, index

    else:
        raise TypeError


def deserialize_class(cls):
    if cls['class_type']['__name__'] == 'object':
        return object

    else:
        result = type(cls['class_type']["__name__"], tuple(cls['class_type']["__bases__"]),
                      cls['class_type']["__code__"])

        return result


def deserialize_dict(s, index):
    result = {}
    in_key = True
    now_key = None
    index += 1

    while s[index] != '}':
        if s[index] in EXTRA_CHARACTERS_IN_DICT:
            index += 1

        elif s[index] == QUOTATION_MARK and in_key:
            now_key, index = deserialize(s, index)
            result[now_key] = None
            in_key = False

        else:
            value, index = deserialize(s, index)
            result[now_key] = value
            in_key = True

    if 'function_type' in result:
        result = deserialize_function(result)

    elif 'class_type' in result:
        result = deserialize_class(result)

    elif 'type_code' in result:
        result = deserialize_code(result)
    elif 'instance_type' in result:
        result = deserialize_instance(result)
    return result, index + 1


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
              tuple(obj['co_consts']),
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
    result = types.FunctionType(types.CodeType(*my_code), obj['function_type']['__globals__'],
                                obj['function_type']['__name__'])

    for key in obj['function_type']['__globals__']:

        try:
            result.__globals__[key] = __import__(obj['function_type']['__globals__'][key])
        except:
            pass

    result.__globals__.update({result.__name__: result})
    result.__globals__["__builtins__"] = __import__("builtins")

    return result




def deserialize_list(s, index):
    result = []
    index += 1

    while s[index] != ']':
        if s[index] in EXTRA_CHARACTERS_IN_LIST:
            index += 1

        else:
            obj, index = deserialize(s, index)

            result.append(obj)

    return result, index + 1


def deserialize_number(s: str, index):
    end = index

    while end != len(s) and (s[end].isdigit() or s[end] == '.' or s[end] == '-'):
        end += 1

    try:
        result = int(s[index:end])

    except ValueError:
        try:
            result = float(s[index:end])

        except ValueError:
            raise ValueError

    return result, end + 1


def deserialize_string(s, index):
    end = index

    while s[end] != QUOTATION_MARK:
        end += 1

    return s[index:end], end + 1
