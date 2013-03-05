# About

Simple script to bootstrap a python environment using a virtualenv. It's a
single file which is copied inside a python project and customized. It takes
care of downloading virtualenv, setting it up, installing packages and finally
running the specified python module.

# Usage

Copy the file into your project, then edit the value of the following variables
at the top of it

* packages

    A list of packages to install.

* virtualenv_url

    URL to the virtualenv source tarball.

* virtualenv_dir

    Path of the virtualenv installation.

