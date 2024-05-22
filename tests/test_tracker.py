import pytest
import os
import yaml
import asyncio
from llm_tracker.tracker import LLMTracker
# from unittest.mock import patch, MagicMock

@pytest.fixture
def temp_config_file(tmpdir):
    config = {
        'storage_backend': 'json_file',
        'json_file': {
            'file_path': os.path.join(tmpdir, 'test_data.json')
        },
        'sqlite_database': os.path.join(tmpdir, 'test_data.sqlite'),
        'cloud_storage': {
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
    return config_file_path

@pytest.fixture
def tracker(temp_config_file):
    return LLMTracker(config_file=temp_config_file)

def test_record_input_metadata(tracker):
    request_data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': 'Hello, world!'}],
        'metadata_key': 'test_key'
    }
    usage_data = asyncio.run(tracker.record_input_metadata(request_data))
    assert 'prompt_tokens' in usage_data
    assert 'metadata' in usage_data
    assert usage_data['metadata']['metadata_key'] == 'test_key'

def test_record_output_metadata(tracker):
    request_data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': 'Hello, world!'}],
        'metadata_key': 'test_key'
    }
    response_data = {
        'usage': {
            'prompt_tokens': 5,
            'completion_tokens': 5,
            'total_tokens': 10
        }
    }
    asyncio.run(tracker.record_input_metadata(request_data))
    result = asyncio.run(tracker.record_output_metadata(request_data, response_data))
    assert 'response_data' in result
    assert 'usage_data' in result
    assert result['usage_data']['total_tokens'] == 10
