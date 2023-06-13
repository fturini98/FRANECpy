from IPython.display import clear_output
from tkinter import ttk
import threading
import time
#import pandasgui
from FRANECpy.build_tree import *
from FRANECpy.browse_and_choose_file_paths import *


#Section of the code for load or create the tree, on dependence what the user choose

def choose_open_or_create_tree():
    """
    Prompt the user to choose between loading existing trees or creating a new one.

    This function continuously prompts the user to choose between loading existing trees or creating a new one until a valid choice is made.

    Returns:
        str: The user's choice, either "create" or "load".
    """
    while True:
        user_input = input("\033[34mDo you want to load trees or create a new one? (create=c / load=l):\033[0m ")
        choice = user_input.lower()
        if choice in ["q", "quit"]:
            print("\033[31mProgram stopped.\033[0m")
            # Perform any necessary cleanup or additional actions before exiting
            sys.exit(0)
        elif choice in ["c", "create"]:
            return "create"
        elif choice in ["l", "load"]:
            return "load"
        else:
            print("\033[33mInvalid choice! Please try again.\033[0m")

def load_trees(tree_paths):
    """
    Load multiple trees from the specified file paths.

    This function loads multiple trees from the given file paths and stores them in a dictionary, where the keys are the tree names (derived from the file names) and the values are the loaded trees. It also includes a special "paths" branch in the dictionary, which contains all the tree paths.

    Args:
        tree_paths (list): A list of file paths to the tree files.

    Returns:
        dict: A dictionary containing the loaded trees and the tree paths.
    """
    trees = {}
    for tree_path in tree_paths:
        tree, tree_name = load_tree_from_path(tree_path)
        trees[tree_name] = tree

    # Create a branch for saving all the tree paths
    trees["paths"] = tree_paths

    return trees

def browse_load_trees(data_folder_paths):
    """
    Browse and load trees from the specified data folder paths.

    This function prompts the user to browse and select tree files from the specified data folder paths. It then loads the selected tree files using the `load_trees` function and returns the loaded trees.

    Args:
        data_folder_paths (list): A list of data folder paths to browse for tree files.

    Returns:
        dict: A dictionary containing the loaded trees and the tree paths.
    """
    tree_paths = jupyter_choose_tree_paths(data_folder_paths)
    trees = load_trees(tree_paths)

    return trees

def tree_call(standard_data_folder="C:/Users/fturi/Desktop/Dati"):
    """
    Perform the tree call operation based on user choice.

    This function performs the tree call operation based on the user's choice of creating a new tree or loading existing trees.
    It interacts with the user to select files and folders, generate trees, and save or load trees accordingly.

    Args:
        standard_data_folder (str): The standard data folder path. Default is "C:/Users/fturi/Desktop/Dati".

    Returns:
        dict or Tree: If a new tree is created, it returns the generated tree object.
                      If existing trees are loaded, it returns a dictionary containing the loaded trees.
    """
    # Get the main data folder path
    data_folder_path = get_main_data_folder_path(standard_data_folder)

    # Ask the user to choose between creating a new tree or loading existing trees
    user_choice = choose_open_or_create_tree()

    if user_choice == "create":
        # User chose to create a new tree
        file_paths, folder_paths = jupyter_choose_file_paths(data_folder_path)
        tree = generate_tree(file_paths, folder_paths)
        print("\033[32mTree created\033[0m")

        # Save the created tree
        save_tree_with_shell(tree, standard_data_folder)

        while True:
            user_input = input("\033[34mDo you want to use this tree or load others? (this=Enter/ others=o)\033[0m ")

            if not user_input:
                # User chose to use the created tree
                return tree
            elif user_input.lower() in ["n", "no"]:
                # User chose not to use any tree
                print("\033[31mProgram stopped!\033[0m")
                sys.exit(0)
            elif user_input.lower() in ["other", "others", "o"]:
                # User chose to load other trees
                trees = browse_load_trees(standard_data_folder)
                print("\033[32mTrees loaded\033[0m")
                return trees
            else:
                # Invalid choice
                print("\033[33mInvalid choice! Please try again.\033[0m")
    else:
        # User chose to load existing trees
        trees = browse_load_trees(standard_data_folder)
        print("\033[32mTrees loaded\033[0m")
        return trees

#Section of the code for show the tree structure and work on it

def simple_browse(tree,root=None):
    if root==None:
        root=tk.Tk()
    node_dataframes = {}
    def on_tree_select(event):
        item = treeview.focus()
        node_id = treeview.item(item, "text")
        if node_id in node_dataframes:
            df = node_dataframes[node_id]
            #pandasgui.show(df)

    def populate_treeview(parent, node):
        for key, value in node.items():
            item = treeview.insert(parent, "end", text=key)
            if isinstance(value, pd.DataFrame):
                node_id = treeview.item(item, "text")
                node_dataframes[node_id] = value
            elif isinstance(value, dict):
                populate_treeview(item, value)

    #calling root=tk.Tk() is need it for porting to the jupyter function
    root.title("Tree Browser")

    treeview = ttk.Treeview(root)
    treeview.pack(expand=True, fill="both")

    populate_treeview("", tree)

    treeview.bind("<<TreeviewSelect>>", on_tree_select)

    root.mainloop()

#Section for porting the program to the jupyter notebook

#Function whith gui and return

