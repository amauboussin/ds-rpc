import json

identity = lambda x: x
#  string type description: conversion function
python_to_serializable = {
    'list': identity,
    'ndarray': lambda x: x.tolist() if hasattr(x, 'tolist') else x,
    'int': identity,
    'float': identity,
    'str': identity,
    'unicode': identity,
    'int8': int,
    'int32': int,
    'int64': int,
    'uint8': int,
    'uint16': int,
    'float16': float,
    'float32': float,
    'float64': float,
}

iterable_types = {'list', 'ndarray'}


#  general serialization
def _serialize_tuple(args, prefix=''):
    """Serialize a tuple of arguments in a dictionary"""
    data = {}
    for i, arg in enumerate(args):
        data['%s%d' % (prefix, i)] = _cast_python_obj(arg)
    return data


def _cast_python_obj(arg):
    """Cast arg to the appropriate type for serialization"""
    type_description = type(arg).__name__

    if type_description not in python_to_serializable:
        raise Exception('%s is not a supported type. Options include %s' % (type_description, python_to_serializable.keys()))

    #  if collection, then cast each item
    if type_description in iterable_types:
        arg = map(_cast_python_obj, arg)

    return python_to_serializable[type_description](arg)


#  serialize/deserialize client requests
def serialize_python_function(_function, args):

    data = {
        '_function': _function,
        'n_args': len(args),

    }
    data.update(_serialize_tuple(args, 'arg'))

    return data


#  serialize/deserialize result of computation
def serialize_python_result(result):
    """Prepare the result of a Python function for JSON serialization"""
    if type(result).__name__ == 'tuple':
        return _serialize_tuple(result, 'res')
    else:  # single value
        return {'res0': _cast_python_obj(result)}


def deserialize_results(json_response):
    """Deserialize server response into python"""

    if json_response.startswith('500 Error'):
        raise Exception('Remote exception: %s' % json_response)

    result_data = json.loads(json_response)
    get_res = lambda i: result_data.get('res%d' % i, None)

    results = []
    i = 0
    while get_res(i):
        results.append(get_res(i))
        i += 1

    if len(results) > 1:
        return tuple(results)
    elif len(results) == 1:
        return results[0]
    else:
        return None
