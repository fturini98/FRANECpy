.. FRANECpy documentation master file, created by
   sphinx-quickstart on Mon Jun 12 15:09:30 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to FRANECpy's documentation!
====================================
This library is created to analyze the FRANEC program output.
The main goal of this library is creating an interactive whindow tho choose and import, in a tree format (managed via dictionary and dataframes), the data taken from the files.dat, provided by the FRANEC simulations, to analyze it.
These tree colud be saved and reloaded if you want to make the data analysis faster.

We tried to port the functions into the jupyter environment, even though the kernel crashes from time to time, the functions actually work.

Most uselful functions:
------------------------

:usere_interaction module:

- *itree_call()*:   
   When you call this function it creates an interactive window where you choose to import or create data trees. The function returns a data tree.

- *load_trees(list(files paths))*: 
   When you call this function it loads the trees that you have alredy saved from their files phats. It return a data tree whit all the trees that you have chosen.
   
- *jupyter_simple_browse(tree)*: 
   When you call the function it opens a window to browse the tree. It works also in jupyter enviroment.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   Modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
