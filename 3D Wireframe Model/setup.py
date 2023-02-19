import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = 'Console'

setup(  name = "Wireframe Modeler",
        version = "1.0",
        description = "A simple 3D modeling program.",
        options = {"build_exe": build_exe_options},
        executables = [Executable("model.py", base=base)])
