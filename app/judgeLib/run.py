import subprocess
import psutil

def run(file_dir: str, input: str, timeLimit: float, memoryLimit: int) -> str:
    res = ''

    try:
        # run the program
        
        process = subprocess.Popen(
            ['./'+file_dir], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    except RuntimeError:
        res = 'RE'
    except MemoryError:
        res = 'MLE'
    except TimeoutError:
        res = 'TLE'
    except:
        res = 'CE'

    if res == '':
        # calculate memory usage
        memory_usage = psutil.Process(process.pid).memory_info().rss / (1024 ** 2)
        if memory_usage > memoryLimit:
            res = 'MLE'

        # check if the program is something wrong
        try:
            output, error = process.communicate(
                input.encode('utf-8', 'ignore'), timeout=timeLimit)
            if error:
                print(error)
                res = 'CE'  
        except subprocess.TimeoutExpired:
            res = 'TLE'
        except:
            res = 'RE'

        # close the process
        process.terminate()
        process.wait()
    
    return (res or output.decode('utf-8'))
