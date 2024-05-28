import os
from openai import AzureOpenAI
import asyncio
import yaml
from llm_tracker.tracker import LLMTracker

# Load configuration
config_file = 'config.yaml'
with open(config_file, 'r') as f:
    config = yaml.safe_load(f)

# Initialize LLMTracker
tracker = LLMTracker(config_file=config_file)

# Set OpenAI API key and endpoint
# openai.azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
# openai.api_key = os.getenv('OPENAI_API_KEY')

async def live_test():
    request_data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Can you tell me a joke?"}
        ],
        'metadata_key': 'live_test_key'
    }

    # Record input metadata
    usage_data_input = await tracker.record_input_metadata(request_data)
    print("Input Metadata Recorded:", usage_data_input)

    # Send a request to OpenAI API
    client = AzureOpenAI(
    api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")  # Your Azure OpenAI resource's endpoint value.
    )

    # response = client.chat.completions.create(
    #     model=request_data['model'],
    #     messages=request_data['messages'],
    #     azure_endpoint=openai.azure_endpoint,  # Specify the Azure endpoint base URL
    #     api_key=openai.api_key  # Specify the Azure API key
    # )
    
    # response_data = {
    #     'usage': response['usage'],
    #     'choices': response['choices']
    # }

    # for chunk in response:
    #     if chunk.choices[0].delta.content is not None:
    #         print(chunk.choices[0].delta.content, end="")

    # # Record output metadata
    # result = await tracker.record_output_metadata(request_data, response_data)
    # print("Output Metadata Recorded:", result)

    # # Verify recorded data
    # recorded_usage = tracker.get_usage()
    # print("Recorded Usage:", recorded_usage)

if __name__ == "__main__":
    asyncio.run(live_test())
