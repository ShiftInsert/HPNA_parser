import os

def check_write_access(f):
    if os.path.exists(f):
        try:
            os.rename(f, f)
            return 'ooo'
        except PermissionError:
            return ('*** FILE ' + f.split("\\")[-1] + ' IS LOCKED BY ANOTHER PROCESS, WRITE FAILED ***')

