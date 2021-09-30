# Python Hard Link Copy


## Usage

Drag & Drop folder over **hardlinkcopy.bat** to make linked copy of folder.


### Benefits of linked copy
- Copy terabytes of data instantly
- Copy does not consume disk space
- Files mostly behave just like regular files.
- Unique copies of files will be stored only for files that are changed saving disk space.

### Cons of linked copy
- Properties of files are shared. Read only checkbox in file properties will affect both files.
- Linked copies are only possible among same partition.
- Windows reports filesize incorrectly.
- While deleting file or saving over it does not affect shared data, it's still possible for special software to change all linked copies of file at once.

### Things that turn linked copy back into normal file
- Moving file out of disk or partition
- Making copy of file
- Saving changes to file
