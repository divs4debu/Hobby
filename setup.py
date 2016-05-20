#!/usr/bin/env python
import os.path
from setuptools import setup, find_packages


def auto_version_setup(**kwargs):
    pkg_name = kwargs["packages"][0]

    # Populate the "version" argument from the "VERSION" file.
    pkg_path = os.path.join(os.path.dirname(__file__), pkg_name)
    with open(os.path.join(pkg_path, "VERSION"), "r") as handle:
        pkg_version = handle.read().strip()
    kwargs["version"] = pkg_version

    # Make sure the "VERSION" file is included when we build the package.
    package_data = kwargs.setdefault("package_data", {})
    this_pkg_data = package_data.setdefault(pkg_name, [])
    if "VERSION" not in this_pkg_data:
        this_pkg_data.append("VERSION")

    setup(**kwargs)


auto_version_setup(
    name="tube",
    description="Download youtube clips",
    packages=find_packages(),
    package_data={
        "tube": [
            "VERSION",
        ],
    },
    install_requires=[
        "bs4",
        "lxml",
        "pytube",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            'tube = tube.tube:run',
        ],
    },
)
