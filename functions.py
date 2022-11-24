import os

def make_dir(dir_name):
    try:
        os.mkdir(dir_name)
        print("Directory ", dir_name, " created.")
    except FileExistsError:
        print("Directory ", dir_name, " already exist.")