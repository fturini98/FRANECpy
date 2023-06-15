import pandas as pd

def clear_tree(tree, target_name):
    cleared_tree = {}

    for key, values in tree.items():
        if key == target_name:
            for metall, masses in values.items():
                print(metall)
                if metall not in cleared_tree:
                    cleared_tree[metall] = {}
                metall_folder = cleared_tree[metall]
                for mass, df in masses.items():
                    metall_folder[mass] = df
        else:
            if isinstance(values, dict):
                subtree = clear_tree(values, target_name)
                cleared_tree.update(subtree)
    
    return cleared_tree
