GitRoom Manager
===============

|Build Status| |PyPI version|

GitRoom Manager allows instructors to more easily manage a GitHub-based
virtual classroom. From within the program, the user can:

-  Initialize student repositories, locally and remotely, from a CSV
   roster and a local master repository
-  Add students to an existing course
-  Add administrators to the course (other instructors)
-  Associate each student with a personal private repository
-  Update student repositories with new course content
-  Pull from/push to student repositories
-  Grade assignments

Requirements
------------

-  Python >= 3.3
-  Git >= 2.0
-  Ownership of a `GitHub Classroom <https://classroom.github.com/>`__
-  `GitHub Personal
   Token <https://help.github.com/articles/creating-an-access-token-for-command-line-use/>`__
   with full permissions
-  Class roster with columns for student: first name, last name, GitHub
   ID

Installation
------------

To install the ``grm`` module, clone the repository to your local
machine and ``cd`` into the top-level directory. From the terminal,
type:

::

    python setup.py install

*NOTE:* You may need to use ``python3`` or ``python3.x`` in place of
``python`` in order to utilize a Python 3.x installation.

You may also install with pip:

.. code:: bash

    pip install grm

Usage
-----

You can call GitRoom Manager from within an interactive Python session
by calling:

.. code:: python

    import grm
    grm.main()

The installation also adds an executable script to your path. You can
call GitRoom Manager from terminal using:

.. code:: bash

    $ gitroom

*NOTE:* The command line script is just a wrapper for the first set of
commands above. The script searches your environment for your Python 3.x
interpreter. If it cannot find it, the script may revert to your system
Python interpreter---which is often 2.x---and may fail. If you have
trouble with the command line script, first make sure that your Python
3.x interpreter is in your system path and callable by ``python3``.

How it works
------------

GitRoom Manager uses a primary course repository on your local machine
as the basis for each student's personal repository. When seeding
student repositories, you are actually copying from the local master to
each student's personal directory and then performing git interactions
from within those repositories.

A setup might look this:

::

    ./CourseDir
     +-./MasterRepo
     |      +-./Lessons
     |      |      +-lesson_1.md
     |      |      +-lesson_2.md
     |      |
     |      +-./Assignments
     |         +-./assignment_1
     |         |      +-assignment_1.md
     |         +-./assignment_2
     |            +-assignment_2.md
     +-./student_smith           
     |      +-./Lessons
     |      |      +-lesson_1.md
     |      |      +-lesson_2.md
     |      |
     |      +-./Assignments
     |         +-./assignment_1
     |         |      +-assignment_1.md
     |         +-./assignment_2
     |            +-assignment_2.md
     +-./student_skinner         
     |      +-./Lessons
     |      |      +-lesson_1.md
     |      |      +-lesson_2.md
     |      |
     |      +-./Assignments
     |         +-./assignment_1
     |         |      +-assignment_1.md
     |         +-./assignment_2
     |            +-assignment_2.md
     

When adding files (*e.g.*, new lessons/assignments), GitRoom Manager
uses the ``rsync`` utility to copy files from the course master to each
student repository. **Any existing files that have been changed by the
student but not the instructor will be overwritten.** This is an
important feature in that it allows the instructor to make changes to
existing files (*e.g.*, corrections to lessons). It is important,
therefore, that students learn a workflow in which they create new files
when pushing their assignments.

A couple of notes about the syncing:

1. Hidden files and directories are not copied to the student
   repositories. This prevents clutter as well as keeps the MasterRepo
   ``.git`` directory (if it has one) from overwritting the student
   ``.git`` directories.
2. Subdirectories beginning with an underscore are not copied. This is
   allows the instructor to have hidden working directories. In fact,
   the student repositories can be copied into the MasterRepo as long as
   they live in a directory starting with and underscore.

Here's an updated example. ``_gitadmin``, ``_working``, and
``_student_repositories`` will not be copied into the ``student_<name>``
local repositories:

::

    +-./MasterRepo
     +-./Lessons
     |      +-lesson_1.md
     |      +-lesson_2.md
     |
     +-./Assignments
     |      +-./assignment_1
     |      |      +-assignment_1.md
     |      +-./assignment_2
     |         +-assignment_2.md
     +-./_gitadmin
     |      +-GitHub_token.txt
     |      +-CourseRoster.csv
     |      +-<CourseName_grm.json
     +-./_working
     |
     +-./_student_repositories
     |      +-./student_smith            
     |             +-./Lessons
     |             |      +-lesson_1.md
     |             |      +-lesson_2.md
     |             |
     |             +-./Assignments
     |                +-./assignment_1
     |                |      +-assignment_1.md
     |                +-./assignment_2
     |                   +-assignment_2.md
     

*NOTE:* If you structure your MasterRepo this way and host it on GitHub,
be sure to add ``/_*`` to your ``.gitignore`` file so that your and your
students' sensitive data aren't pushed to the remote.

Example Roster
--------------

+--------------+---------------+-------------+
| last\_name   | first\_name   | ghid        |
+==============+===============+=============+
| Skinner      | Benjamin      | btskinner   |
+--------------+---------------+-------------+
| Student      | Bob           | bstudent    |
+--------------+---------------+-------------+

.. |Build Status| image:: https://travis-ci.org/btskinner/grm.svg?branch=master
   :target: https://travis-ci.org/btskinner/grm
.. |PyPI version| image:: https://badge.fury.io/py/grm.svg
   :target: https://badge.fury.io/py/grm
