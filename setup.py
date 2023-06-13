from setuptools import setup, find_packages

setup(
    name='FRANECpy',
    __version__ = 'dev',
    author='Francesco Turini',
    author_email='fturini.turini7@gmail.com',
    description='A simple library for help in the data analysis from FRANEC simulation.',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'ipython',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)