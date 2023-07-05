import shutil
source_folder = 'H://work_projects//network_slicing//ns//results'
destination_folder = 'H://work_projects//network_slicing//ns//prev_results'

# Copy the contents of the source folder to the destination folder
shutil.copytree(source_folder, destination_folder)

print("Folder contents copied successfully.")