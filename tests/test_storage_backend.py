import pytest
import os
import json
from llm_tracker.storage.json_storage import JSONStorage
from llm_tracker.storage.sqlite_storage import SQLiteStorage
from llm_tracker.storage.cloud_storage import CloudStorage
from unittest.mock import patch, MagicMock

@pytest.fixture
def json_storage(tmpdir):
    config = {
        'json_file': {
            'file_path': os.path.join(tmpdir, 'test_data.json')
        }
    }
    return JSONStorage(config)

@pytest.fixture
def sqlite_storage(tmpdir):
    config = {
        'sqlite_database': os.path.join(tmpdir, 'test_data.sqlite')
    }
    return SQLiteStorage(config)

@pytest.fixture
@patch('boto3.client')
def cloud_storage(mock_boto_client):
    mock_s3 = MagicMock()
    mock_boto_client.return_value = mock_s3
    config = {
        'cloud_storage': {
            'bucket_name': 'test-bucket',
            'credentials': {
                'access_key_id': 'fake-access-key',
                'secret_access_key': 'fake-secret-key'
            }
        }
    }
    return CloudStorage(config)

def test_json_storage_save_load(json_storage):
    test_data = {'key': 'value'}
    json_storage.save(test_data)
    loaded_data = json_storage.load()
    assert loaded_data == [test_data]

def test_sqlite_storage_save_load(sqlite_storage):
    test_data = {'key': 'value'}
    sqlite_storage.save(test_data)
    loaded_data = sqlite_storage.load()
    assert len(loaded_data) > 0
    assert loaded_data[0] == test_data

def test_cloud_storage_save_load(cloud_storage):
    test_data = {'key': 'value'}
    cloud_storage.save(test_data)
    cloud_storage.s3.get_object.return_value = {
        'Body': MagicMock(read=lambda: json.dumps(test_data).encode('utf-8'))
    }
    loaded_data = cloud_storage.load()
    assert loaded_data == test_data
