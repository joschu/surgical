from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext = Extension(
    "doo", 
    sources=["doo.pyx"],
    language="c++",
    include_dirs=["/home/joschu/surgical/DiscreteRods","/home/joschu/surgical/utils","/usr/include/eigen2"],
    library_dirs=["/home/joschu/surgical/DiscreteRods"],
    extra_objects=["../DiscreteRods/thread_discrete.o","../DiscreteRods/threadpiece_discrete.o","../DiscreteRods/threadutils_discrete.o"],
    extra_compile_args=["-DISOTROPIC","-DEIGEN_NO_DEBUG","-ggdb","-Dsurgical1"],
)


setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [ext]    
)

