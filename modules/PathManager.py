#import modules
import os
import json

from PySide2.QtWidgets import QMessageBox

class PathManager:
    """
    A class to manage and update paths for Nuke and RV Player in a JSON file.

    This class allows setting and updating paths for Nuke and RV Player in a JSON file,
    ensuring that the file exists and contains default values if not already created.
    """

    def __init__(self):
        """
        Initializes the PathManager class and ensures that the directory and JSON file
        for storing paths exist. If the JSON file does not exist, it will be created
        with default empty values for 'Nuke Path' and 'RV Player Path'.
        """

        # Get the user's home directory, define the RenderMate directory, and specify the path to the JSON file
        home_dir = os.path.expanduser("~")
        render_mate_dir = os.path.join(home_dir, "RenderMate")
        self.json_file_path = os.path.join(render_mate_dir, "set_paths.json")

        # If the RenderMate directory doesn't exist, create it
        if not os.path.exists(render_mate_dir):
            os.makedirs(render_mate_dir)

        # If the JSON file doesn't exist, create it with default values
        if not os.path.exists(self.json_file_path):
            default_paths = {"Nuke Path": "", "RV Player Path": ""}
            with open(self.json_file_path, "w") as file:
                json.dump(default_paths, file, indent=4)


    # Define a private method at the class level to update a specified path in the JSON file
    def _update_paths(self, path_key, new_path_value):
        """
        Updates the specified path in the JSON file.

        Args:
            path_key (str): The key to update (either "Nuke Path" or "RV Player Path").
            new_path_value (str): The new value to set for the given path key.
        """
        # Check if the JSON file exists, open it in read-write mode, load current data, update it, and write it back with proper indentation
        if os.path.exists(self.json_file_path):
            with open(self.json_file_path, "r+") as file:
                current_data = json.load(file)
                current_data[path_key] = new_path_value
                file.seek(0)
                json.dump(current_data, file, indent=4)


    # Define a function to set the Nuke path in the JSON file
    def set_nuke_path(self, nuke_path):
        """
        Sets the Nuke executable path in the JSON file.

        Args:
            nuke_path (str): The path to the Nuke executable.
        """
        self._update_paths("Nuke Path", nuke_path)


    # Define a function to set the rv player path in the JSON file
    def set_rv_player_path(self, rv_player_path):
        """
        Sets the RV Player executable path in the JSON file.

        Args:
            rv_player_path (str): The path to the RV Player executable.
        """
        self._update_paths("RV Player Path", rv_player_path)



    def get_nuke_path(self):
        """
        Retrieves the Nuke executable path from the JSON configuration file.
        
        If the Nuke path is empty, it shows a warning message box indicating that no path is set.
        
        Returns:
            str: The Nuke executable path if found, or None if no path is set.
        """

        # Open the JSON file containing the configuration and load its contents
        with open(self.json_file_path, "r") as file:
            current_data = json.load(file)

            # Retrieve the Nuke Path from the configuration
            nuke_path = current_data.get("Nuke Path")

            # Create and configure the warning message box
            if nuke_path == '':
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setWindowTitle("No Nuke Path Found")
                msg_box.setText("The Nuke executable path is not set in the configuration.")
                msg_box.exec_()
            
            # If the Nuke path exists (is not empty), return it
            else:
                return nuke_path

            
if __name__ == "__main__":
    a = PathManager()
    a.get_nuke_path()
