import os, shutil

FOLDER_PATH = "/home/atulkumar/Documents/"
DELETE_FOLDER = [
    "Objectives"
]

def delete_folder(FOLDER_PATH, DELETE_FOLDER):
    folders = os.listdir(FOLDER_PATH)
    for d_f in DELETE_FOLDER:
        for f in folders:
            sub_folder_path = os.path.join(FOLDER_PATH, f)
            if os.path.isdir(sub_folder_path):
                if d_f == f:
                    try:
                        shutil.rmtree(sub_folder_path)
                        print(f"{sub_folder_path} Deleted!")
                    except Exception as e:
                        print(f"{sub_folder_path} Not Deleted!")
                else:
                    delete_folder(sub_folder_path, DELETE_FOLDER)

if input("Are you sure? [y|N] ").lower() in ["y", "yes"]:
    delete_folder(FOLDER_PATH, DELETE_FOLDER)
