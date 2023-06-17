import pandas as pd
import matplotlib.pyplot as plt
import sys
import re

def clear_tree(tree, target_name):
    """
    Clears a tree dictionary by extracting a specific target_name and its associated data.
    Creating a new tree that has for the base root the "traget_name" branch of the parent tree.
    
    Works only if the structure is  Tree[...]...["RID"/"RAW"/"ISO"][metallicity][masses/ages dataframes]

    Args:    
        tree (dict):
            The input tree dictionary.
        
        target_name (str):    
            The target_name to extract from the tree.
        Could be only:
        
            "RID" for reduced traces.
            
            "ISO" for isochrones.
            
            "RAW" for raw data.
            
            
        

    Returns:    
        tree (dict):
            The cleared tree dictionary containing only the specified target_name and its associated data.
    """

    # Create an empty dictionary to store the cleared tree
    cleared_tree = {}

    # Iterate over the items in the input tree dictionary
    for key, values in tree.items():
        # Check if the current key matches the target_name
        if key == target_name:
            # Iterate over the metals and their corresponding masses in the values dictionary
            for metall, masses in values.items():
                # If the metall is not already present in the cleared_tree, add it as an empty dictionary
                if metall not in cleared_tree:
                    cleared_tree[metall] = {}
                # Get the current metall folder in the cleared_tree
                metall_folder = cleared_tree[metall]
                # Iterate over the masses and their associated dataframes
                for mass, df in masses.items():
                    # Add the mass and its corresponding dataframe to the metall_folder
                    metall_folder[mass] = df
        else:
            # If the "values" is a dictionary, recursively call the clear_tree function on it
            if isinstance(values, dict):
                subtree = clear_tree(values, target_name)
                # Update the cleared_tree with the cleared subtree
                cleared_tree.update(subtree)

    # Return the cleared_tree
    return cleared_tree

def HR_plot_equal_metall(tree, type, metal, mass_min=None, mass_max=None):
    """
    Plots the Hertzsprung Russell diagram for a specific metallicity.
    
    If the optional arguments are None the boundaries limits are ignored.

    Args:
        tree (dict): 
            The input tree dictionary.
        
        type (str):
            The type of data ('RID' or 'RAW').
        
        metal (str):
            The metallicity to plot.
        
        mass_min (float, optional):
            Minimum mass value to include in the plot. Defaults to None.
        
        mass_max (float, optional):
            Maximum mass value to include in the plot. Defaults to None.
    
    """

    # Check if the given metal exists in the tree
    if metal in tree:
        masses = tree[metal]
    else:
        # Print an error message and exit if the metal is not found in the tree
        print(f"No data for {metal}. Exiting!")
        sys.exit(0)

    # Iterate over the masses and their associated data frames
    for mass, df in masses.items():
        # Extract the mass value from the mass string using a regular expression
        match = re.search(r'M([\d.]+)', mass)
        mass = float(match.group(1))

        # Check if the mass is within the specified range (if any)
        if (mass_min is None or mass_min <= mass) and (mass_max is None or mass <= mass_max):
            if type == "RID":
                # Plotting logic for RID type
                plt.plot(df["LOG_TE_(K)"], df["LOG_L/Lo"], label=f"Mass {mass} ({metal})")
            elif type == "RAW":
                # Plotting logic for RAW type
                plt.plot(df["LOG TE"], df["LOG L"], label=f"Mass {mass} ({metal})")

    # Customize the plot based on the type of data
    if type == "RID":
        plt.xlabel("LOG TE (K)")
        plt.ylabel("LOG L/Lo")
    elif type == "RAW":
        plt.xlabel("LOG TE")
        plt.ylabel("LOG L")

    plt.title(f"Different masses for {metal}")
    #invert x axis for making the HR plot.
    plt.gca().invert_xaxis()
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.show()

