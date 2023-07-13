'''这个模块用python来运行一个文件或者内容'''

import sys
import os
import tempfile

def python_run_file(filename: str):
    '''用python来运行一个文件。'''

    if os.system("python3 -V") != 0:
        return os.system(f"python {filename}")
    else:
        return os.system(f"python3 {filename}")

def python_run(content):
    '''用python来运行一个内容。'''
    
    tmp_name = None
    with tempfile.NamedTemporaryFile(mode = "w", encoding = "utf-8", delete = False) as fil:
        tmp_name = fil.name
        fil.write(content)

    if tmp_name is not None:
        python_run_file(tmp_name)