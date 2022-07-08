"""
A simple module consisting of an init function to easily generate a new
python package. It could in the future be part of a complete tool to maintain
packages.
terminal and use:
    >>> from pylejandria.module import init
    >>> init()
It will write all the necesary files and folder for an easy pypi project. You
must check each file to fill all the info.
"""

import os
from pylejandria.gui import ask

SETUP = f"""[metadata]
    name = module_name
    version = 0.0.1
    author = _____
    author_email = _____
    description = _____
    long_description = _____
    long_description_content_type = text/markdown
    url = _____
    project_urls =
        Bug Tracker = _____
    classifiers =
        Programming Language :: Python :: 3
        License :: OSI Approved :: MIT License
        Operating System :: OS Independent

    [options]
    package_dir =
        = src
    packages = find:
    python_requires = >= _____

    [options.packages.find]
    where = src"""

PYPROJECT = f"""[build-system]
    requires = [
        "setuptools>=42",
        "wheel"
    ]
    build-backend = "setuptools.build_meta"""

LICENSE = f"""MIT License
    Copyright (c) [_____] [_____]

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE."""


def init(name: str) -> None:
    src = ask('directory')
    if not src:
        return
    folders = [f'{src}/src', f'{src}/src/{name}', f'{src}/tests']
    files = [
        ('setup.cfg', SETUP.replace('module_name', name)),
        ('pyproject.toml', PYPROJECT),
        ('LICENSE', LICENSE),
        ('README.md', ''),
        (f'/src/{name}/__init__.py', '')
    ]
    for folder in folders:
        os.makedirs(folder)

    for file, info in files:
        with open(f'{src}/{file}', 'w') as f:
            f.write(info)


if __name__ == '__main__':
    init('Testing')
