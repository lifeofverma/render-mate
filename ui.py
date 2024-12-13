# Import modules
import sys
from getpass import getuser
import os
from pathlib import Path 
import subprocess

# Importing third party modules
from PySide2.QtWidgets import QApplication, QComboBox, QSpacerItem,QSizePolicy, QMainWindow, QProgressBar, QMenuBar, QWidget, QPushButton, QVBoxLayout,  QHBoxLayout, QLabel, QTableWidget, QFileDialog, QTableWidgetItem, QHeaderView
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtCore import Qt , QSize

# Importing custom modules
from constants.constants import NUKE_ICON, USER_ICON, ADD_ICON, REMOVE_ICON, REMOVE_SELECTED_ICON, PLAY_ICON, STOP_ICON, OPERATION_PLAY_ICON, OPERATION_STOP_ICON, OPEN_DIR_ICON, RV_ICON




from pprint import pprint



class RenderMate(QMainWindow):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("RenderMate V1.0.0")
        self.setMinimumSize(1600, 800)
        self.menu_bar = QMenuBar()        
        self.set_path = self.menu_bar.addMenu("Set Path")
        self.setMenuBar(self.menu_bar)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)



        # header widget starts from here
        self.header = QWidget()
        # self.header.setStyleSheet("background-color: #1d1d1d;")
        # self.header.setFixedSize(1000,100)
        self.nuke_icon_label = QLabel()
        self.user_icon_label = QLabel()
        self.user_name = QLabel(getuser())
        self.tool_name = QLabel("RenderMate")
        self.nuke_icon_label.setPixmap(QPixmap(NUKE_ICON).scaled(64, 64 , Qt.KeepAspectRatio,  Qt.SmoothTransformation ))
        self.user_icon_label.setPixmap(QPixmap(USER_ICON).scaled(64,64 , Qt.KeepAspectRatio , Qt.SmoothTransformation))

        self.header_layout = QHBoxLayout()
        self.header_layout.addWidget(self.nuke_icon_label)
        self.header_layout.addWidget(self.user_icon_label)
        self.header_layout.addWidget(self.tool_name)
        self.header_layout.addWidget(self.user_name)
        self.header.setLayout(self.header_layout)


        #############################################################################################################################################

        # Sidebar widget setup
        self.side_bar_widget = QWidget()
        self.side_bar_widget.setFixedWidth(105)
        # self.side_bar.setStyleSheet("background-color: #323232;")
        
        # Create buttons
        self.add_button = QPushButton()
        self.add_button.setFlat(True)
        self.remove_selected = QPushButton()
        self.remove_all = QPushButton()
        self.start_all = QPushButton()
        self.stop_all = QPushButton()



        self.add_button.clicked.connect(self.add_files_to_table)
        self.remove_all.clicked.connect(self.clear_table)
        self.remove_selected.clicked.connect(self.remove_selected_rows)

        # set buttons icons
        self.add_button.setIcon(QIcon(ADD_ICON))
        self.start_all.setIcon(QIcon(PLAY_ICON))
        self.stop_all.setIcon(QIcon(STOP_ICON))
        self.remove_all.setIcon(QIcon(REMOVE_ICON))
        self.remove_selected.setIcon(QIcon(REMOVE_SELECTED_ICON))



        self.add_button.setIconSize(QSize(40, 40)) 
        self.remove_selected.setIconSize(QSize(40, 40)) 
        self.remove_all.setIconSize(QSize(60, 40)) 
        self.start_all.setIconSize(QSize(40, 40)) 
        # self.stop_all.setStyleSheet("QPushButton { border: none; }") 
        self.stop_all.setIconSize(QSize(40, 40)) 
        


        # Create labels for buttons
        self.add_label = QLabel("Add")
        self.add_label.setFixedHeight(40)
        self.remove_all_label = QLabel("Remove all")
        self.remove_selected_label = QLabel("Remove Selected")
        self.start_all_label = QLabel("Start all")
        self.stop_all_label = QLabel("Stop all")
        
        self.add_label.setFixedHeight(20)
        self.remove_selected_label.setFixedHeight(30)
        self.remove_all_label.setFixedHeight(10)
        self.start_all_label.setFixedHeight(20)
        self.stop_all_label.setFixedHeight(20)

        
        self.add_label.setAlignment(Qt.AlignCenter)
        self.remove_selected_label.setAlignment(Qt.AlignCenter)
        self.remove_all_label.setAlignment(Qt.AlignCenter)
        self.start_all_label.setAlignment(Qt.AlignCenter)
        self.stop_all_label.setAlignment(Qt.AlignCenter)




        # Create individual layouts for each button and label pair
        self.add_layout = QVBoxLayout()
        self.add_layout.setSpacing(0)
        self.add_layout.addWidget(self.add_button)
        self.add_layout.addWidget(self.add_label)

        self.remove_all_layout = QVBoxLayout()
        self.remove_all_layout.setSpacing(0)
        self.remove_all_layout.addWidget(self.remove_all)
        self.remove_all_layout.addWidget(self.remove_all_label)

        self.remove_selected_layout = QVBoxLayout()
        self.remove_selected_layout.setSpacing(0)
        self.remove_selected_layout.addWidget(self.remove_selected)
        self.remove_selected_layout.addWidget(self.remove_selected_label)

        self.start_all_layout = QVBoxLayout()
        self.start_all_layout.setSpacing(0)
        self.start_all_layout.addWidget(self.start_all)
        self.start_all_layout.addWidget(self.start_all_label)
        

        self.stop_all_layout = QVBoxLayout()
        self.stop_all_layout.setSpacing(0)
        self.stop_all_layout.addWidget(self.stop_all)
        self.stop_all_layout.addWidget(self.stop_all_label)

        # Create the main layout and add each button layout
        self.side_bar_main_layout = QVBoxLayout()
        self.side_bar_main_layout.addLayout(self.add_layout)
        self.side_bar_main_layout.addLayout(self.remove_all_layout)
        self.side_bar_main_layout.addLayout(self.remove_selected_layout)
        self.side_bar_main_layout.addLayout(self.start_all_layout)
        self.side_bar_main_layout.addLayout(self.stop_all_layout)
        
        # Create a spacer item with a fixed height
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Add the spacer before the sidebar widget in the layout
        self.side_bar_main_layout.addItem(spacer)
        # set Layout for sidebar buttons
        self.side_bar_widget.setLayout(self.side_bar_main_layout)



        #############################################################################################################################################


        # Property widget (table) setup
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels(["File Path", "File Name" , "Writes" , "Progress" , "Status" , "Operations" , "Launchers"]) 
        
        # Set header behavior for property widget
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        
        # Table and sidebar layout setup
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.side_bar_widget)
        self.hbox_layout.addWidget(self.table_widget)

        # Main layout setup
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.header)
        main_layout.addLayout(self.hbox_layout)
        self.central_widget.setLayout(main_layout) 




    #############################################################################################################################################
    
    
    def create_operation_row_widget(self):
            """
            Creates a QWidget containing multiple buttons for operations in the table rows.
            
            Returns:
                operation_row_widget (QWidget): A widget containing operation buttons.
            """
            self.operation_row_widget = QWidget()

            self.start_button = QPushButton("")
            self.start_button.setIcon(QIcon(OPERATION_PLAY_ICON))
            self.start_button.setIconSize(QSize(40, 40)) 
            self.start_button.setMinimumHeight(40)

            self.stop_button = QPushButton("")
            self.stop_button.setIcon(QIcon(OPERATION_STOP_ICON))
            self.stop_button.setIconSize(QSize(40, 40)) 
            self.stop_button.setMinimumHeight(40)

            # Create horizontal layout for buttons
            self.button_layout = QHBoxLayout()
            self.button_layout.addWidget(self.start_button)
            self.button_layout.addWidget(self.stop_button)

            # Set layout to the widget
            self.operation_row_widget.setLayout(self.button_layout)

            return self.operation_row_widget





    def create_launcher_row_widget(self):
            """
            Creates a QWidget containing multiple buttons for launcher in the table rows.
            
            Returns:
                create_launcher_row_widget (QWidget): A widget containing operation buttons.
            """
            self.launcher_row_widget = QWidget()

            # Initialize buttons
            self.rv_button = QPushButton("")
            self.rv_button.setIcon(QIcon(RV_ICON))
            self.rv_button.setIconSize(QSize(40, 40)) 
            self.rv_button.setFlat(True)
            self.rv_button.setMinimumHeight(40)

            self.nuke_button = QPushButton("")
            self.nuke_button.setIcon(QIcon(NUKE_ICON))
            self.nuke_button.setFlat(True)
            self.nuke_button.setIconSize(QSize(40, 40)) 
            self.nuke_button.clicked.connect(self.open_nuke_file)
            self.nuke_button.setMinimumHeight(40)

            self.open_render_dir_button = QPushButton("")
            self.open_render_dir_button.setFlat(True)
            self.open_render_dir_button.setIcon(QIcon(OPEN_DIR_ICON))
            self.open_render_dir_button.setIconSize(QSize(40, 40)) 
            self.open_render_dir_button.setMinimumHeight(40)

            # Create horizontal layout for buttons
            self.button_layout = QHBoxLayout()
            self.button_layout.addWidget(self.rv_button)
            self.button_layout.addWidget(self.nuke_button)
            self.button_layout.addWidget(self.open_render_dir_button)

            # Set layout to the widget
            self.launcher_row_widget.setLayout(self.button_layout)

            return self.launcher_row_widget






    def get_list_of_write_nodes_name(self , file_path):
        """
        This function reads a Nuke script file (.nk) and extracts the names of all write nodes 
        defined within the script. 

        Parameters:
        file_path (str): The path to the Nuke script file.

        Returns:
        list: A list of names of all write nodes found in the file.
        """
        write_node_names = []  # List to store names of all Write nodes

        # Open the Nuke script file for reading
        with open(file_path, 'r') as nuke_file:
            nuke_file_data = nuke_file.readlines()

            in_write_node = False  # Flag to track if we're inside a Write node
            current_write_node_lines = []  # List to store lines of the current Write node

            # Iterate through each line in the file
            for line in nuke_file_data:
                stripped_line = line.strip()

                # Check for the beginning of a Write node and if We are inside a Write node
                if stripped_line.startswith("Write {"):
                    in_write_node = True

                if in_write_node:
                    current_write_node_lines.append(stripped_line) 

                # When we reach the closing brace of a Write node, process it, Extract the name after 'name' Add the name to the list
                if stripped_line == "}":
                    for line_in_node in current_write_node_lines:
                        if line_in_node.startswith("name "):
                            write_node_name = line_in_node.split()[1]
                            write_node_names.append(write_node_name)
                            break

                    # Reset for the next Write node
                    in_write_node = False
                    current_write_node_lines = []

        # Return the list of Write node names
        return write_node_names

































    def add_files_to_table(self):
        """
        Opens a file dialog to select Nuke files, 
        extracts file paths and names, 
        and populates them in the table widget.
        """

        # Open file dialog to select Nuke files
        self.selected_files = list(QFileDialog.getOpenFileNames(
            None, 
            "Select Nuke Files", 
            r"D:\GamutX\Render_Mate\Nuke_files", 
            "Nuke Files (*.nk)"
        )[0])

        # Separate file paths and names
        file_paths = []
        file_names = []

        for file in self.selected_files:
            file_paths.append(os.path.dirname(file))
            file_names.append(os.path.basename(file))

        # Set the number of rows in the table to match the number of selected files
        self.table_widget.setRowCount(len(file_paths))

        # Populate the table widget with file paths, names, and operation widgets
        for row in range(len(file_paths)):
            file_path_item = QTableWidgetItem(file_paths[row])
            file_name_item = QTableWidgetItem(file_names[row])

            # Align text to the center
            file_path_item.setTextAlignment(Qt.AlignCenter)
            file_name_item.setTextAlignment(Qt.AlignCenter)

            # Set items and widgets in the respective columns
            self.table_widget.setItem(row, 0, file_path_item)
            self.table_widget.setItem(row, 1, file_name_item)
            self.table_widget.setCellWidget(row, 5, self.create_operation_row_widget())
            self.table_widget.setCellWidget(row, 6, self.create_launcher_row_widget())
            progress_bar = QProgressBar()
            progress_bar.setValue(50)  # Set an initial value, you can modify it as needed
            self.table_widget.setCellWidget(row, 3, progress_bar)


        # Set write nodes name in the respective columns
        for row, nuke_file in enumerate(self.selected_files):
            # Create a widget to display write nodes or a message and Fetch the list of write nodes from the Nuke file
            write_nodes_widget = QComboBox()
            write_node_names = self.get_list_of_write_nodes_name(nuke_file)

            # Populate the combo box with the write nodes OR Set a QLabel with "No write nodes found" message
            if write_node_names:
                write_nodes_widget.addItems(write_node_names)
                self.table_widget.setCellWidget(row, 2, write_nodes_widget)
            
            else:
                no_nodes_label = QLabel("No write nodes found")
                no_nodes_label.setAlignment(Qt.AlignCenter)
                self.table_widget.setCellWidget(row, 2, no_nodes_label)

            

    ######################################################################################
    
    
    def clear_table(self):
        """
        Removes all rows from the table widget.
        """
        self.table_widget.setRowCount(0)










    ######################################################################################
    def remove_selected_rows(self):
        """
        Removes only the selected rows from the table widget.
        """
        # Get selected rows
        selected_rows = self.table_widget.selectionModel().selectedRows()

        # Remove rows in descending order to maintain row integrity
        for row in sorted(selected_rows, reverse=True):
            self.table_widget.removeRow(row.row())







    ######################################################################################
    def open_nuke_file(self):
        """
        Opens the selected Nuke file using the Nuke software.

        This function determines which row in the table the 'Open in Nuke' button
        was clicked, retrieves the file path and name, and launches Nuke with 
        the selected script.
        """

        # Get the row of the clicked button within the table
        selected_row  = self.table_widget.indexAt(self.sender().parent().pos()).row()

        # Retrieve the file path and file name from the respective table columns
        file_path = self.table_widget.item(selected_row  , 0)
        file_name = self.table_widget.item(selected_row , 1)

        # Combine file path and file name to get the full path of the Nuke file
        nuke_file_path  = Path(Path(file_path.text()) / file_name.text()).as_posix()

        # Define the path to the Nuke executable and the required arguments
        nuke_executable_path  = r"C:\Program Files\Nuke13.2v5\Nuke13.2.exe"
        nukeX_arguments  = "--nukex"

        subprocess.Popen([f"{nuke_executable_path}", nukeX_arguments , nuke_file_path  ] , creationflags= subprocess.CREATE_NEW_CONSOLE)
















if __name__ == "__main__":
    app = QApplication()
    ui = RenderMate()
    ui.show()
    sys.exit(app.exec_())