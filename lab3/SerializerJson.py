import types
import inspect
import lab3.DeserializerJson
from lab3.constants import NULL, TRUE, FALSE, QUOTATION_MARK, EXTRA_ATTRIBUTE_CLASS_CODE


def serialize(obj, indent, new_indent=0):
    if obj is None:
        return NULL

    elif obj is True:
        return TRUE

    elif obj is False:
        return FALSE

    elif isinstance(obj, (int, float)):
        return str(obj)

    elif isinstance(obj, str):
        if obj[0] == QUOTATION_MARK:
            result = obj
        else:
            result = QUOTATION_MARK + obj + QUOTATION_MARK
        return result

    elif isinstance(obj, dict):
        return serialize_dict(obj, indent, new_indent)

    elif isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set) or isinstance(obj, frozenset):
        return serialize_list(obj, indent, new_indent)

    elif inspect.isclass(obj):
        return serialize_class(obj, indent, new_indent)

    elif inspect.isfunction(obj):
        return serialize_function(obj, indent, new_indent)

    elif isinstance(obj, types.CodeType):
        return serialize_code(obj, indent, new_indent)

    elif inspect.ismethod(obj):
        return serialize_function(obj, indent, new_indent)

    else:
        try:
            return serialize_instance(obj, indent, new_indent)
        except TypeError:
            raise TypeError


def serialize_instance(obj, indent, new_indent):
    data = {
        'instance_type': {
            'class': obj.__class__,
            'dict': obj.__dict__,
        }
    }

    result = serialize_dict(data, indent, new_indent)

    return result


def serialize_class(obj, indent, new_indent):
    class_dict = {
        "class_type": {
            "__name__": get_name_class(obj, indent, new_indent),
            "__bases__": tuple(get_bases_class(obj, indent, new_indent)),
            "__code__": get_code_class(obj, indent, new_indent)
        }
    }

    result = serialize_dict(class_dict, indent, new_indent)

    return result


def get_name_class(obj, indent, new_indent):
    result = serialize(obj.__name__, indent, new_indent)

    return result


def get_bases_class(obj, indent, new_indent):
    data = serialize_list(obj.__bases__, indent, new_indent)
    result = lab3.DeserializerJson.deserialize_list(data, 0)[0]

    return result


def serialize_dict_class(obj, indent, new_indent=0):
    if len(obj) == 0:
        return '{}'

    else:
        result = '{\n'
        new_indent += indent

        for key in list(obj)[:len(obj) - 1]:

            if key in EXTRA_ATTRIBUTE_CLASS_CODE:
                continue

            result += ' ' * new_indent + QUOTATION_MARK + str(key) + QUOTATION_MARK + ': ' \
                      + serialize(obj[key], indent, new_indent) + ',\n'

        if list(obj)[len(obj) - 1] not in EXTRA_ATTRIBUTE_CLASS_CODE:
            result += ' ' * new_indent + QUOTATION_MARK + str(list(obj)[len(obj) - 1]) \
                      + QUOTATION_MARK + ': ' + serialize(obj[list(obj)[len(obj) - 1]], indent, new_indent) + '\n'

        result += ' ' * (new_indent - indent) + '}'

    return result


def get_code_class(obj, indent, new_indent):
    if obj.__name__ != 'object':
        data = serialize_dict_class(dict(obj.__dict__), indent, new_indent)
        result = lab3.DeserializerJson.deserialize_dict(data, 0)[0]

    else:
        result = {}

    return result


def get_globals(obj):
    result = {}

    for key in obj.__globals__:

        if isinstance(obj.__globals__[key], types.ModuleType):
            result[key] = obj.__globals__[key].__name__

        elif key in obj.__code__.co_names and obj.__name__ != key:
            result[key] = obj.__globals__[key]

    return result


def serialize_code(obj: types.CodeType, indent, new_indent):
    code_dict = {
        "type_code": {
            "co_argcount": obj.co_argcount,
            "co_posonlyargcount": obj.co_posonlyargcount,
            "co_kwonlyargcount": obj.co_kwonlyargcount,
            "co_nlocals": obj.co_nlocals,
            "co_stacksize": obj.co_stacksize,
            "co_flags": obj.co_flags,
            "co_code": list(obj.co_code),
            "co_consts": obj.co_consts,
            "co_names": obj.co_names,
            "co_varnames": obj.co_varnames,
            "co_filename": obj.co_filename,
            "co_name": obj.co_name,
            "co_firstlineno": obj.co_firstlineno,
            "co_lnotab": list(obj.co_lnotab),
            "co_freevars": obj.co_freevars,
            "co_cellvars": obj.co_cellvars
        }
    }

    result = serialize_dict(code_dict, indent, new_indent)

    return result


def serialize_function(obj: types.FunctionType, indent, new_indent):
    glob = get_globals(obj)

    function_dict = {
        "function_type": {
            "__globals__": glob,
            "__name__": obj.__name__,
            "__code__": {
                "code_type": {
                    "co_argcount": obj.__code__.co_argcount,
                    "co_posonlyargcount": obj.__code__.co_posonlyargcount,
                    "co_kwonlyargcount": obj.__code__.co_kwonlyargcount,
                    "co_nlocals": obj.__code__.co_nlocals,
                    "co_stacksize": obj.__code__.co_stacksize,
                    "co_flags": obj.__code__.co_flags,
                    "co_code": list(obj.__code__.co_code),
                    "co_consts": obj.__code__.co_consts,
                    "co_names": obj.__code__.co_names,
                    "co_varnames": obj.__code__.co_varnames,
                    "co_filename": obj.__code__.co_filename,
                    "co_name": obj.__code__.co_name,
                    "co_firstlineno": obj.__code__.co_firstlineno,
                    "co_lnotab": list(obj.__code__.co_lnotab),
                    "co_freevars": obj.__code__.co_freevars,
                    "co_cellvars": obj.__code__.co_cellvars
                }
            }
        }
    }

    result = serialize_dict(function_dict, indent, new_indent)

    return result


def serialize_dict(obj, indent, new_indent=0):
    if len(obj) == 0:
        return '{}'

    else:
        result = '{\n'
        new_indent += indent

        for key in list(obj)[:len(obj) - 1]:
            result += ' ' * new_indent + QUOTATION_MARK + str(key) + QUOTATION_MARK + ': ' \
                      + serialize(obj[key], indent, new_indent) + ',\n'

        result += ' ' * new_indent + QUOTATION_MARK + str(list(obj)[len(obj) - 1]) + QUOTATION_MARK + ': ' + \
                  serialize(obj[list(obj)[len(obj) - 1]], indent, new_indent) + '\n'
        result += ' ' * (new_indent - indent) + '}'

    return result


def serialize_list(obj, indent, new_indent=0):
    if len(obj) == 0:
        return '[]'

    else:
        result = '[\n'
        new_indent += indent

        for el in obj[:len(obj) - 1]:
            result += ' ' * new_indent + serialize(el, indent, new_indent) + ',\n'

        result += ' ' * new_indent + serialize(obj[len(obj) - 1], indent, new_indent) + '\n'
        result += ' ' * (new_indent - indent) + ']'

    return result
