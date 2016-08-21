---
layout: default
title: grm
---

# About 

GitRoom Manager allows instructors to more easily manage a GitHub-based
virtual classroom from the command line. From within the program, the user can:

-   Initialize student repositories, locally and remotely, from a CSV
    roster and a local master repository
-   Add students to an existing course
-   Add administrators to the course (other instructors)
-   Associate each student with a personal private repository
-   Update student repositories with new course content
-   Pull from/push to student repositories
-   Grade assignments

Requirements
------------

-   Python &gt;= 3.3
-   Git &gt;= 2.0
-   Ownership of a [GitHub Classroom](https://classroom.github.com/)
-   [GitHub Personal
    Token](https://help.github.com/articles/creating-an-access-token-for-command-line-use/)
    with full permissions
-   Class roster with columns for student: first name, last name, GitHub
    ID

Installation
------------

To install the `grm` module, clone the repository to your local machine
and `cd` into the top-level directory. From the terminal, type:

```
python setup.py install
```

*NOTE:* You may need to use `python3` or `python3.x` in place of
`python` in order to utilize a Python 3.x installation.

You may also install with pip:

```bash
pip install grm
```
