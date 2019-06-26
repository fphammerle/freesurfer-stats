import datetime
import os

from conftest import SUBJECTS_DIR
from freesurfer_stats import CorticalParcellationStats


def test_read_dktatlas():
    stats = CorticalParcellationStats.read(os.path.join(
        SUBJECTS_DIR, 'fabian', 'stats', 'lh.aparc.DKTatlas.stats'))
    assert stats.headers == {
        'CreationTime': datetime.datetime(2019, 5, 9, 21, 5, 54, tzinfo=datetime.timezone.utc),
        'generating_program': 'mris_anatomical_stats',
        'cvs_version': 'Id: mris_anatomical_stats.c,v 1.79 2016/03/14 15:15:34 greve Exp',
        'mrisurf.c-cvs_version': 'Id: mrisurf.c,v 1.781.2.6 2016/12/27 16:47:14 zkaufman Exp',
        'cmdline': 'mris_anatomical_stats -th3 -mgz -cortex ../label/lh.cortex.label'
                   ' -f ../stats/lh.aparc.DKTatlas.stats -b -a ../label/lh.aparc.DKTatlas.annot'
                   ' -c ../label/aparc.annot.DKTatlas.ctab fabian lh white',
        'sysname': 'Linux',
        'hostname': 'another-hostname',
        'machine': 'x86_64',
        'user': 'some-username',
        'SUBJECTS_DIR': '/home/some-username/freesurfer-subjects',
        'anatomy_type': 'surface',
        'subjectname': 'fabian',
        'hemi': 'lh',
        'AnnotationFile': '../label/lh.aparc.DKTatlas.annot',
        'AnnotationFileTimeStamp': datetime.datetime(2019, 5, 9, 23, 5, 40),
    }
    assert stats.hemisphere == 'left'


def test_read_pial():
    stats = CorticalParcellationStats.read(os.path.join(
        SUBJECTS_DIR, 'fabian', 'stats', 'rh.aparc.pial.stats'))
    assert stats.headers == {
        'CreationTime': datetime.datetime(2019, 5, 9, 21, 3, 42, tzinfo=datetime.timezone.utc),
        'generating_program': 'mris_anatomical_stats',
        'cvs_version': 'Id: mris_anatomical_stats.c,v 1.79 2016/03/14 15:15:34 greve Exp',
        'mrisurf.c-cvs_version': 'Id: mrisurf.c,v 1.781.2.6 2016/12/27 16:47:14 zkaufman Exp',
        'cmdline': 'mris_anatomical_stats -th3 -mgz -cortex ../label/rh.cortex.label'
                   ' -f ../stats/rh.aparc.pial.stats -b -a ../label/rh.aparc.annot'
                   ' -c ../label/aparc.annot.ctab fabian rh pial',
        'sysname': 'Linux',
        'hostname': 'some-hostname',
        'machine': 'x86_64',
        'user': 'some-username',
        'SUBJECTS_DIR': '/home/some-username/freesurfer-subjects',
        'anatomy_type': 'surface',
        'subjectname': 'fabian',
        'hemi': 'rh',
        'AnnotationFile': '../label/rh.aparc.annot',
        'AnnotationFileTimeStamp': datetime.datetime(2019, 5, 9, 22, 27, 28),
    }
    assert stats.hemisphere == 'right'
