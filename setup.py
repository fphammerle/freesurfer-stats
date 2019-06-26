import os

import setuptools

with open('README.rst', 'r') as readme:
    LONG_DESCRIPTION = readme.read()

setuptools.setup(
    name='freesurfer-stats',
    use_scm_version={
        'write_to': os.path.join('freesurfer_stats', 'version.py'),
        # `version` triggers pylint C0103
        'write_to_template': "__version__ = '{version}'\n",
    },
    description="Python Library to Read FreeSurfer's cortical parcellation anatomical statistics",
    long_description=LONG_DESCRIPTION,
    author='Fabian Peter Hammerle',
    author_email='fabian@hammerle.me',
    url='https://github.com/fphammerle/freesurfer-stats',
    # TODO add license
    keywords=[
        'anatomy',
        'aparc',
        'area',
        'brain',
        'cortex',
        'dataframe',
        'freesurfer',
        'mris_anatomical_stats',
        'neuroimaging',
        'pandas',
        'parcellation',
        'reader',
        'statistics',
        'surface',
        'volume',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Utilities',
    ],
    packages=setuptools.find_packages(),
    install_requires=[
        # TODO add lower version constraint
        'pandas<1',
    ],
    setup_requires=[
        'setuptools_scm',
    ],
    tests_require=[
        'pylint>=2.3.0,<3',
        'pytest-cov<3,>=2',
        'pytest-timeout<2',
        'pytest<5',
    ],
)
