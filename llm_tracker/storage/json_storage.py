import json
import os
from .storage_backend import StorageBackend

class JSONStorage(StorageBackend):
    def __init__(self, config):
        self.file_path = config['json_file']['file_path']

    def save(self, data: dict):
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                existing_data = json.load(file)
        else:
            existing_data = []

        existing_data.append(data)

        with open(self.file_path, "w") as file:
            json.dump(existing_data, file, indent=4)

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                return json.load(file)
        return []
