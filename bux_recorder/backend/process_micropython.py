import importlib.util
import sys
from inspect import getmembers, isfunction


def list_methods_in_module(path, filepath):
    sys.path.append(path)
    spec = importlib.util.spec_from_file_location("belay_script", filepath)
    user_module = importlib.util.module_from_spec(spec)
    sys.modules["module.name"] = user_module
    spec.loader.exec_module(user_module)
    methods = getmembers(user_module, isfunction)
    return methods


def run_belay_script(path, filepath, device, function):
    sys.path.append(path)
    spec = importlib.util.spec_from_file_location("belay_script", filepath)
    user_module = importlib.util.module_from_spec(spec)
    sys.modules["module.name"] = user_module
    spec.loader.exec_module(user_module)
    function_to_call = getattr(user_module, function)
    function_to_call(device)
