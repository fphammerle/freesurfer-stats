"""
Python Library to Read FreeSurfer's cortical parcellation anatomical statistics
([lh]h.aparc(.*)?.stats)

Freesurfer
https://surfer.nmr.mgh.harvard.edu/

>>> stats = CorticalParcellationStats.read('tests/subjects/fabian/stats/lh.aparc.DKTatlas.stats')
>>> stats.creation_time.isoformat()
'2019-05-09T21:05:54+00:00'
>>> stats.cvs_version
'Id: mris_anatomical_stats.c,v 1.79 2016/03/14 15:15:34 greve Exp'
>>> stats.cmdline[:64]
'mris_anatomical_stats -th3 -mgz -cortex ../label/lh.cortex.label'
"""

import datetime
import re
import typing

import pandas

from freesurfer_stats.version import __version__


class CorticalParcellationStats:

    def __init__(self):
        self.creation_time = None  # type: typing.Optional[datetime.datetime]
        self.generating_program = None  # type: typing.Optional[str]
        self.cvs_version = None  # type: typing.Optional[str]
        self.mrisurf_ccvs_version = None  # type: typing.Optional[str]
        self.cmdline = None  # type: typing.Optional[str]
        self.sysname = None  # type: typing.Optional[str]
        self.hostname = None  # type: typing.Optional[str]
        self.machine = None  # type: typing.Optional[str]
        self.user = None  # type: typing.Optional[str]

    def _read_headers(self, stream: typing.TextIO) -> None:
        creation_time_str = stream.readline()[len('# CreationTime '):].rstrip()
        self.creation_time = datetime.datetime.strptime(
            creation_time_str, '%Y/%m/%d-%H:%M:%S-%Z')
        if self.creation_time.tzinfo is None:
            assert creation_time_str.endswith('-GMT')
            self.creation_time = self.creation_time.replace(
                tzinfo=datetime.timezone.utc)
        while True:
            line = stream.readline().rstrip()
            if line == '#':
                break
            prefix, attr_name, attr_value = line.split(' ', maxsplit=2)
            assert prefix == '#'
            attr_value = attr_value.lstrip()
            if attr_name == 'generating_program':
                self.generating_program = attr_value
            elif attr_name == 'cvs_version':
                self.cvs_version = attr_value.strip('$').rstrip()
            elif attr_name == 'mrisurf.c-cvs_version':
                self.mrisurf_ccvs_version = attr_value.strip('$').rstrip()
            elif attr_name == 'cmdline':
                self.cmdline = attr_value
            elif attr_name == 'sysname':
                self.sysname = attr_value
            elif attr_name == 'hostname':
                self.hostname = attr_value
            elif attr_name == 'machine':
                self.machine = attr_value
            elif attr_name == 'user':
                self.user = attr_value
            else:
                raise ValueError(attr_name)

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
