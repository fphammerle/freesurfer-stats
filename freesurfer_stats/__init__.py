"""
Python Library to Read FreeSurfer's cortical parcellation anatomical statistics
([lh]h.aparc(.*)?.stats)

Freesurfer
https://surfer.nmr.mgh.harvard.edu/

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
"""

import datetime
import re
import typing

import pandas

from freesurfer_stats.version import __version__


class CorticalParcellationStats:

    _HEMISPHERE_PREFIX_TO_SIDE = {'lh': 'left', 'rh': 'right'}

    def __init__(self):
        # type: typing.Dict[str, typing.Union[str, datetime.datetime]]
        self.headers = {}

    @property
    def hemisphere(self) -> str:
        return self._HEMISPHERE_PREFIX_TO_SIDE[self.headers['hemi']]

    def _read_headers(self, stream: typing.TextIO) -> None:
        self.headers = {}
        while True:
            line = stream.readline().rstrip()
            if line.startswith('# Measure'):
                break
            elif line != '#':
                prefix, attr_name, attr_value = line.split(' ', maxsplit=2)
                assert prefix == '#'
                attr_value = attr_value.lstrip()
                if attr_name in ['cvs_version', 'mrisurf.c-cvs_version']:
                    attr_value = attr_value.strip('$').rstrip()
                if attr_name == 'CreationTime':
                    attr_dt = datetime.datetime.strptime(
                        attr_value, '%Y/%m/%d-%H:%M:%S-%Z')
                    if attr_dt.tzinfo is None:
                        assert attr_value.endswith('-GMT')
                        attr_dt = attr_dt.replace(tzinfo=datetime.timezone.utc)
                    attr_value = attr_dt
                if attr_name == 'AnnotationFileTimeStamp':
                    attr_value = datetime.datetime.strptime(
                        attr_value, '%Y/%m/%d %H:%M:%S')
                self.headers[attr_name] = attr_value

    def _read(self, stream: typing.TextIO) -> None:
        assert stream.readline().rstrip() \
            == '# Table of FreeSurfer cortical parcellation anatomical statistics'
        assert stream.readline().rstrip() == '#'
        self._read_headers(stream)

    @classmethod
    def read(cls, path: str) -> 'CorticalParcellationStats':
        stats = cls()
        with open(path, 'r') as stream:
            # pylint: disable=protected-access
            stats._read(stream)
        return stats
