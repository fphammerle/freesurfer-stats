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
    >>> stats.whole_brain_measurements['Estimated Total Intracranial Volume']
    (1670487.274486, 'mm^3')
    >>> stats.whole_brain_measurements['White Surface Total Area']
    (98553.0, 'mm^2')
    >>> stats.structure_measurements['postcentral']
    {'Structure Name': 'postcentral',
     'Number of Vertices': 8102,
     'Surface Area': 5258.0,
     'Gray Matter Volume': 12037.0,
     'Average Thickness': 2.109,
     'Thickness StdDev': 0.568,
     ...}
    >>> stats.structure_measurement_units
    {'Structure Name': None,
     'Number of Vertices': None,
     'Surface Area': 'mm^2',
     'Gray Matter Volume': 'mm^3',
     'Average Thickness': 'mm',
     'Thickness StdDev': 'mm',
     ...}