def HR_plot_equal_mass(tree, type, mass, Z_min=None, Z_max=None, He_min=None, He_max=None, Verbose=False):
    """
    Plots the Hertzsprung Russell diagram for a specific mass.
    
    If the optional arguments are None the boundaries limits are ignored.
    
    Args:
        tree (dict):
            The input data tree dictionary.
            
        type (str): 
            The type of data ('RID' or 'RAW').
            
        mass (str or float):
            The mass to plot. If float, it is formatted as a string with two decimal places to match the data frame keys.
                
        Z_min (float, optional): 
            Minimum metallicity value to include in the plot. Defaults to None.
            
        Z_max (float, optional):
            Maximum metallicity value to include in the plot. Defaults to None.
            
        He_min (float, optional): 
            Minimum helium value to include in the plot. Defaults to None.
            
        He_max (float, optional):
            Maximum helium value to include in the plot. Defaults to None.
        
        Verbose (bool, optional):
            If True, print messages for excluded metallicities due to out-of-range values. Defaults to False.
    """

    # Format the mass string if it is provided as a float
    if not isinstance(mass, str):
        mass = "{:.2f}".format(mass)
        mass_value = mass
        mass = "M" + str(mass)

    # Iterate over the metals in the tree dictionary
    for metal in tree.keys():
        # Extract the Z (metallicity) and He (helium) values from the metal string using regular expressions
        match = re.search(r'Z([\d.]+)_He([\d.]+)', metal)
        Z = float(match.group(1))
        He = float(match.group(2))

        # Check if the metallicity or helium values are within the specified ranges (if any)
        if (Z_min is not None and Z < Z_min) or (Z_max is not None and Z_max < Z) or \
                (He_min is not None and He < He_min) or (He_max is not None and He_max < He):
            if Verbose:
                # Print a message for excluded metallicities due to out-of-range values if Verbose is True
                print(f"Helium or metallicity out of range. Excluding Z:{Z} and He:{He}")
        else:
            df = tree[metal][mass]

            if type == "RID":
                # Plotting logic for RID type
                plt.plot(df["LOG_TE_(K)"], df["LOG_L/Lo"], label=f"Composition ({metal})")
            elif type == "RAW":
                # Plotting logic for RAW type
                plt.plot(df["LOG TE"], df["LOG L"], label=f"Mass {mass} ({metal})")

    # Customize the plot based on the type of data
    if type == "RID":
        plt.xlabel("LOG TE (K)")
        plt.ylabel("LOG L/Lo")
    elif type == "RAW":
        plt.xlabel("LOG TE")
        plt.ylabel("LOG L")

    plt.title(f"Different metallicities for mass={mass_value} M_sun")
    plt.gca().invert_xaxis()
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.show()

def HR_plot_ISO(tree, metal, time_min=None, time_max=None):
    """
    Plots the Hertzsprung Russell diagram for isochrones in the time range for specific metallicity.
    
    If the optional arguments are None the boundaries limits are ignored.

    Args:
        tree (dict):
            The input data tree dictionary.
            
        metal (str): 
            The metallicity to plot.
            
        time_min (float, optional):
            Minimum time value to include in the plot. Defaults to None.
            
        time_max (float, optional): 
            Maximum time value to include in the plot. Defaults to None.
    """

    # Check if the given metal exists in the tree
    if metal in tree:
        times = tree[metal]
    else:
        # Print an error message and exit if the metal is not found in the tree
        print(f"No data for {metal}. Exiting!")
        sys.exit(0)

    # Iterate over the times and their associated dataframes
    for time, df in times.items():
        # Extract the time value from the time string using a regular expression
        match = re.search(r'AGE([\d.]+)', time)
        time = match.group(1)
        time = time[:2] + "." + time[2:]
        time = float(time)

        # Check if the time is within the specified range (if any)
        if (time_min is None or time_min <= time) and (time_max is None or time <= time_max):
            # Plotting logic here
            plt.plot(df["LOG_TE_(K)"], df["LOG_L/Lo"], label=f"At the age of {time} Gyr ({metal})")

    plt.xlabel("LOG TE (K)")
    plt.ylabel("LOG L/Lo")
    plt.title(f"Different ages for {metal}")
    plt.gca().invert_xaxis()
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.show()
    
def HR_plot(tree, type, equal="metallicity", mass_min=None, mass_max=None, Z_min=None, Z_max=None, He_min=None, He_max=None, time_min=None, time_max=None, Verbose=False):
    """
    Plots the Hertzsprung Russell diagram based on the specified parameters.
    
        If you select ISO the mass limits are ignored and you plot isochrones in the metallicity range
                
        If you select RAW or RID you could choose if plot the HR plots for equal metallicity or mass in the range(the age limits are ignored).
        If you have the conditions of equal mass and you have multiple masses, the program will create an HR plot for each mass, the same for metallicity.
    
    If the optional arguments are None the boundaries limits are ignored.
    
    **Note**: There is the Verbose args, if True, print messages for excluded metallicities due to out-of-range values.

    Args:
        tree (dict): 
            The input data tree dictionary.
            
        type (str): 
            The type of data ('RID', 'RAW', or 'ISO'):
            
                If you select ISO the mass limits are ignored and you plot isochrones in the metallicity range
                
                If you select RAW or RID you could choose if plot the HR plots for equal metallicity or mass in the range(the age limits are ignored).
                If you have the conditions of equal mass and you have multiple masses, the program will create an HR plot for each mass, the same for metallicity.
                
        equal (str, optional): 
            The type of equality ('metallicity' or 'mass'). Defaults to 'metallicity'.
            
        mass_min (float, optional): 
            Minimum mass value to include in the plot. Defaults to None.
            
        mass_max (float, optional): 
            Maximum mass value to include in the plot. Defaults to None.
            
        Z_min (float, optional): 
            Minimum metallicity value to include in the plot. Defaults to None.
            
        Z_max (float, optional): 
            Maximum metallicity value to include in the plot. Defaults to None.
            
        He_min (float, optional): 
            Minimum helium value to include in the plot. Defaults to None.
            
        He_max (float, optional): 
            Maximum helium value to include in the plot. Defaults to None.
            
        time_min (float, optional): 
            Minimum time value to include in the plot. Defaults to None.
            
        time_max (float, optional): 
            Maximum time value to include in the plot. Defaults to None.
            
        Verbose (bool, optional):
            If True, print messages for excluded metallicities due to out-of-range values. Defaults to False.
    """

    # Check if the tree dictionary needs to be cleared based on the type
    if not all(key.startswith("Z") for key in tree.keys()):
        if type == "RID":
            tree = clear_tree(tree, "RID")
        elif type == "RAW":
            tree = clear_tree(tree, "RAW")
        elif type == "ISO":
            tree = clear_tree(tree, "ISO")

    if type == "ISO":
        # Iterate over the metals in the tree dictionary for ISO type
        for metal in tree.keys():
            match = re.search(r'Z([\d.]+)_He([\d.]+)', metal)
            Z = float(match.group(1))
            He = float(match.group(2))

            if (Z_min is not None and Z < Z_min) or (Z_max is not None and Z_max < Z) or \
                    (He_min is not None and He < He_min) or (He_max is not None and He_max < He):
                if Verbose:
                    # Print a message for excluded metallicities due to out-of-range values if Verbose is True
                    print(f"Helium or metallicity out of range. Excluding Z:{Z} and He:{He}")
            else:
                HR_plot_ISO(tree, metal, time_min, time_max)

    elif equal in ["metall", "metal", "metallicity"] and type != "ISO":
        # Iterate over the metals in the tree dictionary for metallicity equality
        for metal in tree.keys():
            match = re.search(r'Z([\d.]+)_He([\d.]+)', metal)
            Z = float(match.group(1))
            He = float(match.group(2))

            if (Z_min is not None and Z < Z_min) or (Z_max is not None and Z_max < Z) or \
                    (He_min is not None and He < He_min) or (He_max is not None and He_max < He):
                if Verbose:
                    # Print a message for excluded metallicities due to out-of-range values if Verbose is True
                    print(f"Helium or metallicity out of range. Excluding Z:{Z} and He:{He}")
            else:
                HR_plot_equal_metall(tree, type, metal, mass_min, mass_max)

    elif equal in ["mass", "Mass"] and type != "ISO":
        mass_in_range = []

        # Extract all the mass in the range [mass_min, mass_max]
        for metal, masses in tree.items():
            for mass in masses:
                match = re.search(r'M([\d.]+)', mass)
                mass = float(match.group(1))
                if (mass_min is None or mass_min <= mass) and (mass_max is None or mass <= mass_max):
                    if mass not in mass_in_range:
                        mass_in_range.append(mass)

        # Make a plot for each mass in the range
        for mass in mass_in_range:
            HR_plot_equal_mass(tree, type, mass, Z_min, Z_max, He_min, He_max, Verbose)
                       