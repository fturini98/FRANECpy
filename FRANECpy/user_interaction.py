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

def complex_browse(tree,root=None):
    if root==None:
        root=tk.Tk()
    node_dataframes = {}
    
    #local variables for data analysis
    dataframes_for_analysis={}
    
    #define the fucntion for the buttons
    press_duration=500 #ms
    def on_right_button_press(event):
        root.after(press_duration,lambda: open_context_menu(event))
    
    def on_right_button_relese(event):
        root.after_cancel(open_context_menu)
        
    def on_right_button_motion(event):
        item = treeview.identify_row(event.y)
        if item:
            treeview.selection_add(item)  # Add the item under the mouse to the selection

    def on_left_button_press(event):
        # Clear any previous selections
        treeview.selection_set()

        # Set the starting item for selection
        global start_item
        start_item = treeview.identify_row(event.y)
    
    def on_left_button_motion(event):
        # Get the current item under the mouse cursor
        current_item = treeview.identify_row(event.y)

        # Select all items between start_item and current_item
        items = treeview.tag_has("selected")
        if start_item and current_item:
            items_between = treeview.tag_has(treeview.index(start_item), treeview.index(current_item))
            items = items_between if items else items_between - items

        treeview.selection_set(items)
    
    def on_left_button_release(event):
        # Reset the starting item
        global start_item
        start_item = None
        
    def add_item():
        global type_of_file_selected
        selected_items=treeview.selection()
        for item in selected_items:
            node_id = treeview.item(item, "text")
            parent_item = treeview.parent(item)
            parent_key = treeview.item(parent_item, "text")

            if node_id in node_dataframes and not dataframes_for_analysis:
                df = node_dataframes[node_id]
            
                grand_parent_item=treeview.parent(parent_item)
                grand_parent_key=treeview.item(grand_parent_item, "text")
            
                type_of_file_selected=grand_parent_key
            
                if parent_key not in dataframes_for_analysis:
                    dataframes_for_analysis[parent_key] = {}
        
                dataframes_for_analysis[parent_key][node_id] = df
        
            elif node_id in node_dataframes:
                df = node_dataframes[node_id]
        
                if parent_key not in dataframes_for_analysis:
                    dataframes_for_analysis[parent_key] = {}
        
                dataframes_for_analysis[parent_key][node_id] = df
        
            elif not dataframes_for_analysis and parent_key=="RID" :
                type_of_file_selected="RID"
                print("Ciao")
            elif parent_key=="RID" and type_of_file_selected=="RID":
                print("weee")

        update_list()
    
    
    
    def populate_treeview(parent, node):
        for key, value in node.items():
            item = treeview.insert(parent, "end", text=key)
            if isinstance(value, pd.DataFrame):
                node_id = treeview.item(item, "text")
                node_dataframes[node_id] = value
            elif isinstance(value, dict):
                populate_treeview(item, value)

    def update_list():
        listbox.delete(0, tk.END)
        for parent_key, node_dataframes in dataframes_for_analysis.items():
            for node_id, dataframe in node_dataframes.items():
                listbox.insert(tk.END, f"Parent: {parent_key} | Node: {node_id} | Shape: {dataframe.shape}")


    #calling root=tk.Tk() is need it for porting to the jupyter function
    root.title("Tree Browser")

    treeview = ttk.Treeview(root)
    treeview.pack(expand=True, fill="both")

    populate_treeview("", tree)

    
    # Create the menu
    def open_context_menu(event):
        item = treeview.identify_row(event.y)
        context_menu = tk.Menu(root, tearoff=0)
        if item:
            treeview.selection_set(item)
            context_menu.add_command(label="Add item",command=add_item)
            context_menu.add_separator()
            context_menu.add_command(label="Do Nothing")
            context_menu.tk_popup(event.x_root, event.y_root)
    
    
    # Bind the right button press event
    treeview.bind("<ButtonPress-3>", on_right_button_press)
    treeview.bind("<ButtonRelease-3>", on_right_button_relese)
    
    # Bind the left button events
    treeview.bind("<ButtonPress-1>", on_left_button_press)
    treeview.bind("<B1-Motion>", on_left_button_motion)
    treeview.bind("<ButtonRelease-1>", on_left_button_release)
    
    
    #Listbox
    frame = tk.Frame(root)
    frame.pack(fill="both")

    listbox = tk.Listbox(frame)
    listbox.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    #listbox.bind("<<ListboxSelect>>", on_listbox_select)

    update_list()

    root.mainloop()

#Section for porting the program to the jupyter notebook

#Function whith gui and return

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
 
def jupyter_simple_browse(tree):
    """
    Launches a separate thread to run the 'simple_browse' function and provides a mechanism
    to stop the thread when needed.

    Args:
        tree: The tree parameter to pass to the 'simple_browse' function.

    Returns:
        None
    """

    # Create a stop event object
    stop_event = threading.Event()

    # Start the separate thread
    thread = threading.Thread(target=simple_browse(tree))
    thread.start()

    # Wait for the thread to finish or the stop event to be set
    while thread.is_alive() and not stop_event.is_set():
        time.sleep(0.1)

    # Check if the thread was stopped by the stop event
    if stop_event.is_set():
        # Join the thread to wait for its completion
        thread.join()
 
def jupyter_complex_browse(tree):
    """
    Launches a separate thread to run the 'complex_browse' function and provides a mechanism
    to stop the thread when needed.

    Args:
        tree: The tree parameter to pass to the 'simple_browse' function.

    Returns:
        None
    """

    # Create a stop event object
    stop_event = threading.Event()

    # Start the separate thread
    thread = threading.Thread(target=complex_browse(tree))
    thread.start()

    # Wait for the thread to finish or the stop event to be set
    while thread.is_alive() and not stop_event.is_set():
        time.sleep(0.1)

    # Check if the thread was stopped by the stop event
    if stop_event.is_set():
        # Join the thread to wait for its completion
        thread.join()
        