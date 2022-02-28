from logic import main      # this comes from a compiled binary
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
ext_modules = [
    Extension("Workflow",  ["workflow.py"]),
    #   ... all your modules that need be compiled ...
]
setup(
    name='Workflow',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)
main()
