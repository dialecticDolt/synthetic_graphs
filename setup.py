from Cython.Build import cythonize
from setuptools import setup, find_packages
from setuptools.extension import Extension
import os

#os.environ["CC"] = 'nvcc_wrapper'
#os.environ["CXX"] = 'nvcc_wrapper'

def scandir(dir, files=[]):
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        if os.path.isfile(path) and path.endswith(".pyx"):
            files.append(path.replace(os.path.sep, ".")[:-4])
        elif os.path.isdir(path):
            scandir(path, files)
    return files

def makeExtension(extName):
    extPath = extName.replace(".", os.path.sep)+".pyx"
    return Extension(
        extName,
        [extPath],
        language='c++',
        extra_compile_args=["-std=c++11", "-fopenmp", "-lpthread", "-lgomp",
        "-lm"]
 #       extra_compile_args=["-std=c++11","--expt-extended-lambda", "-Xcudafe","--diag_suppress=esa_on_defaulted_function_ignored"]
    )


extNames = scandir("sleep")
extensions = [makeExtension(name) for name in extNames]

setup(
    setup_requires=['setuptools>=18.0', 'wheel', 'Cython'],
    name="sleep",
    packages=["sleep"],
    ext_modules=cythonize(extensions),
    package_data={
        '':['*.pxd']
    },
    zip_safe=False,
    include_package_data=True,
    )



