import subprocess


def compile(filename: str) -> bool:
    if filename.endswith('.c'):
        return compile_c(filename[:-2])
    elif filename.endswith('.cpp'):
        return compile_cpp(filename[:-4])
    else:
        return False


def compile_c(filename: str) -> bool:
    try:
        subprocess.run(['gcc', filename+'.c', '-o', filename+'.exe'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False


def compile_cpp(filename: str) -> bool:
    try:
        subprocess.run(['g++', filename+'.cpp', '-o', filename+'.exe'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False