def jupyter_run_gui_function(tkinter_function, callback, *args, **kwargs):
    """
    Run a tkinter function in a separate thread within a Jupyter Notebook.

    Parameters:
        tkinter_function (callable): The tkinter function to run.
        
        callback (callable): The callback function to store the result.
        
        (*)args: Variable length argument list to be passed to the tkinter function.
        
        (**)kwargs: Arbitrary keyword arguments to be passed to the tkinter function.

    Returns:
        None
    """
    # Clear the current output in the Jupyter Notebook cell
    clear_output(wait=True)
    
    # Create a separate thread to run the tkinter function
    def thread_func():
        root = kwargs.get('root', tk.Tk())
        
        # This is needed if you call the interactive function multiple times
        root.protocol("WM_DELETE_WINDOW", root.destroy)  # Handle window close event
        result = tkinter_function(root=root, *args, **kwargs)
        root.mainloop()
        
        # Invoke the callback function with the result
        callback(result)
    
    # Create a separate thread to run the tkinter function
    thread = threading.Thread(target=thread_func)
    thread.start()

def jupyter_choose_file_paths(data_folder_path):
    """
    Choose file paths and folder paths using a file dialog within a Jupyter Notebook.

    Parameters:
        data_folder_path (str): The path to the data folder.

    Returns:
        tuple: A tuple containing the selected file paths and folder paths.
    """
    file_paths = []
    folder_paths = []
    result_holder = {'file_paths': file_paths, 'folder_paths': folder_paths}
    thread_event = threading.Event()

    def store_paths(selected_file_paths, selected_folder_paths):
        # Store the selected file paths and folder paths in the result_holder dictionary
        result_holder['file_paths'] = selected_file_paths
        result_holder['folder_paths'] = selected_folder_paths
        thread_event.set()  # Set the event to indicate that the thread has finished

    def choose_file_paths_wrapper(root=None):
        # Call the choose_file_paths function and store the result
        selected_file_paths, selected_folder_paths = choose_file_paths(data_folder_path, root=root)
        if not thread_event.is_set():  # Check if the event has been set (window closed)
            store_paths(selected_file_paths, selected_folder_paths)

    # Run the choose_file_paths_wrapper function in a separate thread
    thread = threading.Thread(target=choose_file_paths_wrapper)
    thread.start()

    # Wait for the thread to finish or the window to be closed
    while thread.is_alive() and not thread_event.is_set():
        time.sleep(0.1)

    # Check if the window was closed before the thread finished
    if not thread_event.is_set():
        thread.join()  # Ensure the thread is terminated
        # Because the window was running in a separate thread, the call to exit inside the choose_file_paths
        # function hasn't stopped the program, so you must call it again. You want to stop the program if the
        # file_paths and folder_paths are empty.
        if not result_holder['file_paths'] and not result_holder['folder_paths']:
            sys.exit(0)

    # Return the selected file paths and folder paths
    return result_holder['file_paths'], result_holder['folder_paths']

def jupyter_choose_tree_paths(data_folder_path):
    """
    Choose tree paths using a file dialog within a Jupyter Notebook.

    Parameters:
        data_folder_path (str): The path to the data folder.

    Returns:
        list: A list of selected tree paths.
    """
    tree_paths = []
    result_holder = {'tree_paths': tree_paths}
    thread_event = threading.Event()

    def store_paths(selected_tree_paths):
        # Store the selected tree paths in the result_holder dictionary
        result_holder['tree_paths'] = selected_tree_paths
        thread_event.set()  # Set the event to indicate that the thread has finished

    def choose_tree_paths_wrapper(root=None):
        # Call the browse_and_select_trees function and store the result
        selected_tree_paths = browse_and_select_trees(data_folder_path, root=root)
        if not thread_event.is_set():  # Check if the event has been set (window closed)
            store_paths(selected_tree_paths)

    # Run the choose_tree_paths_wrapper function in a separate thread
    thread = threading.Thread(target=choose_tree_paths_wrapper)
    thread.start()

    # Wait for the thread to finish or the window to be closed
    while thread.is_alive() and not thread_event.is_set():
        time.sleep(0.1)

    # Check if the window was closed before the thread finished
    if not thread_event.is_set():
        thread.join()  # Ensure the thread is terminated
        # Because the window was running in a separate thread, the call to exit inside the browse_and_select_trees
        # function hasn't stopped the program, so you must call it again. You want to stop the program if the tree_paths
        # is empty.
        if not result_holder['tree_paths']:
            sys.exit(0)

    # Return the selected tree paths
    return result_holder['tree_paths']


#Function whitout return
def jupyter_run_gui_function_whitout_return(tkinter_function, *args, **kwargs):
    """
    Run a tkinter function in a separate thread within a Jupyter Notebook.

    Parameters:
        tkinter_function (callable): The tkinter function to run.
        
        (*)args: Variable length argument list to be passed to the tkinter function.
        
        (**)kwargs: Arbitrary keyword arguments to be passed to the tkinter function.

    Returns:
        None
    """
    # Clear the current output in the Jupyter Notebook cell
    clear_output(wait=True)
    
    # Create a separate thread to run the tkinter function
    def thread_func():
        root = tk.Tk()
        
        #This is need it if you call the interactives function form multiple time, whitout this the kernell crash
        root.protocol("WM_DELETE_WINDOW", root.destroy)  # Handle window close event
        tkinter_function(root=root,*args, **kwargs)
        root.mainloop()
    
    # Create a separate thread to run the tkinter function
    thread = threading.Thread(target=thread_func)
    thread.start()

def jupyter_simple_browse(tree):
    jupyter_run_gui_function_whitout_return(simple_browse,tree)