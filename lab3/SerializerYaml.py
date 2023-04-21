import types
import inspect
import lab3.DeserializerJson
from lab3.constants import NULL, TRUE, FALSE, QUOTATION_MARK, EXTRA_ATTRIBUTE_CLASS_CODE


def serialize(obj):
    '''if obj is None:
        return NULL

    elif obj is True:
        return TRUE

    elif obj is False:
        return FALSE

    elif isinstance(obj, str):
        if obj[0] == QUOTATION_MARK:
            result = obj
        else:
            result = QUOTATION_MARK + obj + QUOTATION_MARK
        return result'''

    '''elif isinstance(obj, dict):
        return serialize_dict(obj, indent, new_indent)

    elif isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set) or isinstance(obj, frozenset):
        return serialize_list(obj, indent, new_indent)
    '''
    if isinstance(obj, (int, float, str, bool)):
        return obj

    elif obj is None:
        return 'None'

    elif isinstance(obj, (list, tuple)):
        return serialize_list(obj)

    elif isinstance(obj, dict):
        return serialize_dict(obj)

    elif inspect.isfunction(obj):
        return serialize_function(obj)

    elif inspect.ismethod(obj):
        return serialize_function(obj)

    elif isinstance(obj, types.CodeType):
        return serialize_code(obj)
    elif inspect.isclass(obj):
        return serialize_class(obj)
    else:
        try:
            return serialize_instance(obj)
        except TypeError:
            raise TypeError


def serialize_instance(obj):
    data = {
        'instance_type': {
            '__class__': serialize(obj.__class__),
            '__dict__': serialize(obj.__dict__),
        }
    }

    result = data

    return result


def serialize_class(obj):
    class_dict = {
        "class_type": {
            "__name__": get_name_class(obj),
            "__bases__": tuple(get_bases_class(obj)),
            "__code__": get_code_class(obj)
        }
    }

    result = serialize_dict(class_dict)

    return result


def get_name_class(obj):
    result = serialize(obj.__name__)

    return result


def get_bases_class(obj):
    data = serialize_list(obj.__bases__)

    result = data
    return result


def serialize_dict_class(obj):
    result = {}

    for key in obj:
        if key in EXTRA_ATTRIBUTE_CLASS_CODE:
            continue
        result[key] = serialize(obj[key])

    return result


def get_code_class(obj):
    if obj.__name__ != 'object':
        data = serialize_dict_class(dict(obj.__dict__))
        result = data

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


def serialize_code(obj: types.CodeType):
    code_dict = {
        "type_code": {
            "co_argcount": obj.co_argcount,
            "co_posonlyargcount": obj.co_posonlyargcount,
            "co_kwonlyargcount": obj.co_kwonlyargcount,
            "co_nlocals": obj.co_nlocals,
            "co_stacksize": obj.co_stacksize,
            "co_flags": obj.co_flags,
            "co_code": list(obj.co_code),
            "co_consts": list(serialize(obj.co_consts)),
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
    result = code_dict

    return result


def serialize_function(obj: types.FunctionType):
    glob = get_globals(obj)
    x = serialize(obj.__code__.co_consts)
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
                    "co_consts": serialize(obj.__code__.co_consts),
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
    result = serialize(function_dict)

    return result


def serialize_list(obj):
    result = []

    for el in obj:
        if el is None:
            result.append("None")

        else:
            result.append(serialize(el))

    return result



def serialize_dict(obj):
    result = {}

    for key in obj:
        '''if obj[key] is None:
            result[key]("None")

        else:'''
        result[key] = serialize(obj[key])

    return result
