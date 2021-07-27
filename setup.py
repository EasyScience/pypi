from setuptools import setup
import platform


try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
    # this overrides standard naming of the wheel to not include
    # architecture or python dot version number

    class Bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = False

        def get_tag(self):
            python, abi, plat = _bdist_wheel.get_tag(self)
#             if platform.system() != 'Windows':
#                 python, abi = 'py3', 'none'
            return python, abi, plat
except ImportError:
    Bdist_wheel = None

cmdclass = {}
if platform.system() != 'Linux':
    cmdclass={
        'bdist_wheel':     Bdist_wheel
    }
    
setup(
    name='GSASII',
    version='0.0.1',
    packages=['GSASII', 'GSASII.CifFile', 'GSASII.exports', 'GSASII.NIST_profile'],
    url='https://subversion.xray.aps.anl.gov/pyGSAS/',
    license='BSD3',
    author='simonward',
    author_email='',
    description='',
    include_package_data=True,
    package_data={
        'GSASII': ['*'],
    },
    cmdclass=cmdclass
)
