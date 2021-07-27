__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'

import os
import shutil
import subprocess
import sys
from distutils.command.install_data import install_data

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.install_lib import install_lib


class SconsExtension(Extension):
    """
    An extension to run the scons build
    This simply overrides the base extension class so that setuptools
    doesn't try to build your sources for you
    """

    def __init__(self, name, sources=[]):
        super().__init__(name=name, sources=sources)


class BuildSconsLibs(build_ext):

    def run(self):
        for extension in self.extensions:
            self.build_scons(extension)

    def build_scons(self, extension: Extension):
        print("Calling SCons to build the module")
        src_dir = os.path.join(self.build_lib, 'GSASII', 'fsource')
        scons_path = [os.environ.get('SCONS_PATH', 'scons')]
        scons_path = scons_path + scons_vars
        subprocess.check_call(scons_path, cwd=src_dir)
        bin_dir = os.path.join(self.build_lib, 'GSASII', 'bindist')
        os.makedirs(bin_dir, exist_ok=True)
        self.distribution.bin_dir = bin_dir


class InstallSconsLibsData(install_data):
    """
    Just a wrapper to get the install data into the egg-info
    Listing the installed files in the egg-info guarantees that
    all of the package files will be uninstalled when the user
    uninstalls your package through pip
    """

    def run(self):
        """
        Out files are the libraries that were built using cmake
        """
        self.outfiles = self.distribution.data_files


class InstallSconsLibs(install_lib):
    """
    Get the libraries from the parent distribution, use those as the outfiles
    Skip building anything; everything is already built, forward libraries to
    the installation step
    """

    def run(self):
        """
        Copy libraries from the bin directory and place them as appropriate
        """

        self.announce("Moving library files", level=3)
        # We have already built the libraries in the previous build_ext step
        self.skip_build = True
        # Move the lib to the correct location.
        bin_dir = os.path.join(self.build_dir, 'GSASII', 'bin')
        install_dir = os.path.join(self.build_dir, 'GSASII', 'bindist')
        for i in os.listdir(bin_dir):
            shutil.move(os.path.join(bin_dir, i), install_dir)
        # Must be forced to run after adding the libs to data_files
        self.distribution.run_command("install_data")
        super().run()


scons_vars = []
if "--scons_args" in sys.argv:
    idx = sys.argv.index("--scons_args")
    sys.argv.remove("--scons_args")
    for opt_idx in range(idx, len(sys.argv)):
        arg = sys.argv[opt_idx]
        scons_vars.append(arg)
    sys.argv = sys.argv[0:idx]

setup(
    name='GSASII',
    version='0.0.1',
    packages=['GSASII', 'GSASII.CifFile', 'GSASII.exports', 'GSASII.NIST_profile'],
    url='https://subversion.xray.aps.anl.gov/pyGSAS/',
    ext_modules=[SconsExtension(name='GSASII')],
    license='BSD3',
    author='simonward',
    author_email='',
    description='',
    include_package_data=True,
    package_data={
        'GSASII': ['*'],
    },
    cmdclass={
        'build_ext':    BuildSconsLibs,
        'install_data': InstallSconsLibsData,
        'install_lib':  InstallSconsLibs,

    },
    setup_requires=['setuptools', 'wheel', 'scons', 'numpy'],
    install_requires=['numpy'],

)
