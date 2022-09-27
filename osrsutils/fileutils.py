import json
import os

def get_data_dir():
    return os.path.dirname(os.path.realpath(__file__)) + '\\'

def write_to_json(file,data):
    try:
        with open(file, 'w+', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii = False, indent = 4,skipkeys = True)
        return True
    except OSError as e:
        print(e)
        return False

def read_json(file):
    try:
        with open(file) as f:
            f.seek(0)
            if(not f.seek(1)):
                data = {}
            else:
                f.seek(0)
                data = json.load(f)
    except OSError as e:
        print(e)
        data = {}

    return data