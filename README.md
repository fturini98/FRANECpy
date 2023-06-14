# FRANECpy

## Badges
[![Documentation Status](https://readthedocs.org/projects/franecpy/badge/?version=latest)](https://franecpy.readthedocs.io/en/latest/?badge=latest)

## Shell scripts to install and other usefull controls

**Install:** 
    
    pip install -e git+https://github.com/fturini98/FRANECpy.git@main#egg=FRANECpy

>The -e flags is to install in editable mode.

**Update to the most recent version:** 
    
    py -m pip install --upgrade  git+https://github.com/fturini98/FRANECpy.git@main#egg=FRANECpy

>The *py -m* is to run python controll in windows, if you use another system, use only pip command.

**Build documentation in local:** 

    py -m sphinx.cmd.build -b html source build

## Description

A simple library for help in the data analysis from FRANEC simulation.

## Most useful functions:

### user_interaction module:

In this module are present three main functions:

>*tree_call()*: 
>>When you call this function it creates an interactive window where you choose to import or create data trees. The function returns a data tree.

>*load_trees(list(files paths))*: 
>>When you call this function it loads the trees that you have alredy saved from their files phats. It return a data tree whit all the trees that you have chosen.

>*jupyter_simple_browse(tree)*: 
>>When you call the function it opens a window to browse the tree. It works also in jupyter enviroment.

