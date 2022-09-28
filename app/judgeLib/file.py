def readFile(file_dir: str) -> str:
    try:
        with open(file_dir, 'r') as f:
            lines = f.readlines()
            return arrange(lines)
    except FileNotFoundError:
        return 'Error: file not found'


def writeFile(file_dir: str, text: str) -> None:
    with open(file_dir, 'w') as f:
        lines = text.split('\r')
        f.write(arrange(lines))


def arrange(lines: list[str]) -> str:
    for index, line in enumerate(lines):
        lines[index] = line.strip()

    for index, line in enumerate(lines):
        if line == '':
            lines.pop(index)
        else:
            lines[index] = line + '\n'

    return ''.join(lines).encode('utf-8', 'ignore').decode('utf-8')