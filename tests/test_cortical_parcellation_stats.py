import datetime
import os

import pytest

from conftest import SUBJECTS_DIR, assert_approx_equal
from freesurfer_stats import CorticalParcellationStats


@pytest.mark.parametrize(
    ('path', 'headers', 'hemisphere',
     'whole_brain_measurements', 'structure_measurements'),
    [(os.path.join(SUBJECTS_DIR, 'fabian', 'stats', 'lh.aparc.DKTatlas.stats.short'),
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
       'Estimated Total Intracranial Volume': (1670487.274486, 'mm^3')},
      {'caudalanteriorcingulate': {
          'Structure Name': 'caudalanteriorcingulate',
          'Number of Vertices': 2061,
          'Surface Area': 1472.0,
          'Gray Matter Volume': 4258.0,
          'Average Thickness': 2.653,
          'Thickness StdDev': 0.644,
          'Integrated Rectified Mean Curvature': 0.135,
          'Integrated Rectified Gaussian Curvature': 0.020,
          'Folding Index': 27,
          'Intrinsic Curvature Index': 1.6},
       'caudalmiddlefrontal': {
           'Structure Name': 'caudalmiddlefrontal',
           'Number of Vertices': 4451,
           'Surface Area': 3039.0,
           'Gray Matter Volume': 8239.0,
           'Average Thickness': 2.456,
           'Thickness StdDev': 0.486,
           'Integrated Rectified Mean Curvature': 0.116,
           'Integrated Rectified Gaussian Curvature': 0.020,
           'Folding Index': 42,
           'Intrinsic Curvature Index': 3.7},
       'insula': {
           'Structure Name': 'insula',
           'Number of Vertices': 3439,
           'Surface Area': 2304.0,
           'Gray Matter Volume': 7594.0,
           'Average Thickness': 3.193,
           'Thickness StdDev': 0.620,
           'Integrated Rectified Mean Curvature': 0.116,
           'Integrated Rectified Gaussian Curvature': 0.027,
           'Folding Index': 33,
           'Intrinsic Curvature Index': 3.5}}),
     (os.path.join(
         SUBJECTS_DIR, 'fabian', 'stats', 'rh.aparc.pial.stats.short'),
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
       'Estimated Total Intracranial Volume': (1670487.274486, 'mm^3')},
      {'bankssts': {
          'Structure Name': 'bankssts',
          'Number of Vertices': 1344,
          'Surface Area': 825.0,
          'Gray Matter Volume': 2171.0,
          'Average Thickness': 2.436,
          'Thickness StdDev': 0.381,
          'Integrated Rectified Mean Curvature': 0.115,
          'Integrated Rectified Gaussian Curvature': 0.028,
          'Folding Index': 19,
          'Intrinsic Curvature Index': 1.7},
       'transversetemporal': {
           'Structure Name': 'transversetemporal',
           'Number of Vertices': 651,
           'Surface Area': 545.0,
           'Gray Matter Volume': 1061.0,
           'Average Thickness': 2.251,
           'Thickness StdDev': 0.317,
           'Integrated Rectified Mean Curvature': 0.110,
           'Integrated Rectified Gaussian Curvature': 0.021,
           'Folding Index': 3,
           'Intrinsic Curvature Index': 0.6}})],
)
def test_read(path, headers, hemisphere, whole_brain_measurements, structure_measurements):
    stats = CorticalParcellationStats.read(path)
    assert headers == stats.headers
    assert hemisphere == stats.hemisphere
    assert_approx_equal(whole_brain_measurements,
                        stats.whole_brain_measurements)
    assert stats.structure_measurement_units == {
        'Structure Name': None,
        'Number of Vertices': None,
        'Surface Area': 'mm^2',
        'Gray Matter Volume': 'mm^3',
        'Average Thickness': 'mm',
        'Thickness StdDev': 'mm',
        'Integrated Rectified Mean Curvature': 'mm^-1',
        'Integrated Rectified Gaussian Curvature': 'mm^-2',
        'Folding Index': None,
        'Intrinsic Curvature Index': None,
    }
    assert_approx_equal(structure_measurements, stats.structure_measurements)
