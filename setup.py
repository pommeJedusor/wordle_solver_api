from setuptools import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize("Solver.py", "second_word.py"))
