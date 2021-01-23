from setuptools import setup
from Cython.Build import cythonize

setup(
    package_dir={'cython_test': ''},
    ext_modules = cythonize("rectangle.pyx")
)
