# Allows the use of py2exe to build to a standalone executable
from distutils.core import setup
import py2exe

setup(console=['cell_gen.py'])
