# LLM Tracker
LLM Tracker is a library to track token usage and cost by end user, prompt id, org id, or any other attribute during usage of Large Language Models (LLMs).

## Features
- Track input and output metadata for LLMs
- Track token and costs by org_id, user_id, prompt_id, prompt_version_id
- Track token and costs by your own tags (e.g. app_id, app_version_id, campaign_id)
- Support for various storage backends (JSON, SQLite, Cloud)
- Visualization of token usage and metadata distribution

## Installation
```bash
pip install llm_tracker
```

## Configuration
Copy the example configuration file:

```bash
cp config.example.yaml config.yaml
```

Edit config.yaml with your specific settings


## Usage
```bash
from llm_tracker import LLMTracker
tracker = LLMTracker('config.json')
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
LLM Tracker is open-source software licensed under the [Apache License 2.0](LICENSE).
For commercial use, please refer to the [Commercial License](LICENSE_COMMERCIAL). For inquiries regarding commercial licensing, please contact us at info@toccata.ai.
