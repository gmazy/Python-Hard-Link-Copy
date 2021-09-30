# Python Hard Link Copy


**Install**

Download version from releases if you don't have Python installed.


**Usage**

Drag & Drop folder over hardlinkcopy.bat to make linked copy of folder.



**Benefits of linked copy**
- Backup terabytes of data in instant backups that do not initially consume any disk space.
- Files mostly behave just like regular files.

**Cons of linked copy**
- Properties of files are shared. Read only checkbox in file properties will affect both files.
- Windows reports full filesize even file does not consume space.
- Linked copies are only possible among same partition.
- While deleting file or saving over it does not affect shared data, it's still possible for special software to change all linked copies of file at once.

**Things that turn linked copy back into normal file**
- Moving file out of disk or partition
- Making copy of file
- Saving changes to file