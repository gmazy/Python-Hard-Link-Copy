# ##### BEGIN LICENSE BLOCK #####
#
# This program is licensed under Creative Commons CC0
# https://creativecommons.org/publicdomain/zero/1.0/
#
# ##### END LICENSE BLOCK #####

# Author  : Gmazy/Mazay
# Purpose : Drag & Drop folder over to make copy using hardlinks

import os, sys, re, time
from datetime import date, datetime
from shutil import copyfile

print("\nHard Link Copier V 1.0\n")


def to_new_path(path, path_in, path_out):
    relative_path = os.path.relpath(path, path_in) # Remove path_in
    new_path = os.path.join(path_out, relative_path) # Add path_out
    if new_path == path: raise ValueError('Path failed to be updated')
    return new_path

def hardlinkcopy(path_in):
    # Output path with date: foldername-Copy-2021-01-01
    path_out = path_in + "-Copy-" + str(date.today())
    
    # Output path with timestamp if folder exist
    if os.path.isdir(path_out): 
        path_out += "_"+str(datetime.now().strftime("%H%M%S"))
    
    print("\nCopying",path_in,"-->",path_out)  


    filecount = 0
    failedfilelist = ''
    starttime = time.time()

    # Loop through subfolders
    for folder, subFolders, files in os.walk(path_in):
        newfolder = to_new_path(folder, path_in, path_out)
        
        # Make folder
        if not os.path.isdir(newfolder):
            print("Mkdir",newfolder)
            os.mkdir(newfolder)
            
        # Loop files in folder
        for file in files:
            
            # Copy files with hard link
            try :
                os.link( os.path.join(folder,file), os.path.join(newfolder,file) ) # mklink /H
            except OSError as error : 
                # Do normal copy if file's hardlink limit exceeded
                if str(error).startswith("[WinError 1142]"):
                    failedfilelist += str(file) + ", "
                    copyfile( os.path.join(folder,file), os.path.join(newfolder,file) )
                else:
                    input(str(error)+"\nFailed to copy file, Press any key to continue")
                
            # Print copied file count once in 2000 files
            filecount += 1
            if (filecount % 2000 == 0):
                print("No. of files copied: ",filecount)

    finished_in = round(time.time()-starttime)
    
    # Print list of files copied as normal files
    if failedfilelist != '':
        print("\n\n",failedfilelist)
        print("\nNotice: Files above exceeded maximum of 1023 hard link duplicates and were created as normal copies.\n")
        input("Press any key to continue")
    
    # Finished            
    print("\nCopied", filecount, "files in", finished_in, "s\n")
 

# Capture drag and drop
if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]): # if folder exists
    hardlinkcopy(path_in=sys.argv[1])
else:
    print("To make copy of folder drag and drop it over.\n")
    time.sleep(5)
    