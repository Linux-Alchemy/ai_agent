from ai_agent.functions.run_python_file import run_python_file

# --- original print-scripts (kept for reference; remove when done) ---
# print(run_python_file("calculator", "main.py"))
# print(run_python_file("calculator", "main.py", ["3 + 5"]))
# print(run_python_file("calculator", "tests.py"))
# print(run_python_file("calculator", "../main.py"))
# print(run_python_file("calculator", "nonexistent.py"))
# print(run_python_file("calculator", "lorem.txt"))


def test_run_python_file_captures_output(tmp_path):
    """Running a .py file returns its captured STDOUT."""
    # TODO: write a tiny script — (tmp_path / "hello.py").write_text('print("hi from subprocess")')
    # TODO: result = run_python_file(str(tmp_path), "hello.py")
    # TODO: assert "hi from subprocess" in result   (STDOUT is included in the result)
    ...


def test_run_python_file_rejects_non_python(tmp_path):
    """A non-.py file returns an Error string."""
    # TODO: create a non-python file — (tmp_path / "note.txt").write_text("nope")
    # TODO: result = run_python_file(str(tmp_path), "note.txt")
    # TODO: assert result.startswith("Error:")
    ...
