import pytest
import os
import yaml
from llm_tracker.tracker import LLMTracker
from llm_tracker.storage.json_storage import JSONStorage
from llm_tracker.storage.sqlite_storage import SQLiteStorage
from llm_tracker.storage.cloud_storage import CloudStorage

def test_initialization_json(tmpdir):
    config = {
        'storage_backend': 'json_file',
        'json_file': {
            'file_path': os.path.join(tmpdir, 'test_data.json')
        }
    }
    config_file_path = os.path.join(tmpdir, 'config.yaml')
    with open(config_file_path, 'w') as f:
        yaml.dump(config, f)
    tracker = LLMTracker(config_file=config_file_path)
    assert tracker.config['storage_backend'] == 'json_file'
    assert isinstance(tracker.storage_backend, JSONStorage)

def test_initialization_sqlite(tmpdir):
    config = {
        'storage_backend': 'sqlite',
        'sqlite_database': os.path.join(tmpdir, 'test_data.sqlite')
    }
    config_file_path = os.path.join(tmpdir, 'config.yaml')
    with open(config_file_path, 'w') as f:
        yaml.dump(config, f)
    tracker = LLMTracker(config_file=config_file_path)
    assert tracker.config['storage_backend'] == 'sqlite'
    assert isinstance(tracker.storage_backend, SQLiteStorage)

def test_initialization_cloud_storage(tmpdir):
    config = {
        'storage_backend': 'cloud_storage',
        'cloud_storage': {
            'provider': 'aws_s3',  # Added provider key
            'bucket_name': 'test-bucket',
            'credentials': {
                'access_key_id': 'fake-access-key',
                'secret_access_key': 'fake-secret-key'
            }
        }
    }
    config_file_path = os.path.join(tmpdir, 'config.yaml')
    with open(config_file_path, 'w') as f:
        yaml.dump(config, f)
    tracker = LLMTracker(config_file=config_file_path)
    assert tracker.config['storage_backend'] == 'cloud_storage'
    assert isinstance(tracker.storage_backend, CloudStorage)
