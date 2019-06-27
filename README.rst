freesurfer-stats
================

.. image:: https://travis-ci.org/fphammerle/freesurfer-stats.svg?branch=master
   :target: https://travis-ci.org/fphammerle/freesurfer-stats
.. image:: https://coveralls.io/repos/github/fphammerle/freesurfer-stats/badge.svg?branch=master
   :target: https://coveralls.io/github/fphammerle/freesurfer-stats?branch=master
.. image:: https://img.shields.io/pypi/v/freesurfer-stats.svg
   :target: https://pypi.org/project/freesurfer-stats/#history
.. image:: https://img.shields.io/pypi/pyversions/freesurfer-stats.svg
   :target: https://pypi.org/project/freesurfer-stats/
.. image:: https://zenodo.org/badge/194054168.svg
   :target: https://zenodo.org/badge/latestdoi/194054168

Python Library to Read FreeSurfer's Cortical Parcellation Anatomical Statistics
`subject/stats/[rl]h.aparc.*.stats`

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
    >>> stats.headers['subjectname']
    'fabian'
    >>> stats.headers['CreationTime'].isoformat()
    '2019-05-09T21:05:54+00:00'
    >>> stats.headers['cvs_version']
    'Id: mris_anatomical_stats.c,v 1.79 2016/03/14 15:15:34 greve Exp'
    >>> stats.headers['cmdline'][:64]
    'mris_anatomical_stats -th3 -mgz -cortex ../label/lh.cortex.label'
    >>> stats.hemisphere
    'left'
    >>> stats.whole_brain_measurements['estimated_total_intracranial_volume_mm^3']
    0    1.670487e+06
    Name: estimated_total_intracranial_volume_mm^3, dtype: float64
    >>> stats.whole_brain_measurements['white_surface_total_area_mm^2']
    0    98553
    Name: white_surface_total_area_mm^2, dtype: int64
    >>> stats.structural_measurements[['structure_name', 'surface_area_mm^2',
    ...                                'gray_matter_volume_mm^3']].head()
                structure_name  surface_area_mm^2  gray_matter_volume_mm^3
    0  caudalanteriorcingulate               1472                     4258
    1      caudalmiddlefrontal               3039                     8239
    2                   cuneus               2597                     6722
    3               entorhinal                499                     2379
    4                 fusiform               3079                     9064

Load Multiple Stats Files
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    >>> import glob, pandas
    >>> from freesurfer_stats import CorticalParcellationStats
    >>> def load_whole_brain_measurements(stats_path) -> pandas.DataFrame:
    ...     stats = CorticalParcellationStats.read(stats_path)
    ...     stats.whole_brain_measurements['subject'] = stats.headers['subjectname']
    ...     stats.whole_brain_measurements['source_basename'] = os.path.basename(stats_path)
    ...     stats.whole_brain_measurements['hemisphere'] = stats.hemisphere
    ...     return stats.whole_brain_measurements
    ...
    >>> whole_brain_measurements = pandas.concat(
    ...     map(load_whole_brain_measurements, glob.glob('tests/subjects/fabian/stats/*h.aparc*.stats')),
    ...     sort=False)
    >>> whole_brain_measurements.reset_index(drop=True, inplace=True)
    >>> whole_brain_measurements[['subject', 'source_basename', 'hemisphere',
    ...                           'white_surface_total_area_mm^2', 'pial_surface_total_area_mm^2']]
      subject          source_basename hemisphere  white_surface_total_area_mm^2  pial_surface_total_area_mm^2
    0  fabian  lh.aparc.DKTatlas.stats       left                        98553.0                           NaN
    1  fabian           rh.aparc.stats      right                        99468.9                           NaN
    2  fabian    rh.aparc.a2009s.stats      right                        99494.9                           NaN
    3  fabian  rh.aparc.DKTatlas.stats      right                        99494.9                           NaN
    4  fabian           lh.aparc.stats       left                        98536.5                           NaN
    5  fabian      lh.aparc.pial.stats       left                            NaN                      118601.0
    6  fabian      rh.aparc.pial.stats      right                            NaN                      121260.0
    7  fabian    lh.aparc.a2009s.stats       left                        98553.0                           NaN

Tests
-----

.. code:: sh

    pip3 install --user pipenv
    git clone https://github.com/fphammerle/freesurfer-stats.git
    cd freesurfer-stats
    pipenv sync --dev
    pipenv run pylint freesurfer_stats
    pipenv run pytest
