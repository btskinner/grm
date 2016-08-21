---
layout: default
title: Usage
---

# Usage

You can call GitRoom Manager from within an interactive Python session
by calling:

```python
import grm
grm.main()
```

The installation also adds an executable script to your path. You can
call GitRoom Manager from terminal using:

```bash
$ gitroom
```

### NOTE 

The command line script is just a wrapper for the first set of
commands above. The script searches your environment for your Python 3.x
interpreter. If it cannot find it, the script may revert to your system
Python interpreter---which is often 2.x---and may fail. If you have
trouble with the command line script, first make sure that your Python
3.x interpreter is in your system path and callable by `python3`.

# Starting menu

Once started, GitRoom Manager will give you a number of options:

```
--------------------------
What would you like to do?
--------------------------

( 1 ) Initialize class
( 2 ) Add students to class
( 3 ) Add new administrator
( 4 ) Clone repositories
( 5 ) Update student remote repositories with local master
( 6 ) Pull down from remote student repositories
( 7 ) Push from local student repositories to remotes
( 8 ) Grade student assignments
( 9 ) << Exit Program >>
```

When first opening the program, you will have to input the relevant course information either by hand through a JSON file (see [Getting started](../start/)). Once set, these values will persist until you close GitRoom Manager. 

Once you select an option, GitRoom Manager will go ask relevant questions, if any. At the end of a task, you will be asked if you wish to exit the program or perform another task. You may exit GitRoom Manager at any time using `Ctrl-D`.


