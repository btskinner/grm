---
layout: default
title: Setup
---

# Basic master course directory structure

A basic master course directory structure might look like this:

```
MasterRepo
|__ Lessons
|   |__ lesson_1.md
|   |__ lesson_2.md 
|__ Assignments
    |__ assignment_1
    |   |__ assignment_1.md
    |__ assignment_2
    	  |__ assignment_2.md

```

Student directories will mimic this master course repo exactly:

```
StudentClassDirectory
|__ Student_1
|	 |__ Lessons
|	 |   |__ lesson_1.md
|	 |   |__ lesson_2.md 
|	 |__ Assignments
|    	  |__ assignment_1
|    	  |   |__ assignment_1.md
|    	  |__ assignment_2
|    	  	   |__ assignment_2.md
|__ Student_2
|	 |__ Lessons
|	 |   |__ lesson_1.md
|	 |   |__ lesson_2.md 
|	 |__ Assignments
|    	  |__ assignment_1
|    	  |   |__ assignment_1.md
|    	  |__ assignment_2
|    	  	   |__ assignment_2.md
|__ Student_3
	 |__ Lessons
	 |   |__ lesson_1.md
	 |   |__ lesson_2.md 
	 |__ Assignments
    	  |__ assignment_1
    	  |   |__ assignment_1.md
    	  |__ assignment_2
    	  	   |__ assignment_2.md

```

# Files that are not synced with master

## Hidden or dot (`.`) files

Hidden files and directories, those that start with a dot (`.`), are not copied to the student repositories. This prevents clutter as well as keeps the master course repo `.git` directory (if it has one) from overwritting the student `.git` directories.

## Files and subdirectories starting with an underscore

Subdirectories beginning with an underscore are not copied. This is allows the instructor to have hidden working directories. These can be used for grading, instructor working files (lessons/assignments not ready to share), and even hosting the local student repos. 

# Updated directory structure

Here's an updated example of a GitHub course directory. All files are stored in a single master course directory. `_gitadmin`, `_working`, and
`_student_repositories` will not be copied into the local student repos.

```
MasterRepo
|__ .git
|__ .gitignore
|__ Lessons
|   |__ lesson_1.md
|   |__ lesson_2.md 
|__ Assignments
|   |__ assignment_1
|   |   |__ assignment_1.md
|   |__ assignment_2
|    	  |__ assignment_2.md
|__ _gitadmin
|   |__ GitHub_token.txt
|   |__ CourseRoster.csv
|   |__ <CourseName>_grm.json
|__ _working
|   |__ assignment_3.md
|__ _student_repositories
	|__ Student_1
	|	 |__ Lessons
	|	 |   |__ lesson_1.md
	|	 |   |__ lesson_2.md 
	|	 |__ Assignments
	|    	  |__ assignment_1
	|    	  |   |__ assignment_1.md
	|    	  |__ assignment_2
	|    	  	   |__ assignment_2.md
	|__ Student_2	
	|	 |__ Lessons
	|	 |   |__ lesson_1.md
	|	 |   |__ lesson_2.md 
	|	 |__ Assignments
	|    	  |__ assignment_1
	|    	  |   |__ assignment_1.md
	|    	  |__ assignment_2
	|    	  	   |__ assignment_2.md
	|__ Student_3
		 |__ Lessons
	 	 |   |__ lesson_1.md
	 	 |   |__ lesson_2.md 
	 	 |__ Assignments
    	 	  |__ assignment_1
    	  	  |   |__ assignment_1.md
    	  	  |__ assignment_2
    	  	  	   |__ assignment_2.md

```

In this example, the GitRoom Manager json file, course roster, and API token reside in the master course repo, but aren't shared with students.

## Very Important Note!

If you use underscore directories in your master course repo and host it on GitHub, for example, be sure to add `/_*` to your `.gitignore` file so that your and your students' sensitive data aren't pushed to the remote. This will also prevent the remote master course repo and `.git` directory from blowing up in size.

If you want to sync a single underscore subdirectory with your remote (the `_working` subdirectory, for example), just add `!/_<important dir to sync>` to your `.gitignore` file. 

*E.g.*

```
# .gitignore

/_*
!/_working
```