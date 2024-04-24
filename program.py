# ##### BEGIN LICENSE BLOCK #####
#
# This program is licensed under Creative Commons CC0
# https://creativecommons.org/publicdomain/zero/1.0/
#
# ##### END LICENSE BLOCK #####

# Author  : Gmazy/Mazay (Multi loose file/folder support by STRmods)
# Purpose : Drag & Drop folders or loose files over this script to make copy using hardlinks

import os, sys, re, time
from datetime import date, datetime
from shutil import copyfile

print("\nHard Link Copier V 1.1\n")


def to_new_path(path, path_in, path_out):
    relative_path = os.path.relpath(path, path_in)  # Remove path_in
    new_path = os.path.join(path_out, relative_path)  # Add path_out
    if new_path == path:
        raise ValueError('Path failed to be updated')
    return new_path

def hlink_file(file_path, path_out):
    filename, extension = os.path.splitext(file_path)
    new_file_name = filename + "-Copy-" + str(date.today()) + extension
    try:
        os.link(file_path, new_file_name)  # Create hard link with new name
        print("Individual file dropped, date being inserted into file name...")
        # Output filename with date: Copy-2024-04-24
        print("File copied:", new_file_name)
        return True
    except OSError as error:
        # Do normal copy if file's hardlink limit exceeded
        if str(error).startswith("[WinError 1142]"):
            copyfile(file_path, new_file_name)
            print("File copied:", new_file_name)
            return True
        else:
            input(str(error) + "\nFailed to copy file, Press any key to continue")
            return False


def hardlinkcopy(paths):
    filecount = 0
    failedfilelist = ''
    starttime = time.time()

    for path_in in paths:
        if os.path.isfile(path_in):
            if hlink_file(path_in, os.path.dirname(path_in)):
                filecount += 1
        elif os.path.isdir(path_in):
            # Output path with date: foldername-Copy-2021-01-01
            path_out = path_in + "-Copy-" + str(date.today())

            # Output path with timestamp if folder exist
            if os.path.exists(path_out):
                path_out += "_"+str(datetime.now().strftime("%H%M%S"))

            print("\nCopying", path_in, "-->", path_out)
            # Create the output folder with the new name
            os.makedirs(path_out, exist_ok=True)

            # Loop through subfolders and files
            for folder, subFolders, files in os.walk(path_in):
                newfolder = to_new_path(folder, path_in, path_out)

                # Make folder
                if not os.path.isdir(newfolder):
                    print("Mkdir", newfolder)
                    os.mkdir(newfolder)

                # Loop files in folder
                for file in files:
                    filename, extension = os.path.splitext(file)
                    new_file_name = filename + extension

                    # Copy files with hard link
                    try:
                        os.link(os.path.join(folder, file), os.path.join(newfolder, new_file_name))  # mklink /H
                        print("File copied:", new_file_name)
                    except OSError as error:
                        # Do normal copy if file's hardlink limit exceeded
                        if str(error).startswith("[WinError 1142]"):
                            failedfilelist += str(file) + ", "
                            copyfile(os.path.join(folder, file), os.path.join(newfolder, new_file_name))
                            print("File copied:", new_file_name)
                        else:
                            input(str(error) + "\nFailed to copy file, Press any key to continue")

                    # Print copied file count once in 2000 files
                    filecount += 1
                    if (filecount % 2000 == 0):
                        print("No. of files copied: ", filecount)

    finished_in = round(time.time() - starttime)

    # Print list of files copied as normal files
    if failedfilelist != '':
        print("\n\n", failedfilelist)
        print("\nNotice: Files above exceeded maximum of 1023 hard link duplicates and were created as normal copies.\n")
        input("Press any key to continue")
    
    # Finished            
    print("\nCopied", filecount, "files in", finished_in, "s\n")
 

# Capture drag and drop
if len(sys.argv) > 1:  # if files or folders are dropped on script
    hardlinkcopy(paths=sys.argv[1:])
else:
    print("Drag & Drop folders or loose files over this script to make copy using hardlinks.\n")
    time.sleep(5)
    