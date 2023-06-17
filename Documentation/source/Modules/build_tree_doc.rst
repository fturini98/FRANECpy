build_tree.py
=============

Description
-----------

This module manages the folders and starting from the file paths builds the data tree.

**Attention:** 
   - The biggest folder that you can choose are *tools-driver-out* and *tools-isocrone-out*.

   - They **must be named like this**, or else they are excluded from the tree.

Useful functions
~~~~~~~~~~~~~~~~

The most useful function of this module are:

build_tree_from_paths
+++++++++++++++++++++
This function builds a hierarchical tree structure from a list of file paths.

save_tree_whit_shell
++++++++++++++++++++
This function permits saving the just created file in the *DataTrees* folder, passing as arguments the tree and the main data folder path.

If the *DataTrees* folder doesn't exist, it is automatically created when a tree is saved for the first time.

load_trees
++++++++++
This function permits to load multiple data trees that are already saved inside the *DataTrees* folder.

Functions
---------

.. automodule:: build_tree
   :members:
   :undoc-members:
