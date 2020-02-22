from undata import *
import re
import json


def data_str2json(data_str):
    return json.loads(re.sub(r'(?P<key>\w+):', lambda x: ('"' + x.group('key') + '":'), data_str))


def data_file2json(file_path):
    return data_str2json(farm_data_read(file_path))


def json2data_str(json_str):
    return re.sub(r'"(?P<key>\w+)":', lambda x: (x.group('key') + ':'), json.dumps(json_str)).replace(" ", "")


def json2data_file(file_path, json_str):
    return farm_data_wirte(file_path, json2data_str(json_str))
