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
            = {}  # type: typing.Dict[str, typing.Dict[str, typing.Union[str, int, float]]]
        self.structure_measurement_units \
            = {}  # type: typing.Dict[str, typing.Union[str, None]]

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
    def _filter_unit(unit: str) -> typing.Union[str, None]:
        if unit in ['unitless', 'NA']:
            return None
        return unit

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
        assert columns[0]['ColHeader'] == 'StructName'
        column_names = [c['FieldName'] for c in columns]
        self.structure_measurements = {}
        for line in stream:
            values = line.rstrip().split()
            assert len(values) == len(column_names)
            struct_name = values[0]
            assert struct_name not in self.structure_measurements
            for column_index, column_attrs in enumerate(columns):
                if column_attrs['ColHeader'] in ['NumVert', 'FoldInd']:
                    values[column_index] = int(values[column_index])
                elif column_attrs['ColHeader'] != 'StructName':
                    values[column_index] = float(values[column_index])
            self.structure_measurements[struct_name] \
                = dict(zip(column_names, values))
        self.structure_measurement_units = {
            c['FieldName']: self._filter_unit(c['Units']) for c in columns}

    @classmethod
    def read(cls, path: str) -> 'CorticalParcellationStats':
        stats = cls()
        with open(path, 'r') as stream:
            # pylint: disable=protected-access
            stats._read(stream)
        return stats
