from judgeLib.compile import compile
from judgeLib.file import readFile, writeFile
from judgeLib.run import run
import os


# this func return the result of judging and IO and expect of the program
def judge(file_dir: str = None, code_text: str = None, language: str = None, input_dir: str = None, answer_dir: str = None, timeLimit: float = 1.0, memoryLimit: int = 512) -> tuple[str, str | None, str | None, str | None]:
    res = ''

    need_delete = False
    if file_dir is None:
        if language is None:
            res = 'language is needed'
        if code_text is None:
            res = 'code text is needed'
        if res == '':
            file_dir = 'temp.' + language
            writeFile(file_dir, code_text)
            need_delete = True

    # compile
    if res == '':
        compileSuccess = compile(file_dir)
        if not compileSuccess:
            res = 'CE'

    if res == '':
        # read input and answer
        input = readFile(input_dir)
        answer = readFile(answer_dir)
        if input == 'Error: file not found':
            res = 'input not found'
        if answer == 'Error: file not found':
            res = 'answer not found'

    # run
    if res == '':
        print(file_dir)
        exe_dir = file_dir.split('.')[0] + '.exe'
        print('exe_dir:', exe_dir)
        if os.path.exists(exe_dir):
            output = run(exe_dir, input, timeLimit, memoryLimit)
        else:
            print('False')
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

        if output == answer:
            res = 'AC'
        else:
            res = 'WA'

    # clean up the file
    if os.path.exists(exe_dir):
        os.remove(exe_dir)
    if os.path.exists(file_dir) and need_delete:
        os.remove(file_dir)
    if os.path.exists(txt_dir):
        os.remove(txt_dir)

    return res, input, output, answer
