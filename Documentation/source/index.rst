.. FRANECpy documentation master file, created by
   sphinx-quickstart on Mon Jun 12 15:09:30 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to FRANECpy's documentation!
====================================
This library is created to analyze the FRANEC program output.
The main goal of this library is to create an interactive window to choose and import, in a tree format (managed via dictionary and data frames), the data taken from the files.dat, provided by the FRANEC simulations, to analyze it.
These trees could be saved and reloaded if you want to make the data analysis faster.

The functions are also ported into the jupyter environment.

Most useful functions:
------------------------

usere_interface module
~~~~~~~~~~~~~~~~~~~~~~~
   - *tree_call()*:   
         When you call this function it creates an interactive window where you choose to import or create data trees. The function returns a data tree.
   
   - *jupyter_simple_browse(tree(dict))*: 
         When you call the function it opens a window to browse the tree. It works also in jupyter environment.

build_tree module
~~~~~~~~~~~~~~~~~
   - *load_trees(list(files paths))*: 
         When you call this function it loads the trees that you have already saved from their files phats. It returns a data tree whit all the trees that you have chosen.

functions module
~~~~~~~~~~~~~~~~
   - *clear_tree(tree(dict), target_name(str))*:
         When you call this function it clears a tree dictionary by extracting a specific target_name and its associated data.

   - *HR_plot(tree(dict), type(str))* :
         Plots the Hertzsprung Russell diagrams based on the specified parameters.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   Modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
