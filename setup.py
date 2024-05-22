from setuptools import setup, find_packages

setup(
    name='llm_tracker',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'tiktoken',
        'sqlalchemy',
        'psycopg2-binary',  # Only if using PostgreSQL for cloud storage
        'boto3',  # Only if using AWS S3 for cloud storage
        'jsonschema',
        'pyyaml',
        'matplotlib',
        'pandas',
        'plotly'
    ],
    extras_require={
        'dev': [
            'pytest',
            'flake8',
            'black',
        ],
        'postgresql': [
            'psycopg2-binary'
        ],
        's3': [
            'boto3'
        ],
        'visualization': [
            'matplotlib',
            'plotly'
        ]
    },
    include_package_data=True,
    description='A library for tracking LLM metadata and usage.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/benyi1981/llm_tracker',
    author='Ben Yi',
    author_email='ben.yi@toccata.ai',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7',
)
