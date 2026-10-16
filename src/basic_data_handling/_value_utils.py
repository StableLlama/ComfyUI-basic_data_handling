"""Small helpers shared by the node modules (this is not a ComfyUI node module)."""

from typing import Any


def as_bool(value: Any) -> bool:
    """Normalize a ComfyUI BOOLEAN widget/input value into a real bool.

    ComfyUI hands over real booleans, but legacy combo widgets ("True" / "False"
    strings) and nodes with ``INPUT_IS_LIST`` (values wrapped into a list) also
    occur, so all of them are accepted here.
    """
    if isinstance(value, (list, tuple)):
        value = value[0] if value else False
    if isinstance(value, str):
        return value.strip().lower() in ("true", "1", "yes", "on")
    return bool(value)


def is_empty_entry(value: Any, treat_whitespace_as_empty: bool = False) -> bool:
    """Tell whether an entry of a Data List / LIST has to be regarded as empty.

    Empty are ``None``, an empty STRING and an empty collection (empty LIST,
    DICT, SET, ...). Numbers and booleans are never empty, so ``0`` and ``False``
    are kept.

    When ``treat_whitespace_as_empty`` is enabled, a STRING that consists only of
    whitespace characters (spaces, tabs, line breaks, ...) counts as empty as
    well. The whitespace rule applies to STRINGs only; objects without a length
    (e.g. plain numbers or 0-dimensional TENSORs) are never empty.
    """
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip() if treat_whitespace_as_empty else not value
    try:
        return len(value) == 0
    except TypeError:
        return False
