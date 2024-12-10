# import modules
from pathlib import Path

# Get the current working directory as a dirPath object
dirpath = Path.cwd()

# Define the path to the 'icons' subfolder
icons_path = dirpath / 'icons' 

# Icon file paths for different actions or tools

ADD_ICON = icons_path / 'add_icon.png'
ADD_ICON = ADD_ICON.as_posix()

NUKE_ICON = icons_path / 'nuke_red_icon.png'
NUKE_ICON = NUKE_ICON.as_posix()

PLAY_ICON = icons_path / 'PLAY_ICON.png'
PLAY_ICON = PLAY_ICON.as_posix()

REMOVE_ICON = icons_path / 'REMOVE_ICON.png'
REMOVE_ICON = REMOVE_ICON.as_posix()

REMOVE_SELECTED_ICON = icons_path / 'REMOVE_SELECTED_ICON.png'
REMOVE_SELECTED_ICON = REMOVE_SELECTED_ICON.as_posix()

USER_ICON = icons_path / 'USER_ICON.png'
USER_ICON = USER_ICON.as_posix()