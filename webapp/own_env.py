import pathlib

def create_dict_env():
    file_env = pathlib.Path(".env").read_text().split()
    dict_env = {}
    for kv in file_env:
        list_kv = kv.split("=")
        dict_env[list_kv[0]] = list_kv[1]
    return dict_env


def getenv(key):
    dict_find = create_dict_env()
    return dict_find[key]