import pytest


def test_resolve_returns_path_for_contained(tmp_path):
    """A normal contained path resolves to an absolute path inside the root."""
    pytest.skip("stub — implement in Task 1.3.4")


def test_resolve_rejects_dotdot_escape(tmp_path):
    """A ``../`` path that climbs out of the root returns None."""
    pytest.skip("stub — implement in Task 1.3.4")


def test_resolve_rejects_symlink_escape(tmp_path):
    """A symlink pointing outside the root is rejected (returns None)."""
    pytest.skip("stub — implement in Task 1.3.4")
