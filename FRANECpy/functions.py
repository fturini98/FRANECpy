import pandas as pd
import matplotlib.pyplot as plt
import sys
import re

def clear_tree(tree, target_name):
    cleared_tree = {}

    for key, values in tree.items():
        if key == target_name:
            for metall, masses in values.items():
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

def HR_plot_equal_metall(tree,type,metal,mass_min=None,mass_max=None):
    if metal in tree:
        masses=tree[metal]
    else:
        print(f"No data for {metal}.Exit!")
        sys.exit(0)
    for mass, df in masses.items():
        match = re.search(r'M([\d.]+)', mass)
        mass=float(match.group(1))
        
        if (mass_min is None or mass_min<= mass) and (mass_max is None or mass<=mass_max):
            
            if type=="RID":
                # Plotting logic here
                plt.plot(df["LOG_TE_(K)"], df["LOG_L/Lo"], label=f"Mass {mass} ({metal})")
            elif type=="RAW":
                plt.plot(df["LOG TE"], df["LOG L"], label=f"Mass {mass} ({metal})")
                
    # Customize the plot
    if type=="RID":  
        plt.xlabel("LOG TE (K)")
        plt.ylabel("LOG L/Lo")
    elif type=="RAW":
        plt.xlabel("LOG TE")
        plt.ylabel("LOG L")
    
    plt.title(f"Different masses for {metal}")
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