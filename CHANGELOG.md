# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2020-05-30
### Added
- `CorticalParcellationStats.read` support `pathlib.Path`, `"http://…"`, `"https://…"`, `"s3://…"` etc.
  via `pandas.io.common.get_filepath_or_buffer`
  (https://github.com/fphammerle/freesurfer-stats/issues/6)

## [1.1.1] - 2020-05-07
### Fixed
- fixed parsing of `BrainVolStatsFixed` header
  (https://github.com/fphammerle/freesurfer-stats/pull/1 @soichih,
  https://github.com/fphammerle/freesurfer-stats/pull/9)

## [1.1.0] - 2020-05-06
### Added
- compatibility with pandas v1

## [1.0.0] - 2019-06-27

[Unreleased]: https://github.com/fphammerle/freesurfer-stats/compare/1.2.0...HEAD
[1.2.0]: https://github.com/fphammerle/freesurfer-stats/compare/1.1.1...1.2.0
[1.1.1]: https://github.com/fphammerle/freesurfer-stats/compare/1.1.0...1.1.1
[1.1.0]: https://github.com/fphammerle/freesurfer-stats/compare/1.0.0...1.1.0
[1.0.0]: https://github.com/fphammerle/freesurfer-stats/tree/1.0.0
