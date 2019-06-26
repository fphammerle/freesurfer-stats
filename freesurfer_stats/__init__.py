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
>>> stats.whole_brain_measurements['Estimated Total Intracranial Volume']
(1670487.274486, 'mm^3')
>>> stats.whole_brain_measurements['White Surface Total Area']
(98553.0, 'mm^2')
>>> stats.structure_measurements[['Structure Name', 'Surface Area (mm^2)', 'Gray Matter Volume (mm^3)']].head()
            Structure Name  Surface Area (mm^2)  Gray Matter Volume (mm^3)
0  caudalanteriorcingulate                 1472                       4258
1      caudalmiddlefrontal                 3039                       8239
2                   cuneus                 2597                       6722
3               entorhinal                  499                       2379
4                 fusiform                 3079                       9064
"""

import datetime
import re
import typing

import pandas

from freesurfer_stats.version import __version__


class CorticalParcellationStats:

    _HEMISPHERE_PREFIX_TO_SIDE = {'lh': 'left', 'rh': 'right'}
    _GENERAL_MEASUREMENTS_REGEX = re.compile(
        r'^Measure \S+, ([^,\s]+),? ([^,]+), ([\d\.]+), (\S+)$')

    def __init__(self):
        self.headers \
            = {}  # type: typing.Dict[str, typing.Union[str, datetime.datetime]]
        self.whole_brain_measurements \
            = {}  # type: typing.Dict[str, typing.Tuple[float, int]]
        self.structure_measurements \
            = {}  # type: typing.Union[pandas.DataFrame, None]

    @property
    def hemisphere(self) -> str:
        return self._HEMISPHERE_PREFIX_TO_SIDE[self.headers['hemi']]

    @staticmethod
    def _read_header_line(stream: typing.TextIO) -> str:
        line = stream.readline()
        assert line.startswith('# ')
        return line[2:].rstrip()

    @classmethod
    def _read_column_header_line(cls, stream: typing.TextIO) -> typing.Tuple[int, str, str]:
        line = cls._read_header_line(stream)
        assert line.startswith('TableCol'), line
        line = line[len('TableCol '):].lstrip()
        index, key, value = line.split(maxsplit=2)
        return int(index), key, value

    def _read_headers(self, stream: typing.TextIO) -> None:
        self.headers = {}
        while True:
            line = self._read_header_line(stream)
            if line.startswith('Measure'):
                break
            elif line:
                attr_name, attr_value = line.split(' ', maxsplit=1)
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

    @staticmethod
    def _format_column_name(column_attrs: typing.Dict[str, str]) -> str:
        name = column_attrs['FieldName']
        unit = column_attrs['Units']
        if unit in ['unitless', 'NA']:
            return name
        return '{} ({})'.format(name, unit)

    @classmethod
    def _read_column_attributes(cls, num: int, stream: typing.TextIO) \
            -> typing.List[typing.Dict[str, str]]:
        columns = []
        for column_index in range(1, int(num) + 1):
            column_attrs = {}
            for _ in range(3):
                column_index_line, key, value \
                    = cls._read_column_header_line(stream)
                assert column_index_line == column_index
                assert key not in column_attrs
                column_attrs[key] = value
            columns.append(column_attrs)
        return columns

    def _read(self, stream: typing.TextIO) -> None:
        assert stream.readline().rstrip() \
            == '# Table of FreeSurfer cortical parcellation anatomical statistics'
        assert stream.readline().rstrip() == '#'
        self._read_headers(stream)
        self.whole_brain_measurements = {}
        line = self._read_header_line(stream)
        while not line.startswith('NTableCols'):
            key, name, value, unit \
                = self._GENERAL_MEASUREMENTS_REGEX.match(line).groups()
            if key == 'SupraTentorialVolNotVent' and name.lower() == 'supratentorial volume':
                name += ' Without Ventricles'
            assert name not in self.whole_brain_measurements, \
                (key, name, self.whole_brain_measurements)
            self.whole_brain_measurements[name] = (float(value), unit)
            line = self._read_header_line(stream)
        columns = self._read_column_attributes(
            int(line[len('NTableCols '):]), stream)
        assert self._read_header_line(stream) \
            == 'ColHeaders ' + ' '.join(c['ColHeader'] for c in columns)
        self.structure_measurements = pandas.DataFrame(
            (line.rstrip().split() for line in stream),
            columns=list(map(self._format_column_name, columns))) \
            .apply(pandas.to_numeric, errors='ignore')

    @classmethod
    def read(cls, path: str) -> 'CorticalParcellationStats':
        stats = cls()
        with open(path, 'r') as stream:
            # pylint: disable=protected-access
            stats._read(stream)
        return stats
