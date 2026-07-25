DANGEROUS: frozenset[str] = frozenset({"write_file", "run_python_file"})


def needs_approval(function_name: str, auto_approve: bool) -> bool:
    """Return True if this call must be confirmed by the human first.

    Args:
        function_name: The tool the model wants to run.
        auto_approve: If True, nothing is ever gated.

    Returns:
        True if the call is dangerous and auto_approve is off.
    """
    return function_name in DANGEROUS and not auto_approve


def confirm(function_name: str, function_args: dict[str, object]) -> bool:
    """Prompt the human to approve one tool call. Returns their yes/no.

    Prints the tool name and its arguments, then reads a y/N answer from
    stdin. Anything other than an explicit yes is treated as no.

    Args:
        function_name: The tool awaiting approval.
        function_args: The arguments the model wants to call it with.

    Returns:
        True only on an explicit yes; default-deny on anything else.
    """
    print(f"Need approval to run {function_name}, {function_args}")
    response = input("Approve [y/N]?: ").strip().lower()
    return response in {"y", "yes"}
