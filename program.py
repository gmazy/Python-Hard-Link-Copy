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
    """Path in to path out function"""
    return os.path.join(path_out, os.path.relpath(path, path_in))

def hlink_file(file_path, new_file_path, failedfilelist=None):
    """Hard link creation with normal copy fallback function"""
    try:
        os.link(file_path, new_file_path)  # Create hard link (mklink /H)
        return True, False  # Successful hard link copy, not normal copy
    except OSError as error:
        if str(error).startswith("[WinError 1142]"):
            failedfilelist.append(os.path.basename(file_path))  # Add the failed file to the list
            copyfile(file_path, new_file_path)  # Do normal copy if file's hard link limit exceeded
            return True, True  # Successful normal copy
        else:
            print("Error:", error)  # Print any other errors that occur during copying
            time.sleep(5)
            return False, False  # Failed to copy

def hardlinkcopy(paths):
    """Main function to copy files and folders"""
    filecount = hardlink_count = normal_copy_count = 0
    failedfilelist = {}  # Initialize dictionary to track failed file copies by their paths
    starttime = time.time() # Start processing timer
    date_today = str(date.today())  # Get date for copy

    if len(paths) == 1 and os.path.isdir(paths[0]):  # Only one item dropped and it's a directory
        print("\nCopying folder(s):")
        print(paths[0])
    else:  # Files or multiple items dropped
        print("\nCopying file(s):")

    for path_in in paths:  # Go through each path
        if os.path.isfile(path_in):  # If the path is a file, make a copy
            if len(paths) > 1 or not os.path.isdir(paths[0]):  # If file or files were dropped (not a directory)
                print("File copied:", path_in)
            file_name, file_extension = os.path.splitext(os.path.basename(path_in))
            new_file_name = f"{file_name}-Copy-{date_today}{file_extension}"  # Output filename with date: Copy-2024-04-24
            new_file_path = os.path.join(os.path.dirname(path_in), new_file_name)
            success, normal_copy = hlink_file(path_in, new_file_path, failedfilelist=failedfilelist.setdefault(os.path.dirname(path_in), []))   # Counters for file and if hard link or not
            if success:
                filecount += 1
                if normal_copy:
                    normal_copy_count += 1
                else:
                    hardlink_count += 1
        elif os.path.isdir(path_in):  # If the path is a directory, copy its contents
            path_out = path_in + "-Copy-" + date_today  # Output path with date: foldername-Copy-2021-01-01
            if os.path.exists(path_out):
                path_out += "_"+str(time.strftime("%H%M%S"))

            os.makedirs(path_out, exist_ok=True)

            for folder, _, files in os.walk(path_in):  # Loop through subfolders and files
                newfolder = to_new_path(folder, path_in, path_out)
                if not os.path.isdir(newfolder):  # Make folder if it doesn't exist
                    os.mkdir(newfolder)
                    if folder != path_in:
                        print("Folder created:", newfolder)  # Print created subfolder

                for file in files:  # Loop files in folder
                    new_file_name = os.path.join(newfolder, file)
                    success, normal_copy = hlink_file(os.path.join(folder, file), new_file_name, failedfilelist=failedfilelist.setdefault(folder, []))  # Counters for file and if hard link or not
                    if success:
                        filecount += 1
                        if normal_copy:
                            normal_copy_count += 1
                        else:
                            hardlink_count += 1

    finished_in = round(time.time() - starttime)    # Completed task time

    if any(files for files in failedfilelist.values()): # Print failed file list
        print("\n\nFiles that failed to hard link:")
        for folder, files in failedfilelist.items():
            print(f"\nFailed files in: \"{folder}\"")
            for file in files:
                print(file)
        print(f"\nCopied {filecount} files in {finished_in} s") # Total number of files copied
        print(f"{hardlink_count} hard links | {normal_copy_count} normal copies")   # Count for hard links vs normal copy
        input("Press the enter key to continue.")
    else:   # When no failed files print number of hard link copied files
        print(f"\nCopied {filecount} files with hard link in {finished_in} s")
        time.sleep(3)

if len(sys.argv) > 1:
    hardlinkcopy(paths=sys.argv[1:])
else:
    print("Drag & Drop folders or loose files over this script to make copy using hard links.\n")    # Message displayed when running the script with no file dropped
    time.sleep(5)
