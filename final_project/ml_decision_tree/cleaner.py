import os
import shutil
from config import remove_dir_name


def remove_model_from_local_directory(model_name: str):
    if os.path.exists(model_name):
        os.remove(model_name)
        print(f"The file {model_name} has been deleted successfully")
    else:
        print(f"The file {model_name} does not exist!")


def remove_wand_local_directory():
    if os.path.isdir(remove_dir_name):
        shutil.rmtree(remove_dir_name)
    else:
        print(f'{remove_dir_name} directory does not exist!')


def clean_all(model_name: str):
    remove_model_from_local_directory(model_name)
    remove_wand_local_directory()