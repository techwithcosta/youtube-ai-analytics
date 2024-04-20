if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import time
import pandas as pd
import numpy as np
from openai import OpenAI
import tiktoken

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
number_top_videos = config.number_top_videos
max_token_length = config.max_token_length
openai_model = config.openai_model
system_prompt = config.system_prompt

# OpenAI API to analyse comments from "n" most commented videos
api_key = os.environ.get('OPENAI_API_KEY')
client = OpenAI()

# Function to summarize comments using OpenAI's API
def summarize_comments(comments):
    print(len(comments.split('-- || --')))
    print('# Comments = ' + str(len(comments.split('-- || --'))))
    start_time = time.time()
    # Create OpenAI completion
    completion = client.chat.completions.create(
        model=openai_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": comments}
        ]
    )
    # Get AI's response
    ai_answer = completion.choices[0].message.content
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(elapsed_time)
    return ai_answer

def truncate_to_max_tokens(comments, max_tokens, system_prompt):
    """Truncates a text string to a maximum number of tokens."""
    encoding = tiktoken.get_encoding('cl100k_base')
    encoded_text_count = encoding.encode(comments + system_prompt)
    encoded_text = encoding.encode(comments)
    if len(encoded_text_count) > max_tokens:
        truncated_encoded_text = encoded_text[:max_tokens]
        truncated_string = encoding.decode(truncated_encoded_text)
    else:
        truncated_string = comments
    return truncated_string

def num_tokens_from_string(comments, system_prompt):
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding('cl100k_base')
    num_tokens = len(encoding.encode(comments + system_prompt))
    return num_tokens

@transformer
def transform(df_channels_videos, data, *args, **kwargs):
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
    df_comments = data[2]

    # Get most commented videos for summarization
    top_videos = df_channels_videos.groupby('channel_id').apply(lambda group: group.nlargest(number_top_videos, 'video_comment_count')).reset_index(drop=True)
    top_videos = top_videos[['video_id']]
    top_videos_with_comments = pd.merge(top_videos, df_comments, on='video_id', how='left')
    top_videos_with_comments = top_videos_with_comments[['video_id', 'comment_text', 'comment_like_count']]

    top_videos_with_comments['comment_text'] = top_videos_with_comments['comment_text'].fillna('')

    # Sort by comment_like_count to have most liked comments first
    comments_concatenated = top_videos_with_comments.groupby('video_id').apply(lambda x: '-- || --'.join(x.sort_values(by='comment_like_count', ascending=False)['comment_text'])).reset_index(name='all_comments')

    df_comments_analysis = pd.merge(df_channels_videos, comments_concatenated, on='video_id', how='right')

    # Truncate comments to max tokens supported by LLM
    df_comments_analysis['tokens'] = df_comments_analysis['all_comments'].apply(num_tokens_from_string, system_prompt=system_prompt)
    df_comments_analysis['all_comments'] = df_comments_analysis['all_comments'].apply(truncate_to_max_tokens, max_tokens=max_token_length, system_prompt=system_prompt)

    df_comments_analysis['comments_summary'] = df_comments_analysis['all_comments'].apply(summarize_comments)

    # df_comments_analysis.to_excel('df_comments_analysis.xlsx')

    return df_comments_analysis


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
