from functions.get_file_content import get_file_content

# Truncation check — don't print the full contents, just the shape of the result
result = get_file_content("calculator", "lorem.txt")
print(f"lorem.txt length: {len(result)}")
print(f"lorem.txt truncated: {'truncated' in result}")

# TODO: print get_file_content("calculator", "main.py")

# TODO: print get_file_content("calculator", "pkg/calculator.py")

# TODO: print get_file_content("calculator", "/bin/cat")   # expect an Error string

# TODO: print get_file_content("calculator", "pkg/does_not_exist.py")   # expect an Error string
