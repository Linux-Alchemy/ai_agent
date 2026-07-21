from ai_agent.functions.get_file_content import get_file_content
from pathlib import Path



def test_get_file_content_returns_contents(tmp_path: Path):
    """Reading a file returns its text contents."""
    test_file = tmp_path/"test.txt"
    test_file.write_text("So long and thanks for all the fish")
    result = get_file_content(str(tmp_path), "test.txt")
    assert "fish" in result



def test_get_file_content_rejects_escape(tmp_path: Path):
    """A path outside the working directory returns an Error string."""
    result = get_file_content(str(tmp_path), "../")
    assert result.startswith("Error:")

