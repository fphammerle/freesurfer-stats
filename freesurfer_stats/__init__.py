"""
Python Library to Read FreeSurfer's Cortical Parcellation Anatomical Statistics
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

import datetime
import io
import pathlib
import re
import typing

import numpy
import pandas

from freesurfer_stats.version import __version__


def _get_filepath_or_buffer(
    path: typing.Union[str, pathlib.Path]
) -> typing.Tuple[
    typing.Any, bool  # pandas._typing.FileOrBuffer, bool)
]:  # pragma: no cover
    # can't check coverage due to pandas version branching.
    # pipeline tests against multiple pandas versions.
    if not hasattr(pandas.io.common, "get_filepath_or_buffer"):
        # pandas.io.common.get_filepath_or_buffer was made private in v1.2.0:
        # https://github.com/pandas-dev/pandas/commit/6d1541e1782a7b94797d5432922e64a97934cfa4#diff-934d8564d648e7521db673c6399dcac98e45adfd5230ba47d3aabfcc21979febL247
        # semver?!? breaking change not even mentioned in changelog:
        # https://pandas.pydata.org/pandas-docs/stable/whatsnew/v1.2.0.html
        # new wrapper: get_handle
        # https://github.com/pandas-dev/pandas/blob/v1.2.0/pandas/io/common.py#L490
        # pandas v1.1's get_handle does not yet support urls
        # pylint: disable=no-member; for python<v1.2.0
        io_handle = pandas.io.common.get_handle(path, "r")
        return io_handle.handle, True
    # path_or_buffer: typing.Union[str, pathlib.Path, typing.IO[typing.AnyStr],
    #                              s3fs.S3File, gcsfs.GCSFile]
    # https://github.com/pandas-dev/pandas/blob/v0.25.3/pandas/io/parsers.py#L436
    # https://github.com/pandas-dev/pandas/blob/v0.25.3/pandas/_typing.py#L30
    # pylint: disable=no-member; for python>=v1.2.0
    (path_or_buffer, _, _, *instructions) = pandas.io.common.get_filepath_or_buffer(
        path
    )
    if instructions:
        # https://github.com/pandas-dev/pandas/blob/v0.25.3/pandas/io/common.py#L171
        assert len(instructions) == 1, instructions
        should_close = instructions[0]
    else:
        # https://github.com/pandas-dev/pandas/blob/v0.21.0/pandas/io/common.py#L171
        should_close = hasattr(path_or_buffer, "close")
    return path_or_buffer, should_close


class CorticalParcellationStats:

    _HEMISPHERE_PREFIX_TO_SIDE = {"lh": "left", "rh": "right"}
    _GENERAL_MEASUREMENTS_REGEX = re.compile(
        r"^Measure \S+, ([^,\s]+),? ([^,]+), ([\d\.]+), (\S+)$"
    )
    _COLUMN_NAMES_NON_SAFE_REGEX = re.compile(r"\s+")

    def __init__(self):
        self.headers = (
            {}
        )  # type: typing.Dict[str, typing.Union[str, datetime.datetime]]
        self.whole_brain_measurements = (
            {}
        )  # type: typing.Dict[str, typing.Tuple[float, int]]
        self.structural_measurements = {}  # type: typing.Union[pandas.DataFrame, None]

    @property
    def hemisphere(self) -> str:
        return self._HEMISPHERE_PREFIX_TO_SIDE[typing.cast(str, self.headers["hemi"])]

    @staticmethod
    def _read_header_line(stream: typing.TextIO) -> str:
        line = stream.readline()
        assert line.startswith("# ")
        return line[2:].rstrip()

    @classmethod
    def _read_column_header_line(
        cls, stream: typing.TextIO
    ) -> typing.Tuple[int, str, str]:
        line = cls._read_header_line(stream)
        assert line.startswith("TableCol"), line
        line = line[len("TableCol ") :].lstrip()
        index, key, value = line.split(maxsplit=2)
        return int(index), key, value

    def _read_headers(self, stream: typing.TextIO) -> None:
        self.headers = {}
        while True:
            line = self._read_header_line(stream)
            if line.startswith("Measure"):
                break
            if line:
                attr_name, attr_value_str = line.split(" ", maxsplit=1)
                attr_value_str = attr_value_str.lstrip()
                if attr_name in ["cvs_version", "mrisurf.c-cvs_version"]:
                    attr_value = typing.cast(
                        typing.Union[str, datetime.datetime],
                        attr_value_str.strip("$").rstrip(),
                    )
                elif attr_name == "CreationTime":
                    attr_dt = datetime.datetime.strptime(
                        attr_value_str, "%Y/%m/%d-%H:%M:%S-%Z"
                    )
                    if attr_dt.tzinfo is None:
                        assert attr_value_str.endswith("-GMT")
                        attr_dt = attr_dt.replace(tzinfo=datetime.timezone.utc)
                    attr_value = attr_dt
                elif attr_name == "AnnotationFileTimeStamp":
                    attr_value = datetime.datetime.strptime(
                        attr_value_str, "%Y/%m/%d %H:%M:%S"
                    )
                else:
                    attr_value = attr_value_str
                self.headers[attr_name] = attr_value

    @classmethod
    def _format_column_name(cls, name: str, unit: str) -> str:
        column_name = name.lower()
        if unit not in ["unitless", "NA"]:
            column_name += "_" + unit
        return cls._COLUMN_NAMES_NON_SAFE_REGEX.sub("_", column_name)

    @classmethod
    def _parse_whole_brain_measurements_line(
        cls, line: str
    ) -> typing.Tuple[str, numpy.ndarray]:
        match = cls._GENERAL_MEASUREMENTS_REGEX.match(line)
        if not match:
            raise ValueError("unexpected line: {!r}".format(line))
        key, name, value, unit = match.groups()
        if (
            key == "SupraTentorialVolNotVent"
            and name.lower() == "supratentorial volume"
        ):
            name += " Without Ventricles"
        column_name = cls._format_column_name(name, unit)
        return column_name, pandas.to_numeric([value], errors="raise")

    @classmethod
    def _read_column_attributes(
        cls, num: int, stream: typing.TextIO
    ) -> typing.List[typing.Dict[str, str]]:
        columns = []
        for column_index in range(1, int(num) + 1):
            column_attrs = {}  # type: typing.Dict[str, str]
            for _ in range(3):
                column_index_line, key, value = cls._read_column_header_line(stream)
                assert column_index_line == column_index
                assert key not in column_attrs
                column_attrs[key] = value
            columns.append(column_attrs)
        return columns

    def _read(self, stream: typing.TextIO) -> None:
        assert (
            stream.readline().rstrip()
            == "# Table of FreeSurfer cortical parcellation anatomical statistics"
        )
        assert stream.readline().rstrip() == "#"
        self._read_headers(stream)
        self.whole_brain_measurements = pandas.DataFrame()
        line = self._read_header_line(stream)
        while not line.startswith("NTableCols"):
            if line.startswith("BrainVolStatsFixed"):
                # https://surfer.nmr.mgh.harvard.edu/fswiki/BrainVolStatsFixed
                assert (
                    line.startswith("BrainVolStatsFixed see ")
                    or line == "BrainVolStatsFixed-NotNeeded because voxelvolume=1mm3"
                )
                self.headers["BrainVolStatsFixed"] = line[len("BrainVolStatsFixed-") :]
            else:
                column_name, value = self._parse_whole_brain_measurements_line(line)
                assert column_name not in self.whole_brain_measurements, column_name
                self.whole_brain_measurements[column_name] = value
            line = self._read_header_line(stream)
        columns = self._read_column_attributes(int(line[len("NTableCols ") :]), stream)
        assert self._read_header_line(stream) == "ColHeaders " + " ".join(
            c["ColHeader"] for c in columns
        )
        self.structural_measurements = pandas.DataFrame(
            (line.rstrip().split() for line in stream),
            columns=[
                self._format_column_name(c["FieldName"], c["Units"]) for c in columns
            ],
        ).apply(pandas.to_numeric, errors="ignore")

    @classmethod
    def read(cls, path: typing.Union[str, pathlib.Path]) -> "CorticalParcellationStats":
        path_or_buffer, should_close = _get_filepath_or_buffer(path)
        stats = cls()
        try:  # pragma: no cover
            # can't check coverage due to pandas version branching.
            # pylint: disable=protected-access; false-positive for ._read
            if isinstance(path_or_buffer, io.TextIOWrapper):  # pandas>=v1.2.0
                stats._read(path_or_buffer)
            elif hasattr(path_or_buffer, "readline"):
                stats._read(io.TextIOWrapper(path_or_buffer))
            else:
                with open(path_or_buffer, "r") as stream:
                    stats._read(stream)
        finally:
            if should_close:
                path_or_buffer.close()
        return stats
