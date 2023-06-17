functions.py
============

Description
-----------

This module adds some useful functions for analyzing the data tree.

Useful functions
~~~~~~~~~~~~~~~~
The most useful function in this module is:

HR_plot()
+++++++++
This function summarizes all the other functions for generating **Hertzsprung-Russell diagrams**.
It could generate diagrams for equal masses or equal metallicities and also generate isochrones in the metallicities range.
You could choose the *mass*,*metallicity* and *helium* range where plot the HR diagrams.

**Attention**: This is the only HR function that could take as data tree input a tree that isn't cleared before if you use the other HR
functions you must clear the tree before whit the **clear_tree** function. 

Functions
----------

.. automodule:: functions
   :members:
   :undoc-members: