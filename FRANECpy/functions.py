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
    
        tree (dict): The input tree dictionary.
        
        target_name (str): The target_name to extract from the tree.
        Could be only:
        
            "RID" for reduced traces.
            
            "ISO" for isochrones.
            
            "RAW" for raw data.
            
            
        

    Returns:
    
        dict: The cleared tree dictionary containing only the specified target_name and its associated data.
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
    Plots the Hertzsprung Russell diagram for a specific metal from the given tree dictionary.
    
    If the optional arguments are None the boundaries limits are ignored.

    Args:
    
        tree (dict): The input tree dictionary.
        
        type (str): The type of data ('RID' or 'RAW').
        
        metal (str): The metal to plot.
        
        mass_min (float, optional): Minimum mass value to include in the plot. Defaults to None.
        
        mass_max (float, optional): Maximum mass value to include in the plot. Defaults to None.
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

def HR_plot_equal_mass(tree,type,mass,Z_min=None,Z_max=None,He_min=None,He_max=None,Verbose=False):
    if not isinstance(mass,str):
        mass="{:.2f}".format(mass)
        mass_value=mass
        mass="M"+str(mass)
        
    for metal in tree.keys():
        match=re.search(r'Z([\d.]+)_He([\d.]+)',metal)
        Z=float(match.group(1))
        He=float(match.group(2))
        if (Z_min!=None and Z<Z_min) or (Z_max!=None and Z_max<Z) or (He_min!=None and He<He_min) or (He_max!=None and He_max<He):
            if Verbose==True:
                print(f"Helium or metallicity out of range. Excluding Z:{Z} and He:{He}") 
        else:
            df=tree[metal][mass]
            
            if type=="RID":
                plt.plot(df["LOG_TE_(K)"], df["LOG_L/Lo"], label=f"Composition ({metal})")
            elif type=="RAW":
                plt.plot(df["LOG TE"], df["LOG L"], label=f"Mass {mass} ({metal})")
    
    # Customize the plot
    if type=="RID":  
        plt.xlabel("LOG TE (K)")
        plt.ylabel("LOG L/Lo")
    elif type=="RAW":
        plt.xlabel("LOG TE")
        plt.ylabel("LOG L")

    plt.title(f"Different metalicities for mass={mass_value} M_sun")
    plt.gca().invert_xaxis()
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.show()

def HR_plot_ISO(tree,metal,time_min=None,time_max=None):
    if metal in tree:
        times=tree[metal]
    else:
        print(f"No data for {metal}.Exit!")
        sys.exit(0)
    for time, df in times.items():
        match = re.search(r'AGE([\d.]+)', time) 
        time=match.group(1)
        time=time[:2]+"."+time[2:]
        time=float(time)
        
        if (time_min is None or time_min<= time) and (time_max is None or time<=time_max):
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
    
def HR_plot(tree,type,equal="metallicity",mass_min=None,mass_max=None,Z_min=None,Z_max=None,He_min=None,He_max=None,time_min=None,time_max=None,Verbose=False):
    if not all(key.startswith("Z") for key in tree.keys()):
        if type=="RID":
            tree=clear_tree(tree,"RID")
        elif type=="RAW":
            tree=clear_tree(tree,"RAW")
            #ui.simple_browse()
        elif type=="ISO":
            tree=clear_tree(tree,"ISO")
        
    if type=="ISO":
        for metal in tree.keys():
            match=re.search(r'Z([\d.]+)_He([\d.]+)',metal)
            Z=float(match.group(1))
            He=float(match.group(2))
                
            if (Z_min!=None and Z<Z_min) or (Z_max!=None and Z_max<Z) or (He_min!=None and He<He_min) or (He_max!=None and He_max<He):
                if Verbose==True:
                    print(f"Helium or metallicity out of range. Excluding Z:{Z} and He:{He}") 
            else:            
                HR_plot_ISO(tree,metal,time_min,time_max)
        
    elif equal in ["metall","metal","metallicity"] and type!="ISO":    
        for metal in tree.keys():
            match=re.search(r'Z([\d.]+)_He([\d.]+)',metal)
            Z=float(match.group(1))
            He=float(match.group(2))
                
            if (Z_min!=None and Z<Z_min) or (Z_max!=None and Z_max<Z) or (He_min!=None and He<He_min) or (He_max!=None and He_max<He):
                if Verbose==True:
                    print(f"Helium or metallicity out of range. Excluding Z:{Z} and He:{He}") 
            else:            
                HR_plot_equal_metall(tree,type,metal,mass_min,mass_max)
                
    elif equal in ["mass", "Mass"] and type!="ISO":
        mass_in_range=[]
        #extract all the mass in range [mass_min, mass_max]
        for metal,masses in tree.items():
            for mass in masses:
                match = re.search(r'M([\d.]+)', mass)
                mass=float(match.group(1))
                if (mass_min is None or mass_min<= mass) and (mass_max is None or mass<=mass_max):
                    if mass not in mass_in_range:
                        mass_in_range.append(mass)
        
        #make a plot for each mass in range.        
        for mass in mass_in_range:
            HR_plot_equal_mass(tree,type,mass,Z_min,Z_max,He_min,He_max,Verbose)