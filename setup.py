from setuptools import setup

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
)
