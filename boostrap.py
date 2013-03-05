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
import tarfile
import tempfile
import urllib.request

packages = []

virtualenv_url = "https://pypi.python.org/packages/source/v/" \
                 "virtualenv/virtualenv-1.8.4.tar.gz"

virtualenv_dir = os.path.join(os.path.dirname(__file__), "sandbox")

run_module = ""


def create_virtualenv():
    if os.path.exists(virtualenv_dir):
        return

    f = urllib.request.urlopen(virtualenv_url)

    temp_dir = tempfile.mkdtemp()

    with tarfile.open(fileobj=f, mode="r:gz") as tar:
        tar.extractall(temp_dir)

    source_dir = os.path.join(temp_dir, os.listdir(temp_dir)[0])

    try:
        subprocess.check_call(["python3",
                               os.path.join(source_dir, "virtualenv.py"),
                               virtualenv_dir])
    finally:
        shutil.rmtree(temp_dir)


def install_packages():
    args = [os.path.join(virtualenv_dir, "bin", "pip"), "-q", "install"]
    args.extend(packages)

    subprocess.check_call(args)


def main():
    try:
        create_virtualenv()
        install_packages()
    except (subprocess.CalledProcessError, KeyboardInterrupt) as e:
        shutil.rmtree(virtualenv_dir)
        raise e

    subprocess.check_call(["python3", "-m", run_module])


if __name__ == "__main__":
    main()
