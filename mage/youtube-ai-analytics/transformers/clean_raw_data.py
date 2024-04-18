if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import time
import pandas as pd
import numpy as np
from openai import OpenAI

# Load config.py file
import sys
import os
# Add project folder to import packages
sys.path.append(os.getcwd() + '/' + os.environ.get('PROJECT_NAME'))
import config
# Reload config.py file to update changes (instead of restarting Docker)
import importlib
importlib.reload(config)

# Load inputs from config.py file
data_types_channels = config.data_types_channels
data_types_videos = config.data_types_videos
data_types_comments = config.data_types_comments

@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Get data from loader
    df_channels, df_videos, df_comments = data

    # CHANNELS TRANSFORMATIONS
    df_channels = df_channels.drop(columns=['channel_uploads_playlist_id'])
    df_channels['channel_custom_url'] = 'https://www.youtube.com/' + df_channels['channel_custom_url']
    df_channels['channel_custom_url'] = 'https://www.youtube.com/' + df_channels['channel_custom_url']
    df_channels['channel_title'].replace('DataTalksClub ⬛', 'DataTalksClub', inplace=True)

    # VIDEOS TRANSFORMATIONS
    df_videos['video_url'] = 'https://www.youtube.com/watch?v=' + df_videos['video_id']
    
    # Extract hours, minutes, and seconds from 'video_duration'
    time_parts = df_videos['video_duration'].str.extract(r'PT(\d+H)?(\d+M)?(\d+S)?')
    # Convert extracted parts to numeric and fill NaN with 0
    df_videos['video_hours'] = pd.to_numeric(time_parts[0].str.replace('H', ''), errors='coerce').fillna(0).astype('Int64')
    df_videos['video_minutes'] = pd.to_numeric(time_parts[1].str.replace('M', ''), errors='coerce').fillna(0).astype('Int64')
    df_videos['video_seconds'] = pd.to_numeric(time_parts[2].str.replace('S', ''), errors='coerce').fillna(0).astype('Int64')
    df_videos['video_duration_seconds'] = df_videos['video_hours'] * 3600 + df_videos['video_minutes'] * 60 + df_videos['video_seconds']
    df_videos['video_duration'] = df_videos['video_hours'].apply(lambda x: '{:02d}'.format(x)) + ':' + df_videos['video_minutes'].apply(lambda x: '{:02d}'.format(x)) + ':' + df_videos['video_seconds'].apply(lambda x: '{:02d}'.format(x))
    df_videos = df_videos.drop(columns=['video_hours','video_minutes','video_seconds'])
    # Filter videos with duration > 0
    df_videos = df_videos[df_videos['video_duration_seconds'] > 0]

    # COMMON TRANSFORMATIONS
    # Replace nulls with 0 on Int64 cols
    int_cols = df_channels.select_dtypes(include=['Int64']).columns
    df_channels[int_cols] = df_channels[int_cols].fillna(0)

    int_cols = df_videos.select_dtypes(include=['Int64']).columns
    df_videos[int_cols] = df_videos[int_cols].fillna(0)

    int_cols = df_comments.select_dtypes(include=['Int64']).columns
    df_comments[int_cols] = df_comments[int_cols].fillna(0)

    # Replace "nan" with np.nan (or empty string) on str / object cols
    df_channels.replace('nan', np.nan, inplace=True)
    df_videos.replace('nan', np.nan, inplace=True)
    df_comments.replace('nan', np.nan, inplace=True)

    # df_channels.to_excel('df_channels.xlsx')
    # df_videos.to_excel('df_videos.xlsx')
    # df_comments.to_excel('df_comments.xlsx')

    return [df_channels, df_videos, df_comments]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
