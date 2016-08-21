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

Manual
------

A more complete manual for GitRoom Manager can be found at
`btskinner.me/grm <http://btskinner.me/grm>`__



.. |Build Status| image:: https://travis-ci.org/btskinner/grm.svg?branch=master
   :target: https://travis-ci.org/btskinner/grm
.. |PyPI version| image:: https://badge.fury.io/py/grm.svg
   :target: https://badge.fury.io/py/grm
