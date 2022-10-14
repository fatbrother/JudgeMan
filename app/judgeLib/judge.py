import time
from .compile import compile
from .file import readFile, writeFile
from .run import run
import os


# this func return the result of judging and IO and expect of the program
def judge(file_dir: str = None, code_text: str = None, language: str = None, input_dir: str = None, input: str = None, answer_dir: str = None, answer: str = None, timeLimit: float = 1, memoryLimit: int = 512) -> tuple[str, str | None, str | None, str | None]:
    res, input, output, answer = '', '', '', ''

    if file_dir is None:
        if language is None:
            res = 'language is needed'
        if code_text is None:
            res = 'code text is needed'
        if res == '':
            file_dir = 'temp.' + language
            writeFile(file_dir, code_text)

    # compile
    if res == '':
        compileSuccess = compile(file_dir)
        if not compileSuccess:
            res = 'CE'

    if res == '':
        # read input and answer
        if input is None:
            try:
                input = readFile(input_dir)
            except:
                res = 'input file not found'
        if answer is None:
            try:
                answer = readFile(answer_dir)
            except:
                res = 'answer file not found'

        if input == 'Error: file not found':
            res = 'input not found'
        if answer == 'Error: file not found':
            res = 'answer not found'

    # run
    if res == '':
        exe_dir = file_dir.split('.')[0] + '.exe'
        if os.path.exists(exe_dir):
            output = run(exe_dir, input, timeLimit, memoryLimit)
        else:
            output = 'CE'

        if output == 'TLE':
            res = 'TLE'
            output = ''
        if output == 'MLE':
            res = 'MLE'
            output = ''
        if output == 'RE':
            res = 'RE'
            output = ''
        if output == 'CE':
            res = 'CE'
            output = ''

    txt_dir = './temp.txt'
    if res == '':
        # wash the output
        writeFile(txt_dir, output)
        output = readFile(txt_dir)

        res = 'AC' if output == answer else 'WA'

    # clean up the file
    try:
        os.remove(exe_dir)
    except:
        pass
    try:
        os.remove(file_dir)
    except:
        pass
    try:
        os.remove(txt_dir)
    except:
        pass

    return res, input, output, answer
