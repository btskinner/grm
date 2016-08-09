GitRoom Manager  
===============

GitRoom Manager allows instructors to more easily manage a
GitHub-based virtual classroom. From within the program, the user can:

- Initialize student repositories, locally and remotely, from a CSV
  roster and a local master repository
- Add students to an existing course
- Add administrators to the course (other instructors)
- Update student repositories with new course content
- Pull from/push to student repositories
- Grade assignments

Requirements
------------

- Python 3.x
- Ownership of a `GitHub Classroom`_
.. _GitHub Classroom: https://classroom.github.com/  

Installation
------------

To install the `grm` module, clone the repository to your local
machine and `cd` into the top-level directory. From the terminal, type:

.. code::

   python setup.py install


*NOTE:* You may need to use `python3` or `python3.x` in place of
`python` in order to utilize a Python 3 installation.


Usage
-----

You can call GitRoom Manager from within an interactive Python session by
calling:

.. code:: python

   import grm
   grm.main()

the installation also adds an executable to your path. You can call
GitRoom Manager from terminal using:

.. code::

   $ gitroom

   

