import pytest
import os
import yaml
import asyncio
from llm_tracker.tracker import LLMTracker

@pytest.fixture
def temp_config_file(tmpdir):
    config = {
        'storage_backend': 'json_file',
        'json_file': {
            'file_path': os.path.join(tmpdir, 'test_data.json')
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

def test_record_input_metadata_empty(tracker):
    request_data = {
        'model': 'gpt-3.5-turbo',
        'messages': [],
        'metadata_key': 'test_key_empty'
    }
    usage_data = asyncio.run(tracker.record_input_metadata(request_data))
    assert usage_data['prompt_tokens'] == 0

def test_record_input_metadata_large(tracker):
    large_text = "Hello, world! " * 1000
    request_data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': large_text}],
        'metadata_key': 'test_key_large'
    }
    usage_data = asyncio.run(tracker.record_input_metadata(request_data))
    assert usage_data['prompt_tokens'] > 0
