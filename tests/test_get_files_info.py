from ai_agent.functions.get_files_info import get_files_info
from pathlib import Path


def test_get_files_info_lists_contents(tmp_path: Path):
    """Listing a directory returns each entry with its size and is_dir flag."""
    test_file = tmp_path/"test.txt"
    test_file.write_text("These are not the droids you're looking for")

    result = get_files_info(str(tmp_path), ".")
    assert "test.txt" in result
    assert "is_dir" in result



def test_get_files_info_rejects_escape(tmp_path: Path):
    """A path outside the working directory returns an Error string."""
    result = get_files_info(str(tmp_path), "../")
    assert result.startswith("Error:")
