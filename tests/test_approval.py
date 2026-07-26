from ai_agent.approval import needs_approval

# NOTE: `confirm` is deliberately untested — it reads from stdin, and simulating
# that costs more than it proves here. Known, accepted hole.


def test_dangerous_tool_without_auto_approve_needs_approval() -> None:
    """A dangerous tool with auto_approve off must be gated."""
    result = needs_approval("write_file", auto_approve=False)
    assert result is True


def test_read_only_tool_never_needs_approval() -> None:
    """A read-only tool is never gated, even with auto_approve off."""
    result = needs_approval("get_file_content", auto_approve=False)
    assert result is False


def test_auto_approve_bypasses_the_gate() -> None:
    """auto_approve=True skips the gate even for a dangerous tool."""
    result = needs_approval("write_file", auto_approve=True)
    assert result is False   # asserting that the tool does not need approval from the human
