#!/usr/bin/env python3
# Copyright 2013 Daniel Narvaez
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request

environ_namespace = "TEST"

packages = ["osourcer"]

virtualenv_url = "https://pypi.python.org/packages/source/v/" \
                 "virtualenv/virtualenv-1.8.4.tar.gz"

virtualenv_dir = "sandbox"

run_module = "osourcer.tool"


def get_base_dir():
    return os.path.dirname(os.path.abspath(__file__))


def get_virtualenv_dir():
    return os.path.join(get_base_dir(), virtualenv_dir)


def get_bin_path(name):
    return os.path.join(get_virtualenv_dir(), "bin", name)


def create_virtualenv():
    if os.path.exists(get_virtualenv_dir()):
        return

    f = urllib.request.urlopen(virtualenv_url)

    temp_dir = tempfile.mkdtemp()

    with tarfile.open(fileobj=f, mode="r:gz") as tar:
        tar.extractall(temp_dir)

    source_dir = os.path.join(temp_dir, os.listdir(temp_dir)[0])

    try:
        subprocess.check_call(["python3",
                               os.path.join(source_dir, "virtualenv.py"),
                               "-q", get_virtualenv_dir()])
    finally:
        shutil.rmtree(temp_dir)


def install_packages():
    args = [get_bin_path("pip"), "-q", "install"]
    args.extend(packages)

    subprocess.check_call(args)


def main():
    os.environ[environ_namespace + "_DIR"] = get_base_dir()
    os.environ[environ_namespace + "_VIRTUALENV"] = get_virtualenv_dir()

    try:
        create_virtualenv()
        install_packages()
    except (subprocess.CalledProcessError, KeyboardInterrupt) as e:
        shutil.rmtree(get_virtualenv_dir())
        raise e

    args = [get_bin_path("python3"), "-m", run_module]
    if len(sys.argv) > 1:
        args.extend(sys.argv[1:])

    subprocess.check_call(args)


if __name__ == "__main__":
    main()
