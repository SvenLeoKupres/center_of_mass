import json


def load_json_data(path):
    with open(path, 'r') as f:
        data = json.load(f)

    return data


class Dataset:
    def __init__(self):
        pass


class RPlanDataset (Dataset):
    def __init__(self, path="./rplan/dataset_json/data_test.json"):
        super().__init__()

        self.data = load_json_data(path)
