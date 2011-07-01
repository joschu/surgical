from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from glob import glob
from os.path import join

SURGICAL = "/home/joschu/surgical"

ext = Extension(
    "doo", 
    sources=["doo.pyx"],
    language="c++",
    include_dirs=["/home/joschu/surgical/DiscreteRods","/home/joschu/surgical/utils","/usr/include/eigen2","eigen_src"],
    library_dirs=["/usr/lib",join(SURGICAL,"DiscreteRods")],
    libraries=["glut","gle"],
    extra_objects=glob(join(SURGICAL,"DiscreteRods/*.o"))+glob("./*.o"),
    extra_compile_args=["-DISOTROPIC","-DEIGEN_NO_DEBUG","-ggdb","-Dsurgical1"],
)


setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [ext]    
)

