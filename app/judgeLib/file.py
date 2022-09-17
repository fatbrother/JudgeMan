def readFile(file_dir: str) -> str:
    try:
        with open(file_dir, 'r') as f:
            lines = f.readlines()
            return arrange(lines)
    except FileNotFoundError:
        return 'Error: file not found'


def writeFile(file_dir: str, text: str) -> None:
    with open(file_dir, 'w') as f:
        f.write(text)


def arrange(lines: list[str]) -> str:
    # clean up the empty lines in the end of the file
    while lines[-1] == '\n':
        lines.pop()

    # clean up the empty lines in the beginning of the file
    while lines[0] == '\n':
        lines.pop(0)

    lines[-1].strip()

    return ''.join(lines).encode('utf-8', 'ignore').decode('utf-8')