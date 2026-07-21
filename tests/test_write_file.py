from ai_agent.functions.write_file import write_file
from pathlib import Path


def test_write_file_reports_char_count(tmp_path: Path):
    """A successful write returns the success message with the char count."""
    content = "testing the write_file function"
    result = write_file(str(tmp_path), "note.txt", content)
    assert "Success" in result
    assert str(len(content)) in result



def test_write_file_rejects_escape(tmp_path: Path):
    """A path outside the working directory returns an Error string."""
    result = write_file(str(tmp_path), "/tmp/temp.txt", "this should not be allowed")
    assert result.startswith("Error:")


