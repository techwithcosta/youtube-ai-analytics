import io
import pandas as pd
from pandas import json_normalize
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import json
from urllib.parse import parse_qs, urlparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import numpy as np

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
input_videos = config.input_videos
max_videos_per_channel = config.max_videos_per_channel
fields_to_extract_channels = config.fields_to_extract_channels
data_types_channels = config.data_types_channels
fields_to_extract_videos = config.fields_to_extract_videos
data_types_videos = config.data_types_videos
fields_to_extract_comments = config.fields_to_extract_comments
data_types_comments = config.data_types_comments

# Load inputs from .env file
api_key = os.environ.get('YOUTUBE_API_KEY')

# Function to get channel ids from input videos
def get_channel_ids(youtube, input_videos):
    channel_ids = []
    for input_video in input_videos:
        parsed_url = urlparse(input_video)
        video_id = parse_qs(parsed_url.query)['v'][0]
        channel_id = youtube.videos().list(part='snippet', id=video_id).execute()['items'][0]['snippet']['channelId']
        channel_ids.append(channel_id)
        # Return unique channel ids
    return list(set(channel_ids))

# Function to extract values from nested dictionaries
def extract_value(dictionary, keys):
    for key in keys.split('.'):
        dictionary = dictionary.get(key)
        if dictionary is None:  # If key is not found, return NaN
            return np.nan
    return dictionary

# Function to get channels' information
def get_channels_info(youtube, channel_ids, fields_to_extract_channels, data_types_channels):
    get_part = 'id,snippet,contentDetails,statistics'
    channels_info = []
    # Initialize empty dataframe with correct columns
    df_channels = pd.DataFrame(columns=fields_to_extract_channels.keys())
    for channel_id in channel_ids:
        channel_info = youtube.channels().list(part=get_part, id=channel_id).execute()['items'][0]
        channel_data = {}
        for key, value in fields_to_extract_channels.items():
            channel_data[key] = extract_value(channel_info, value)
        channels_info.append(channel_data)
    # Parse data types
    df_channels = df_channels.append(channels_info, ignore_index=True)
    for key, value in data_types_channels.items():
        df_channels[key] = df_channels[key].astype(value)
    return df_channels

# Function to get videos' ids from uploads playlist
def get_video_ids(youtube, uploads_playlist_ids, max_videos_per_channel):
    video_ids = []
    for uploads_playlist_id in uploads_playlist_ids:
        next_page_token = None
        video_ids_channel = []
        while True:
            get_part = ['contentDetails']
            playlist_items = youtube.playlistItems().list(
                part=get_part,
                playlistId=uploads_playlist_id,
                maxResults=max_videos_per_channel,
                pageToken=next_page_token).execute()

            for playlist_item in playlist_items['items']:
                video_ids_channel.append(playlist_item['contentDetails']['videoId'])
            
            if len(video_ids_channel) < max_videos_per_channel and 'nextPageToken' in playlist_items:
                next_page_token = playlist_items['nextPageToken']
            else:
                video_ids_channel = video_ids_channel[:max_videos_per_channel]
                video_ids.extend(video_ids_channel)
                break
    return video_ids

# Function to get videos' information
def get_videos_info(youtube, video_ids, fields_to_extract_videos, data_types_videos):
    get_part = 'id,snippet,contentDetails,statistics'
    videos_info = []
    # Initialize empty dataframe with correct columns
    df_videos = pd.DataFrame(columns=fields_to_extract_videos.keys())
    for video_id in video_ids:
        video_info = youtube.videos().list(part=get_part, id=video_id).execute()['items'][0]
        video_data = {}
        for key, value in fields_to_extract_videos.items():
            video_data[key] = extract_value(video_info, value)
        videos_info.append(video_data)
    # Parse data types
    df_videos = df_videos.append(videos_info, ignore_index=True)
    
    for key, value in data_types_videos.items():
        df_videos[key] = df_videos[key].astype(value)
    
    return df_videos

# Function to get comments' information
def get_comments_info(youtube, video_ids, fields_to_extract_comments, data_types_comments):
    get_part = 'snippet'
    comments_info = []
    # Initialize empty dataframe with correct columns
    df_comments = pd.DataFrame(columns=fields_to_extract_comments.keys())
    for video_id in video_ids:
        next_page_token = None
        while True:
            # Handle videos with disabled comments
            try:
                comment_info = youtube.commentThreads().list(part=get_part, videoId=video_id, pageToken=next_page_token).execute()
            except HttpError as e:
                error_response = json.loads(e.content)
                if error_response['error']['errors'][0]['reason'] == 'commentsDisabled':
                    print("Comments are disabled for this video.")
                    # Handle this situation, such as logging, notifying the user, or skipping this video
                else:
                    # Handle other errors
                    print("An error occurred:", e)
            for comment in comment_info['items']:
                comment_data = {}
                for key, value in fields_to_extract_comments.items():
                    comment_data[key] = extract_value(comment, value)
                comments_info.append(comment_data)
            if 'nextPageToken' in comment_info:
                next_page_token = comment_info['nextPageToken']
            else:
                break
    # Parse data types
    df_comments = df_comments.append(comments_info, ignore_index=True)
    for key, value in data_types_comments.items():
        df_comments[key] = df_comments[key].astype(value)
    return df_comments

# Function to load data from YouTube API
@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    
    youtube = build('youtube', 'v3', developerKey=api_key)

    channel_ids = get_channel_ids(youtube, input_videos)
    print("DONE -> channel_ids")
    
    df_channels = get_channels_info(youtube, channel_ids, fields_to_extract_channels, data_types_channels)
    print("DONE -> df_channels")

    # df_channels.to_excel('raw_df_channels.xlsx')

    uploads_playlist_ids = df_channels['channel_uploads_playlist_id']
    print("DONE -> uploads_playlist_ids")

    video_ids = get_video_ids(youtube, uploads_playlist_ids, max_videos_per_channel)
    print("DONE -> video_ids")

    df_videos = get_videos_info(youtube, video_ids, fields_to_extract_videos, data_types_videos)
    print("DONE -> df_videos")

    # df_videos.to_excel('raw_df_videos.xlsx')

    df_comments = get_comments_info(youtube, video_ids, fields_to_extract_comments, data_types_comments)
    print("DONE -> df_comments")

    # df_comments.to_excel('raw_df_comments.xlsx')

    # TODO cannot pass dfs with dictionary?
    return [df_channels, df_videos, df_comments]

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
