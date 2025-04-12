from pprint import pprint

class GetNukeFileProperties():
    """
    A class to parse and extract properties from a Nuke script file (.nk).

    This class reads the Nuke script and extracts information about 'Write' nodes, 
    including their render directories, frame ranges, and node names.
    """
    
    def __init__(self , file_path):       
        # List to store properties of all Write nodes
        self.write_nodes_data  = []
        
        # Open and read the Nuke script file
        with open(file_path, 'r') as nuke_file:
            nuke_file_data = nuke_file.readlines()

        # Flag to check if currently parsing a Write node
        in_write_node = False
       
        # Parse each line in the Nuke script
        for line in nuke_file_data:
            stripped_line = line.strip()
        
            # Start of a Write node block
            if stripped_line.startswith("Write {"):
                in_write_node = True
                write_node_properties = {} # Dictionary to store the properties of the current Write node
                           
            if in_write_node:
                # Extract the render directory
                if stripped_line.startswith("file "):
                    write_node_properties["render_dir"] = stripped_line.split()[1]
                
                #Extract the first frame and create the frame range
                if stripped_line.startswith("first "):
                    write_node_properties["first frame"] = stripped_line.split()[1]
                
                #Extract the last frame and create the frame range
                if stripped_line.startswith("last "):
                    write_node_properties["last frame"] = stripped_line.split()[1]
                
                # Extract the write node name
                if stripped_line.startswith("name "):
                    write_node_properties["write_node_names"] = stripped_line.split()[1]
                
                # Extract if the write node is disable
                if stripped_line.startswith("disable "):
                    write_node_properties["disable"] = stripped_line.split()[1]

                 # End of the Write node block
                if stripped_line.startswith("}"):
                    self.write_nodes_data .append(write_node_properties) 
                    in_write_node = False

    # Function to retrieve all Write node names from the Nuke script
    def get_write_nodes_name(self):
        """
        Retrieve a list of all Write node names from the parsed Nuke script.

        Returns:
            list: A list of Write node names.
        """

        write_nodes_list = []

        for write_nodes in self.write_nodes_data :
            if not write_nodes.get("disable"):
                write_nodes_list.append(write_nodes.get("write_node_names"))
            
        return write_nodes_list

    # Function to retrieve the frame range for a specific Write node
    def get_frame_range(self, write_node_name=None):
        """
        Retrieve the frame range for a specified Write node.

        Args:
            node_name (str): The name of the Write node.

        Returns:
            list: A list containing the first and last frame numbers, or None if not found.
        """
        
        # Loop through each item in the 'write_nodes_data' list and  Check if the current write node matches the given 'write_node_name'
        for write_node in self.write_nodes_data :
            if write_node.get("write_node_names") == write_node_name:
                frame_range = f"{write_node.get('first frame' , 1)}-{write_node.get('last frame')}"  # Get the 'first and last frame' value from the dictionary; if first frame doesn't exist, default to 1
                return frame_range
                
    # Function to retrieve the render directory path for a specific Write node
    def get_file_path(self, write_node_name=None):
        """
        Retrieve the render directory path for a specified Write node.

        Args:
            node_name (str): The name of the Write node.

        Returns:
            str: The render directory path, or None if not found.
        """

        for file_path in self.write_nodes_data :
            if file_path.get("write_node_names") == write_node_name:
                return file_path.get("render_dir")

if __name__ == "__main__":
    file_properties =  GetNukeFileProperties(r"D:\GamutX\Render_Mate\Nuke_files\PRJ_102_013_v001 - Copy (13).nk")
    pprint(file_properties.get_file_path("mov"))