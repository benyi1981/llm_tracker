import boto3
import json
from botocore.exceptions import NoCredentialsError
from .storage_backend import StorageBackend

class CloudStorage(StorageBackend):
    def __init__(self, config):
        self.bucket_name = config['cloud_storage']['bucket_name']
        self.access_key = config['cloud_storage']['credentials']['access_key_id']
        self.secret_key = config['cloud_storage']['credentials']['secret_access_key']
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
        )

    def save(self, data):
        self.s3.put_object(
            Bucket=self.bucket_name,
            Key='llm_tracker_data.json',
            Body=json.dumps(data)
        )

    def load(self):
        try:
            response = self.s3.get_object(
                Bucket=self.bucket_name,
                Key='llm_tracker_data.json'
            )
            return json.loads(response['Body'].read().decode('utf-8'))
        except self.s3.exceptions.NoSuchKey:
            return []
