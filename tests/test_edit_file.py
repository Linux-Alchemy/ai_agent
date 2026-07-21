import pytest


def test_edit_file_happy_path_returns_diff(tmp_path):
    """One match is replaced, the file changes, and a unified diff is returned."""
    pytest.skip("stub — implement in Task 2.2.4")


def test_edit_file_missing_old_string_errors(tmp_path):
    """A missing old_string returns an Error and leaves the file unchanged."""
    pytest.skip("stub — implement in Task 2.2.4")


def test_edit_file_ambiguous_old_string_errors(tmp_path):
    """An old_string with >1 match returns an Error and leaves the file unchanged."""
    pytest.skip("stub — implement in Task 2.2.4")
