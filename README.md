# About

Simple script to bootstrap a python environment using a virtualenv. It's a
single file which is copied inside a python project and customized. It takes
care of downloading virtualenv, setting it up, installing packages and finally
running the specified python module.

# Usage

Copy the file into your project, then edit the value of the following variables
at the top of it

* message

    A message to print before starting.

* environ_namespace

    Namespace prepended to environment variables.

* packages

    A list of packages to install.

* virtualenv_version

    The virtualenv version number.

* virtualenv_dir

    Path of the virtualenv installation.

* cache_dir

    A directory where to cache downloads.
