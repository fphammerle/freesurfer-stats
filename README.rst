freesurfer-stats
================

TODO add badges

Python Library to Read FreeSurfer's cortical parcellation anatomical statistics

Freesurfer https://surfer.nmr.mgh.harvard.edu/

Install
-------

.. code:: sh

    pip3 install --user freesurfer-stats

Releases follow the `semantic versioning <https://semver.org/>` scheme.

Usage
-----

.. code:: python

    >>> from freesurfer_stats import CorticalParcellationStats
    >>> stats = CorticalParcellationStats.read('tests/subjects/fabian/stats/lh.aparc.DKTatlas.stats')
    >>> stats.headers['CreationTime'].isoformat()
    '2019-05-09T21:05:54+00:00'
    >>> stats.headers['cvs_version']
    'Id: mris_anatomical_stats.c,v 1.79 2016/03/14 15:15:34 greve Exp'
    >>> stats.headers['cmdline'][:64]
    'mris_anatomical_stats -th3 -mgz -cortex ../label/lh.cortex.label'
    >>> stats.hemisphere
    'left'
