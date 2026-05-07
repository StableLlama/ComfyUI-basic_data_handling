import pytest

from src.basic_data_handling._dynamic_input import ContainsDynamicDict


def test_contains_dynamic_dict_basic_lookup():
    d = ContainsDynamicDict({
        'value': ('x', {'_dynamic': 'number'}),
        'fixed': 'y',
    })

    # direct behavior
    assert 'value' in d
    assert d['value'] == ('x', {'_dynamic': 'number'})

    # dynamic numeric key lookup
    assert 'value1' in d
    assert d['value1'] == ('x', {'_dynamic': 'number'})
    assert 'value999' in d
    assert d['value999'] == ('x', {'_dynamic': 'number'})

    # non-dynamic key and fallback
    assert 'fixed' in d
    assert d['fixed'] == 'y'

    # non-matching key should not be present
    assert 'novalue' not in d
    with pytest.raises(KeyError):
        _ = d['novalue']


def test_contains_dynamic_dict_partial_prefix_not_numeric():
    d = ContainsDynamicDict({'val': ('z', {'_dynamic': 'number'})})

    assert 'val' in d
    assert d['val'] == ('z', {'_dynamic': 'number'})
    assert 'val1' in d
    assert d['val1'] == ('z', {'_dynamic': 'number'})
    assert 'valx' not in d
    with pytest.raises(KeyError):
        _ = d['valx']
