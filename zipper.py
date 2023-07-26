from zipfile import ZipFile
import os
"""
tree:
    <path>
    ├───config.json
    ├───token.txt
    ├───log.txt
    ├───long_log.txt
    ├───error_dict.json
"""
def save_config(path:str, config):
    zip_ = ZipFile(path, 'a')
    zip_.writestr('config.json', config)
    zip_.close()
def save_token(path:str, token):
    zip_ = ZipFile(path, 'a')
    zip_.writestr('token.txt', token)
    zip_.close()
def save_log(path:str, log):
    zip_ = ZipFile(path, 'a')
    if "log.txt" in zip_.namelist():
        zip_.writestr('log.txt', zip_.read('log.txt').decode() + "\n" + log)
    else:
        zip_.writestr('log.txt', log)
        zip_.close()
def save_long_log(path:str, long_log):
    zip_ = ZipFile(path, 'a')
    if "long_log.txt" in zip_.namelist():
        zip_.writestr('long_log.txt', zip_.read('long_log.txt').decode() + "\n" + long_log)
    else:
        zip_.writestr('long_log.txt', long_log)
        zip_.close()
def save_error_dict(path:str, error_dict):
    zip_ = ZipFile(path, 'a')
    zip_.writestr('error_dict.json', error_dict)
    zip_.close()
def read_config(path:str):
    zip_ = ZipFile(path, 'r')
    config = zip_.read('config.json')
    zip_.close()
    return config
def read_token(path:str):
    zip_ = ZipFile(path, 'r')
    token = zip_.read('token.txt')
    zip_.close()
    return token
def read_log(path:str):
    zip_ = ZipFile(path, 'r')
    log = zip_.read('log.txt')
    zip_.close()
    return log
def read_long_log(path:str):
    zip_ = ZipFile(path, 'r')
    long_log = zip_.read('long_log.txt')
    zip_.close()
    return long_log
def read_error_dict(path:str):
    zip_ = ZipFile(path, 'r')
    error_dict = zip_.read('error_dict.json')
    zip_.close()
    return error_dict

save_config("conf.usscs", "CONFIG")
save_token("conf.usscs", "TOKEN")
save_log("conf.usscs", "LOG")
save_log("conf.usscs", "LOG2")

print(read_config("conf.usscs"))
print(read_token("conf.usscs"))
print(read_log("conf.usscs").decode())
