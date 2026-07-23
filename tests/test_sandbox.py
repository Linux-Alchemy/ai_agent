from pathlib import Path

from ai_agent.sandbox import resolve_in_workdir


def test_resolve_returns_path_for_contained(tmp_path: Path):
    """A normal contained path resolves to an absolute path inside the root."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("I am your father")
    result = resolve_in_workdir(str(tmp_path), test_file.name)
    assert result == str(test_file.resolve())


def test_resolve_rejects_dotdot_escape(tmp_path: Path):
    """A ``../`` path that climbs out of the root returns None."""
    test_path = "../"
    result = resolve_in_workdir(str(tmp_path), test_path)
    assert result is None


def test_resolve_rejects_symlink_escape(tmp_path: Path):
    """A symlink pointing outside the root is rejected (returns None)."""
    sandbox = tmp_path / "sandbox"
    sandbox.mkdir()
    outside_file = tmp_path / "outside.txt"
    outside_file.write_text("Definitely harmless. Probably.")
    escape_link = sandbox / "escape.txt"
    escape_link.symlink_to(outside_file)

    result = resolve_in_workdir(str(sandbox), escape_link.name)
    assert result is None
