from ai_agent.functions.run_python_file import run_python_file
from pathlib import Path




def test_run_python_file_captures_output(tmp_path: Path):
    """Running a .py file returns its captured STDOUT."""
    test_script = tmp_path/ "test_python.py"
    test_script.write_text('print("The Force will be with you. Probably")')
    result = run_python_file(str(tmp_path), "test_python.py")
    assert "The Force" in result



def test_run_python_file_rejects_non_python(tmp_path: Path):
    """A non-.py file returns an Error string."""
    test_file = tmp_path/ "nope.txt"
    test_file.write_text("These are not the droids you're looking for")
    result = run_python_file(str(tmp_path), "nope.txt")
    assert result.startswith("Error:")
