.. Poetryenv documentation master file, created by
   sphinx-quickstart on Fri Apr 24 09:11:23 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Poetryenv
=====================================

Poetryenv is a tool to create new Python project with a project template and specific Python version.

-----------------------

Requirements
=====================================
These tools are needed.

- Poetry_
- Pyenv_

.. _Poetry: https://python-poetry.org/
.. _Pyenv: https://github.com/pyenv/pyenv


Installation
=====================================

Clone this repo and go to the ``poetryenv`` directory.

.. code-block::

   git clone https://github.com/1izard/poetryenv.git
   cd poetryenv

New ``virtualenv`` environment is created automatically and then ``poetryenv`` is installed into the environment.

.. code-block::

   poetry install --no-dev


Usage
=====================================

|  You can create new Python project specifying Python version.
|  Pyenv and Poetry use the Python version in created project directory so you can manage Python version and packages for your project.

|  Basic usage is the same with ``new`` command of Poetry but you can use ``--py`` option like below. 
|  <path> is the destination to make the new project. if ``--name`` optoin is ommited, last directory of the <path> is used as the package name.
- ``poetryenv new --py X.X.X <path>``
- ``poetryenv new --py X.X.X --name <project_name> <path>``

e.g.

.. code-block::

   root@412e4c9d81ae:/home/1izard# poetryenv list -i
   Installed Python versions:
   3.6.5
   3.7.4


   root@412e4c9d81ae:/home/1izard# poetryenv new --py 3.7.4 poetryenv-demo374
   > python 3.7.4 is already installed.
   ⠋ Creating new python project
   > Created package poetryenv_demo374 in poetryenv-demo374
   ✔ Creating new python project

   root@412e4c9d81ae:/home/1izard# ls
   poetryenv-demo374


   root@412e4c9d81ae:/home/1izard# tree poetryenv-demo374
   poetryenv-demo374
   ├── poetryenv_demo374
   │   └── __init__.py
   ├── pyproject.toml
   ├── README.rst
   └── tests
       ├── __init__.py
       └── test_poetryenv_demo374.py

   2 directories, 5 files


   root@412e4c9d81ae:/home/1izard# cd poetryenv-demo374/
   root@412e4c9d81ae:/home/1izard/poetryenv-demo374# poetry env info

   Virtualenv
   Python:         3.7.4
   Implementation: CPython
   Path:           NA

   System
   Platform: linux
   OS:       posix
   Python:   /root/.pyenv/versions/3.7.4

   
   root@412e4c9d81ae:/home/1izard/poetryenv-demo374# cat pyproject.toml
   [build-system]
   requires = [ "poetry>=0.12",]
   build-backend = "poetry.masonry.api"

   [tool.poetry]
   name = "poetryenv-demo374"
   version = "0.1.0"
   description = ""
   authors = [ "1izard",]

   [tool.poetry.dependencies]
   python = "^3.7"

   [tool.poetry.dev-dependencies]
   pytest = "^5.2"


|  If passed Python version is not in your environment, ``poetryenv`` installs the Python of the specified version automatically using Pyenv.

e.g.

.. code-block::

   root@412e4c9d81ae:/home/1izard# poetryenv list -i
   Installed Python versions:
   3.6.5
   3.7.4


   root@412e4c9d81ae:/home/1izard# poetryenv new --py 3.8.0 poetryenv-demo380
   > Installing python 3.8.0 is completed.
   ⠹ Creating new python project
   > Created package poetryenv_demo380 in poetryenv-demo380
   ✔ Creating new python project


   root@412e4c9d81ae:/home/1izard# ls
   poetryenv-demo374  poetryenv-demo380


   root@412e4c9d81ae:/home/1izard# tree poetryenv-demo380
   poetryenv-demo380
   ├── poetryenv_demo380
   │   └── __init__.py
   ├── pyproject.toml
   ├── README.rst
   └── tests
       ├── __init__.py
       └── test_poetryenv_demo380.py

   2 directories, 5 files


   root@412e4c9d81ae:/home/1izard# cd poetryenv-demo380
   root@412e4c9d81ae:/home/1izard/poetryenv-demo380# poetry env info

   Virtualenv
   Python:         3.8.0
   Implementation: CPython
   Path:           NA

   System
   Platform: linux
   OS:       posix
   Python:   /root/.pyenv/versions/3.8.0


   root@412e4c9d81ae:/home/1izard/poetryenv-demo380# cat pyproject.toml
   [build-system]
   requires = [ "poetry>=0.12",]
   build-backend = "poetry.masonry.api"

   [tool.poetry]
   name = "poetryenv-demo380"
   version = "0.1.0"
   description = ""
   authors = [ "1izard",]

   [tool.poetry.dependencies]
   python = "^3.8"

   [tool.poetry.dev-dependencies]
   pytest = "^5.2"


Commands
====

| You can also see this description using ``poetryenv -h``.
| The description of each option is shown by ``poetryenv new -h`` or ``poetryenv list -h``.
|

+---------+----------------+-----------+-------------------------------------------------+
| Command | Option         | Argument  | Description                                     |
+---------+----------------+-----------+-------------------------------------------------+
| new     |                | <path>    | Create new Python project to <path>             |
+---------+----------------+-----------+-------------------------------------------------+
|         | --name         | <name>    | Set the resulting package name                  |
+---------+----------------+-----------+-------------------------------------------------+
|         | --src          |           | Use the src layout for the project              |
+---------+----------------+-----------+-------------------------------------------------+
|         | --py           | <version> | Set the Python version                          |
+---------+----------------+-----------+-------------------------------------------------+
| list    |                |           | Display available Python versions               |
+---------+----------------+-----------+-------------------------------------------------+
|         | --installed/-i |           | Display available and installed Python versions |
+---------+----------------+-----------+-------------------------------------------------+
