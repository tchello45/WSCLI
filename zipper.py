from zipfile import ZipFile
def save_config(path:str, config):
    zip_ = ZipFile(path, 'a')
    zip_.writestr('config.json', config)
    zip_.close()
def save_token(path:str, token):
    zip_ = ZipFile(path, 'a')
    zip_.writestr('token.txt', token)
    zip_.close()
def save_log(path:str, log:str):
    da = open("log.txt", "a")
    da.write(log + "\n")
    da.close()
def save_long_log(path:str, long_log):
    da = open("long_log.txt", "a")
    da.write(long_log+ "\n")
    da.close()
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
if __name__ == "__main__":
    #change token to invalid token
    save_token("conf.wscli", "_token_INVALID_TOKEN_")