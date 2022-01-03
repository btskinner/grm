---
layout: default
title: Start
---

# Getting started

The first time you setup a course with GitRoom Manager, you will need
the following things:

1. Your GitHub login ID
2. GitHub organization for which you are the owner
3. GitHub token stored in text file
4. Student roster file [CSV]
5. Location of main course repository
6. Location of student directories (top level directory that hold them
   all)

When you open GitRoom Manager, it will ask you:

```
------------------------------------------------
How would you like to enter GitRoom information?
------------------------------------------------

( 1 ) Manually
( 2 ) From JSON file
```

If this is the first time you have opened GitRoom Manager for the
course, you will have to choose the first option. GitRoom Manager will
ask you for each item.

Once complete, GitRoom Manager will ask if you want to store all the
relevant information in a JSON file. You will have a chance to review
what you've typed and then be able to select the directory in which to
store the file. In the future, you can choose the second option to get
started more quickly.

# Locations of files

When telling GitRoom Manager where to find the relevant files, you may
use relative or absolute paths.

# Example student roster

|last\_name|first\_name|ghid|  
|:---:|:---:|:---:|  
|Skinner|Benjamin|btskinner|  
|Student|Bob|bstudent|

The column names do not have to match these, but your roster must have
three columns: first name, last name, and student GitHub ID with no
missing values.

If your column names do not match those above, GitRoom Manager will as
you to select the column that matches each required element. At the
end, it will as if you want to resave the roster with the GitRoom
Manager names in place of the old (nothing else changed). If you
choose no, you will have to go through the same manual selection
process each time you log into the manager.

