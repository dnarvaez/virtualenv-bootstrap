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

# This script is from https://github.com/dnarvaez/virtualenv-bootstrap

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import urllib.request

base_dir = os.path.dirname(os.path.abspath(__file__))
environ_namespace = "TEST"
start_message = "Installing virtualenv"
end_message = "\n"
packages = ["osourcer"]
submodules = []
virtualenv_version = "1.8.4"
virtualenv_dir = "sandbox"
cache_dir = "cache"
run_module = "osourcer.tool"
etag = "1"


def get_cache_dir():
    return os.path.join(base_dir, cache_dir)


def get_virtualenv_dir():
    return os.path.join(base_dir, virtualenv_dir)


def get_stamp_path():
    return get_virtualenv_dir() + ".stamp"


def get_bin_path(name):
    return os.path.join(get_virtualenv_dir(), "bin", name)


def create_virtualenv():
    source_dir = os.path.join(get_cache_dir(),
                              "virtualenv-%s" % virtualenv_version)

    if not os.path.exists(source_dir):
        url = "https://pypi.python.org/packages/source/v/" \
              "virtualenv/virtualenv-%s.tar.gz" % virtualenv_version

        f = urllib.request.urlopen(url)

        with tarfile.open(fileobj=f, mode="r:gz") as tar:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar, get_cache_dir())

    subprocess.check_call(["python3",
                           os.path.join(source_dir, "virtualenv.py"),
                           "-q", get_virtualenv_dir()])


def get_submodule_dirs():
    return [os.path.join(base_dir, submodule) for submodule in submodules]


def install_packages():
    args = [get_bin_path("pip"), "-q", "install"]
    args.extend(packages)
    args.extend(get_submodule_dirs())

    subprocess.check_call(args)


def upgrade_submodules():
    args = [get_bin_path("pip"), "-q", "install", "--no-deps", "--upgrade"]
    args.extend(get_submodule_dirs())

    subprocess.check_call(args)


def compute_submodules_hash():
    data = ""

    for submodule in submodules:
        for root, dirs, files in os.walk(os.path.join(base_dir, submodule)):
            for name in files:
                path = os.path.join(root, name)
                mtime = os.lstat(path).st_mtime
                data = "%s%s %s\n" % (data, mtime, path)

    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def check_stamp():
    try:
        with open(get_stamp_path()) as f:
            stamp = json.load(f)
    except (IOError, ValueError):
        return True, True

    return (stamp["etag"] != etag,
            stamp["submodules_hash"] != compute_submodules_hash())


def write_stamp():
    stamp = {"etag": etag,
             "submodules_hash": compute_submodules_hash()}

    with open(get_stamp_path(), "w") as f:
        json.dump(stamp, f)


def update_submodules():
    update = os.environ.get(environ_namespace + "_UPDATE_SUBMODULES", "yes")
    if update != "yes":
        return

    os.chdir(base_dir)
    for module in submodules:
        subprocess.check_call(["git", "submodule", "update", "--init",
                               module])


def main():
    os.environ["PIP_DOWNLOAD_CACHE"] = get_cache_dir()

    os.environ[environ_namespace + "_BASE_DIR"] = base_dir
    os.environ[environ_namespace + "_VIRTUALENV"] = get_virtualenv_dir()

    etag_changed, submodules_changed = check_stamp()

    if etag_changed:
        print(start_message)

        update_submodules()

        try:
            shutil.rmtree(get_virtualenv_dir())
        except OSError:
            pass

        create_virtualenv()
        install_packages()

        write_stamp()

        print(end_message)
    elif submodules_changed:
        upgrade_submodules()
        write_stamp()

    args = [get_bin_path("python3"), "-m", run_module]
    if len(sys.argv) > 1:
        args.extend(sys.argv[1:])

    os.execl(args[0], *args)


if __name__ == "__main__":
    main()
