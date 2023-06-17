# FRANECpy

## Badges
[![Documentation Status](https://readthedocs.org/projects/franecpy/badge/?version=latest)](https://franecpy.readthedocs.io/en/latest/?badge=latest)

## Shell scripts

**Install:** 
    
    pip install -e git+https://github.com/fturini98/FRANECpy.git@main#egg=FRANECpy

>The -e flags is to install in editable mode.

**Update to the most recent version:** 
    
    py -m pip install --upgrade  git+https://github.com/fturini98/FRANECpy.git@main#egg=FRANECpy

>The *py -m* is to run python controll in windows, if you use another system, use only pip command.

**Build documentation locally:** 

    py -m sphinx.cmd.build -b html source build

## Description

A simple library for help in the data analysis of FRANEC simulations.

## Most useful functions:

### usere_interface module

   - *tree_call()*:   
        
        When you call this function it creates an interactive window where you choose to import or create data trees. The function returns a data tree.
   
   - *jupyter_simple_browse(tree(dict))*: 
        
        When you call the function it opens a window to browse the tree. It works also in jupyter environment.

### build_tree module

   - *load_trees(list(files paths))*: 
        
        When you call this function it loads the trees that you have already saved from their files phats. It returns a data tree whit all the trees that you have chosen.

### functions module

   - *clear_tree(tree(dict), target_name(str))*:
        
        When you call this function it clears a tree dictionary by extracting a specific target_name and its associated data.

   - *HR_plot(tree(dict), type(_str))_*: 
        
        Plots the Hertzsprung Russell diagrams based on the specified parameters.

