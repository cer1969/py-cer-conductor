
from setuptools import setup
from Cython.Build import cythonize

setup(
    name = "zxlib",
    ext_modules = cythonize("zxlib.pyx", annotate=True),
    #include_dirs=["zxsrc"]
)