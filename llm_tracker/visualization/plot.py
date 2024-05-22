import matplotlib.pyplot as plt
import pandas as pd

def plot_token_usage(usage_data):
    df = pd.DataFrame(usage_data)
    df['timestamp'] = pd.to_datetime(df['metadata'].apply(lambda x: x.get('timestamp')))
    df.set_index('timestamp', inplace=True)

    df['total_tokens'].plot(kind='line', title='Total Token Usage Over Time')
    plt.xlabel('Time')
    plt.ylabel('Total Tokens')
    plt.show()

def plot_metadata_distribution(usage_data, metadata_key):
    df = pd.DataFrame(usage_data)
    distribution = df['metadata'].apply(lambda x: x.get(metadata_key)).value_counts()

    distribution.plot(kind='bar', title=f'Distribution of {metadata_key}')
    plt.xlabel(metadata_key)
    plt.ylabel('Count')
    plt.show()
