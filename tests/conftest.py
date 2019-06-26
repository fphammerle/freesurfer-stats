import os

import pytest

SUBJECTS_DIR = os.path.join(os.path.dirname(__file__), 'subjects')


def assert_approx_equal(value_a, value_b):
    if isinstance(value_a, dict):
        assert isinstance(value_b, dict)
        assert value_a.keys() == value_b.keys()
        for key, sub_a in value_a.items():
            assert_approx_equal(sub_a, value_b[key])
    elif isinstance(value_a, tuple):
        assert len(value_a) == len(value_b)
        for sub_a, sub_b in zip(value_a, value_b):
            assert_approx_equal(sub_a, sub_b)
    elif isinstance(value_a, float):
        assert isinstance(value_b, float)
        assert value_a == pytest.approx(value_b)
    else:
        assert value_a == value_b
