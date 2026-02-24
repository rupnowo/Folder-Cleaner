# Packages
import os 
import shutil
import time
from pathlib import Path
from datetime import datetime

# Start proccess timer
start_time = time.time()

# Paths -
TARGET_FOLDER = Path.home() / "OneDrive/Pictures/Screenshots"
WHERELOGFILEGOES = Path.home() / "OneDrive/Desktop"
DELETE_FOLDER = Path.home() / "OneDrive/Pictures/To_Delete"

# Optional Folders for customization
SVAD_FOLDER = Path.home() / "OneDrive/Pictures/SVAD"
CSIA_FOLDER = Path.home() / "OneDrive/Pictures/CSIA"


# make sure delete folder exists
DELETE_FOLDER.mkdir(exist_ok=True)

# Time Settings
now = time.time()
MAX_FILE_AGE = 7 * 24 * 60 * 60 # days * hours * minutes * seconds

# File Tracking
deleted_files = []
moved_files_csia = []
moved_files_svad = []

# Starting loop process
for item in TARGET_FOLDER.iterdir():

    # Skip directories and the DELETE_FOLDER itself
    if item.is_dir() or item == DELETE_FOLDER:
        continue

    file_age = now - item.stat().st_mtime

    # Move files older than one week to delete folder
    if file_age > MAX_FILE_AGE:
        destination_path = DELETE_FOLDER / item.name

        # Handle duplicate names
        counter = 1
        while destination_path.exists():
            destination_path = DELETE_FOLDER / f"{item.stem}_{counter}{item.suffix}"
            counter += 1

        shutil.move(str(item), str(destination_path))
        deleted_files.append(destination_path.name)
    
    # organize files less than 1 week old
    # get first letter of filename
    second_letter = item.name[1]

    # only process alphabetic characters
    if not second_letter.isalpha():
        second_letter = "O"
    
    # move files 
    if second_letter == "V":
        destination_path = SVAD_FOLDER / item.name
        shutil.move(str(item), str(destination_path))
        moved_files_svad.append(item.name)
    elif second_letter == "S":
        destination_path = CSIA_FOLDER / item.name
        shutil.move(str(item), str(destination_path))
        moved_files_csia.append(item.name)


# End Timer
end_time = time.time()
duration = round(end_time - start_time, 2)

# Create log file
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file_path = WHERELOGFILEGOES / f"cleanup_log_{timestamp}.txt"

with open(log_file_path, "w") as log_file:
    log_file.write("Pictures Cleanup Log\n")
    log_file.write("=" * 30 + "\n\n")
    log_file.write(f"Date: {datetime.now()}\n\n")
    log_file.write(f"Total runtime: {duration} seconds\n")
    log_file.write("Files moved to DELETE_FOLDER:\n\n")

    for file_name in deleted_files:
        log_file.write(f"{file_name}\n")
    log_file.write("\n")
    log_file.write(f"Total files deleted: {len(deleted_files)}\n\n")
    
    # Logging files moved to csia folder
    log_file.write("Files moved to CSIA Folder: \n\n")
    for file_name in moved_files_csia:
        log_file.write(f"{file_name}\n")
    log_file.write("\n")
    log_file.write(f"Total files moved to CSIA folder: {len(moved_files_csia)}\n\n")

    # Logging files moved to svad folder
    log_file.write("Files moved to SVAD Folder: \n\n")
    for file_name in moved_files_svad:
        log_file.write(f"{file_name}\n")
    log_file.write("\n")
    log_file.write(f"Total files moved to SVAD folder: {len(moved_files_svad)}\n")

# Delete the entire delete folder after logging
if DELETE_FOLDER.exists():
    shutil.rmtree(DELETE_FOLDER)
