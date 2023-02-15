import sys
import importlib.util
from inspect import getmembers, isfunction
import belay

file_path = "/Users/roaldarbol/MEGA/Documents/sussex/projects/bux-recorder/python/belay_single_script.py"
module_name = "belay_single_script"

spec = importlib.util.spec_from_file_location(module_name, file_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# check if it's all there..
fcts = []


def bla(mod):
    # for name in dir(mod):
    for o in getmembers(mod):
        print(o)
        if isfunction(o[0]):
            fcts.append(o[0])


bla(module)

# ClassName = device.task(ClassName)
