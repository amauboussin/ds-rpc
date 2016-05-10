"""Server functionality for ds_rpc system"""
import json
import importlib
import os
import time

from python import serialize_python_result

VERSION = 0.1
LANGUAGES = {'python', 'r'}
TEMP_DIR = os.path.join(os.getcwd(), 'temp')


def deserialize_call(json_data):
    """Parses an inbound request, validates it, and passes it on to a language-specific function for computation"""

    data = json.loads(json_data)

    try:
        client_version = data['version']
        language = data['language']
        _function = data['_function']
        n_args = data['n_args']
    except KeyError:
        raise KeyError('Request must contain language, version, n_args, and _function fields')

    if client_version != VERSION:
        raise Exception('Version mismatch (client %.2f; server %.2f)' % (client_version, VERSION))

    if language not in LANGUAGES:
        raise Exception('%s is not a supported language. Options include %s' % (language, LANGUAGES))

    if language == 'python':
        args = (data.get('arg%d' % i) for i in range(data['n_args']))
        return execute_python_code(_function, args)

    if language == 'r':
        return execute_r_code(json_data, _function, n_args)


def split_function(_function):
    """Split a function to return the module and method that need to be called"""

    split_call = _function.split('.')
    module_name, _function_name = '.'.join(split_call[:-1]), split_call[-1]
    return module_name, _function_name


imported_modules = {}
def execute_python_code(_function, args):
    """Get the result of the given Python function"""

    module_name, _function_name = split_function(_function)

    if module_name in imported_modules:
        module = imported_modules[module_name]
    else:
        try:
            module = importlib.import_module(module_name)
            imported_modules[module_name] = module
        except ImportError:
            raise ImportError('Failed to parse function %s. Cannot import module %s' % (_function, module_name))

    try:
        runnable_function = getattr(module, _function_name)
    except AttributeError:
        raise ImportError('Failed to parse function %s. Cannot find %s in module %s' % (_function, module_name))

    try:
        result = runnable_function(*args)
    except Exception as e:
        raise Exception('Exception while running function %s: %s' % (_function, e))

    return serialize_python_result(result)


def execute_r_code(json_data, _function, n_args):
    """Get the result of the given R function"""
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    timestamp = str(time.time()).replace('.', '')

    module_name, _function_name = split_function(_function)

    #  write json file to be parse in R
    json_path = os.path.join(TEMP_DIR, '%s.json' % timestamp)
    r_code_path = os.path.join(TEMP_DIR, '%s.r' % timestamp)
    res_path = os.path.join(TEMP_DIR, '%sres.json' % timestamp)

    open(json_path, 'w').write(json_data)

    #  write R code to be exectuted
    load_json_lib = 'library("jsonlite")'
    load_function_module = 'library("%s")' % module_name if module_name.strip() else ''
    set_path = 'path <- "%s"' % json_path
    load_data = 'df <- fromJSON(readChar(path, file.info(path)$size))'

    args_list = 'list(%s)' % ', '.join(['df$arg%d' % i for i in range(n_args)])
    call = 'res <- do.call(%s, %s)' % (_function_name, args_list)
    write = 'print(toJSON(list(res0 = res)))'

    r_code = '\n'.join([load_json_lib, load_function_module, set_path, load_data, call, write])

    r_code = """options(warn=-1)
    tryCatch({
      %s
    },
     error = function(e){
       print(e)
     },
    finally = {})""" % r_code

    #  execute R code in shell and capture output
    open(r_code_path, 'w').write(r_code)

    r_data_stream = os.popen('Rscript %s --vanilla' % r_code_path)
    r_data = r_data_stream.read()
    print r_data
    try:
        res = json.loads(r_data)
    except ValueError:
        raise Exception('Error in R: %s' % r_data)

    return res


def clean_old_scripts():
    """Delete the files containing old R code and serialized arguments from the file system"""
    for f in os.listdir(TEMP_DIR):
        os.remove(os.path.join(TEMP_DIR, f))
