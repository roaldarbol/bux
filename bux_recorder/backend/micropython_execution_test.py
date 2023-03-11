import importlib.util
import sys
import belay
from inspect import getmembers, isfunction

# importlib.import_module("/Users/roaldarbol/MEGA/Documents/sussex/projects/bux-recorder/python/new.py")


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


if __name__ == "__main__":
    # Find input device - will be excluded
    devices = belay.list_devices()
    selected_port = devices[-1]

    # Try it out
    path = "/Users/roaldarbol/MEGA/Documents/sussex/research/experiments/"
    filepath = "/Users/roaldarbol/MEGA/Documents/sussex/research/experiments/experiments/protocols/test_led.py"

    # A few key inputs for our run_belay function
    functions = list_methods_in_module(path, filepath)
    function_n = 0  # "testing_it_all"
    selected_function = functions[function_n][0]

    # Run some code :-)
    run_belay_script(
        path=path, filepath=filepath, device=selected_port, function="testing_it_all"
    )
