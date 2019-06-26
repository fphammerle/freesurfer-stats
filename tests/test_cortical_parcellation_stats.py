import datetime
import os

import pytest

from conftest import SUBJECTS_DIR
from freesurfer_stats import CorticalParcellationStats


@pytest.mark.parametrize(('path', 'headers', 'hemisphere', 'general_measurements'), [
    (os.path.join(SUBJECTS_DIR, 'fabian', 'stats', 'lh.aparc.DKTatlas.stats'),
     {'CreationTime': datetime.datetime(2019, 5, 9, 21, 5, 54, tzinfo=datetime.timezone.utc),
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
      'AnnotationFileTimeStamp': datetime.datetime(2019, 5, 9, 23, 5, 40)},
     'left',
     {'White Surface Total Area': (98553, 'mm^2'),
      'Mean Thickness': (2.50462, 'mm'),
      'Brain Segmentation Volume': (1327432.000000, 'mm^3'),
      'Brain Segmentation Volume Without Ventricles': (1316285.000000, 'mm^3'),
      'Brain Segmentation Volume Without Ventricles from Surf': (1315572.548920, 'mm^3'),
      'Total cortical gray matter volume': (553998.311189, 'mm^3'),
      'Supratentorial volume': (1172669.548920, 'mm^3'),
      'Supratentorial volume Without Ventricles': (1164180.548920, 'mm^3'),
      'Estimated Total Intracranial Volume': (1670487.274486, 'mm^3')}),
    (os.path.join(
        SUBJECTS_DIR, 'fabian', 'stats', 'rh.aparc.pial.stats'),
     {'CreationTime': datetime.datetime(2019, 5, 9, 21, 3, 42, tzinfo=datetime.timezone.utc),
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
      'AnnotationFileTimeStamp': datetime.datetime(2019, 5, 9, 22, 27, 28)},
     'right',
     {'Pial Surface Total Area': (121260, 'mm^2'),
      'Mean Thickness': (2.4817, 'mm'),
      'Brain Segmentation Volume': (1327432.000000, 'mm^3'),
      'Brain Segmentation Volume Without Ventricles': (1316285.000000, 'mm^3'),
      'Brain Segmentation Volume Without Ventricles from Surf': (1315572.548920, 'mm^3'),
      'Total cortical gray matter volume': (553998.311189, 'mm^3'),
      'Supratentorial volume': (1172669.548920, 'mm^3'),
      'Supratentorial volume Without Ventricles': (1164180.548920, 'mm^3'),
      'Estimated Total Intracranial Volume': (1670487.274486, 'mm^3')}),
])
def test_read(path, headers, hemisphere, general_measurements):
    stats = CorticalParcellationStats.read(path)
    assert headers == stats.headers
    assert hemisphere == stats.hemisphere
    assert general_measurements.keys() == stats.general_measurements.keys()
    for key, expected_value_unit in general_measurements.items():
        expected_value, expected_unit = expected_value_unit
        assert expected_value \
            == pytest.approx(stats.general_measurements[key][0])
        assert expected_unit == stats.general_measurements[key][1]
