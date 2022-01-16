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
    packages=setuptools.find_packages(),
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
        # .github/workflows/python.yml
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Utilities",
    ],
    # >=3.6 f-strings & variable type hints
    # >=3.7 postponed evaluation of type annotations (PEP563)
    python_requires=">=3.7",
    install_requires=[
        "numpy<2",
        # still hoping that pandas will stick to semantic versioning in the future
        # <0.23 untested
        "pandas>=0.23,<2",
    ],
    setup_requires=["setuptools_scm"],
    tests_require=["pytest<5"],
)
