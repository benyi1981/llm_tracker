import plotly.express as px
import pandas as pd

def plot_token_usage(usage_data):
    df = pd.DataFrame(usage_data)
    df['timestamp'] = pd.to_datetime(df['metadata'].apply(lambda x: x.get('timestamp')))
    df.set_index('timestamp', inplace=True)

    fig = px.line(df, y='total_tokens', title='Total Token Usage Over Time')
    fig.update_xaxes(title_text='Time')
    fig.update_yaxes(title_text='Total Tokens')
    fig.show()

def plot_metadata_distribution(usage_data, metadata_key):
    df = pd.DataFrame(usage_data)
    distribution = df['metadata'].apply(lambda x: x.get(metadata_key)).value_counts().reset_index()
    distribution.columns = [metadata_key, 'Count']

    fig = px.bar(distribution, x=metadata_key, y='Count', title=f'Distribution of {metadata_key}')
    fig.update_xaxes(title_text=metadata_key)
    fig.update_yaxes(title_text='Count')
    fig.show()
