import asyncio
from tiktoken import Tokenizer
from .storage.json_storage import JSONStorage
from .storage.sqlite_storage import SQLiteStorage
from .storage.cloud_storage import CloudStorage
from .utils.config_loader import load_config

class LLMTracker:
    def __init__(self, config_file='config.json', **tags):
        self.config = load_config(config_file)
        self.storage_backend = self._get_storage_backend(self.config['storage_backend'])
        self.tags = tags  # Store arbitrary tags
        self.metadata_storage = {}  # Dictionary to store metadata for reuse

    def _get_storage_backend(self, backend_type):
        if backend_type == 'json_file':
            return JSONStorage(self.config)
        elif backend_type == 'sqlite':
            return SQLiteStorage(self.config)
        elif backend_type == 'cloud_storage':
            return CloudStorage(self.config)
        else:
            raise ValueError("Unsupported storage backend")

    async def record_input_metadata(self, request_data: dict):
        prompt = " ".join([msg['content'] for msg in request_data['messages']])
        tokenizer = Tokenizer()
        prompt_tokens = len(tokenizer.encode(prompt))

        metadata = {key: value for key, value in request_data.items() if key not in ['messages', 'api_key']}
        metadata.update(self.tags)  # Include arbitrary tags

        usage_data = {
            'prompt_tokens': prompt_tokens,
            'completion_tokens': 0,  # Placeholder, will be updated with output
            'total_tokens': prompt_tokens,  # Initial value, will be updated with output
            'metadata': metadata
        }

        self.metadata_storage[request_data['metadata_key']] = metadata  # Store metadata using a unique key

        await self.storage_backend.save(usage_data)
        return usage_data

    async def record_output_metadata(self, request_data: dict, response_data: dict):
        metadata_key = request_data['metadata_key']
        metadata = self.metadata_storage.get(metadata_key, {})  # Retrieve stored metadata

        usage_data = {
            'prompt_tokens': response_data['usage']['prompt_tokens'],
            'completion_tokens': response_data['usage']['completion_tokens'],
            'total_tokens': response_data['usage']['total_tokens'],
            'metadata': metadata
        }

        await self.storage_backend.save(usage_data)
        return {
            'response_data': response_data,
            'usage_data': usage_data
        }

    async def get_usage(self):
        return await self.storage_backend.load()
