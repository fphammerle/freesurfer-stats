"""
freesurfer-stats, a Python Library to Read FreeSurfer's Cortical Parcellation Anatomical Statistics
Copyright (C) 2019 Fabian Peter Hammerle <fabian@hammerle.me>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import os

import setuptools

with open("README.rst", "r") as readme:
    LONG_DESCRIPTION = readme.read()

setuptools.setup(
    name="freesurfer-stats",
    use_scm_version={
        "write_to": os.path.join("freesurfer_stats", "version.py"),
        # `version` triggers pylint C0103
        "write_to_template": "__version__ = '{version}'\n",
    },
    description="Python Library to Read FreeSurfer's cortical parcellation anatomical statistics",
    long_description=LONG_DESCRIPTION,
    author="Fabian Peter Hammerle",
    author_email="fabian@hammerle.me",
    url="https://github.com/fphammerle/freesurfer-stats",
    license="GPLv3+",
    keywords=[
        "anatomy",
        "aparc",
        "area",
        "brain",
        "cortex",
        "dataframe",
        "freesurfer",
        "mris_anatomical_stats",
        "neuroimaging",
        "pandas",
        "parcellation",
        "reader",
        "statistics",
        "surface",
        "volume",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Utilities",
    ],
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy<2",
        # pandas v1.2.0 made `get_filepath_or_buffer` private without releasing major version.
        # semver?!? not even mentioned in changelog
        # https://pandas.pydata.org/pandas-docs/stable/whatsnew/v1.2.0.html
        # https://github.com/pandas-dev/pandas/commit/6d1541e1782a7b94797d5432922e64a97934cfa4#diff-934d8564d648e7521db673c6399dcac98e45adfd5230ba47d3aabfcc21979febL247
        # TODO verify lower version constraint
        "pandas>=0.21,<1.2",
    ],
    setup_requires=["setuptools_scm"],
    tests_require=["pytest<5"],
)
