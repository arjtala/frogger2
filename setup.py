#!/usr/bin/env python3

# Copyright (c) Meta Platforms, Inc. and affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


import sys
import typing as t

from setuptools import setup, find_packages

with open("README.md", encoding="utf8") as f:
    readme = f.read()

requirements: t.List = []
with open("requirements.txt") as f:
    reqs = f.read()
    requirements.extend(reqs.strip().split("\n"))

external_deps = []

if __name__ == "__main__":
    setup(
        name="frogger",
        version="2",
        description="FAIR Dataset Registration Logger",
        long_description=readme,
        python_requires=">=3.9",
        packages=find_packages(),
        install_requires=external_deps + requirements,
        include_package_data=True,
    )
