import json


def load_json(filepath):
    with open(filepath, "r") as f:
        json_ = json.load(f)
    return json_
