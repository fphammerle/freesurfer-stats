import datetime
import os

from conftest import SUBJECTS_DIR
from freesurfer_stats import CorticalParcellationStats


def test_read_dktatlas():
    stats = CorticalParcellationStats.read(os.path.join(
        SUBJECTS_DIR, 'fabian', 'stats', 'lh.aparc.DKTatlas.stats'))
    assert stats.creation_time == datetime.datetime(
        2019, 5, 9, 21, 5, 54, tzinfo=datetime.timezone.utc)
    assert stats.generating_program == 'mris_anatomical_stats'
    assert stats.cvs_version == 'Id: mris_anatomical_stats.c,v 1.79 2016/03/14 15:15:34 greve Exp'
    assert stats.mrisurf_ccvs_version \
        == 'Id: mrisurf.c,v 1.781.2.6 2016/12/27 16:47:14 zkaufman Exp'
    assert stats.cmdline == 'mris_anatomical_stats -th3 -mgz -cortex ../label/lh.cortex.label' \
        ' -f ../stats/lh.aparc.DKTatlas.stats -b -a ../label/lh.aparc.DKTatlas.annot' \
        ' -c ../label/aparc.annot.DKTatlas.ctab fabian lh white'
    assert stats.sysname == 'Linux'
    assert stats.hostname == 'another-hostname'
    assert stats.machine == 'x86_64'
    assert stats.user == 'some-username'
    assert stats.subjects_dir == '/home/some-username/freesurfer-subjects'
    assert stats.anatomy_type == 'surface'
    assert stats.subject_name == 'fabian'
    assert stats.hemisphere == 'left'
    assert stats.annotation_file == '../label/lh.aparc.DKTatlas.annot'
    assert stats.annotation_file_timestamp \
        == datetime.datetime(2019, 5, 9, 23, 5, 40)


def test_read_pial():
    stats = CorticalParcellationStats.read(os.path.join(
        SUBJECTS_DIR, 'fabian', 'stats', 'rh.aparc.pial.stats'))
    assert stats.creation_time == datetime.datetime(
        2019, 5, 9, 21, 3, 42, tzinfo=datetime.timezone.utc)
    assert stats.generating_program == 'mris_anatomical_stats'
    assert stats.cvs_version == 'Id: mris_anatomical_stats.c,v 1.79 2016/03/14 15:15:34 greve Exp'
    assert stats.mrisurf_ccvs_version \
        == 'Id: mrisurf.c,v 1.781.2.6 2016/12/27 16:47:14 zkaufman Exp'
    assert stats.cmdline == 'mris_anatomical_stats -th3 -mgz -cortex ../label/rh.cortex.label' \
        ' -f ../stats/rh.aparc.pial.stats -b -a ../label/rh.aparc.annot' \
        ' -c ../label/aparc.annot.ctab fabian rh pial'
    assert stats.sysname == 'Linux'
    assert stats.hostname == 'some-hostname'
    assert stats.machine == 'x86_64'
    assert stats.user == 'some-username'
    assert stats.subjects_dir == '/home/some-username/freesurfer-subjects'
    assert stats.anatomy_type == 'surface'
    assert stats.subject_name == 'fabian'
    assert stats.hemisphere == 'right'
    assert stats.annotation_file == '../label/rh.aparc.annot'
    assert stats.annotation_file_timestamp \
        == datetime.datetime(2019, 5, 9, 22, 27, 28)
