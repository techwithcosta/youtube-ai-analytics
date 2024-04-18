# YouTube API - list containing videos URLs (1 per channel) to get corresponding channels
input_videos = [
    "https://www.youtube.com/watch?v=kf8zbD6Wadc", # DataTalksClub
    "https://www.youtube.com/watch?v=QMUZ5HfWMRc", # Alex The Analyst
    "https://www.youtube.com/watch?v=VwX2ymxj5rY", # Sundas Khalid
    "https://www.youtube.com/watch?v=nB7Lo9pGzVk", # Seattle Data Guy
    "https://www.youtube.com/watch?v=-MFcNlHMLDY", # Data with Zach
]

    # "https://www.youtube.com/watch?v=m0Rc9YbunNw", # TechWithCosta
    # "https://www.youtube.com/watch?v=kf8zbD6Wadc", # DataTalksClub
    # "https://www.youtube.com/watch?v=QMUZ5HfWMRc", # Alex The Analyst
    # "https://www.youtube.com/watch?v=-MFcNlHMLDY", # Data with Zach
    # "https://www.youtube.com/watch?v=vUKr5O-94z0", # Luke Barousse
    # "https://www.youtube.com/watch?v=Hyhfa7z0jTk", # Ken Jee
    # "https://www.youtube.com/watch?v=nB7Lo9pGzVk", # Seattle Data Guy
    # "https://www.youtube.com/watch?v=RtuzJuaesmo", # Tina Huang
    # "https://www.youtube.com/watch?v=VwX2ymxj5rY", # Sundas Khalid

# YouTube API - maximum number of videos to extract from each channel
max_videos_per_channel = 100

# YouTube API - fields to extract - CHANNELS
fields_to_extract_channels = {
    "channel_id": "id", # unique identifier
    "channel_title": "snippet.title",
    "channel_description": "snippet.description",
    "channel_custom_url": "snippet.customUrl",
    "channel_published_at": "snippet.publishedAt",
    "channel_thumbnail_url" : "snippet.thumbnails.high.url",
    "channel_uploads_playlist_id": "contentDetails.relatedPlaylists.uploads",
    "channel_view_count": "statistics.viewCount",
    "channel_subscriber_count": "statistics.subscriberCount",
    "channel_video_count": "statistics.videoCount"
}

# YouTube API - data types - CHANNELS
data_types_channels = {
    "channel_id": "str",
    "channel_title": "str",
    "channel_description": "str",
    "channel_custom_url": "str",
    "channel_published_at": "datetime64[ns]",
    "channel_thumbnail_url": "str",
    "channel_uploads_playlist_id": "str",
    "channel_view_count": "Int64",
    "channel_subscriber_count": "Int64",
    "channel_video_count": "Int64"
}

# YouTube API - fields to extract - VIDEOS
fields_to_extract_videos = {
    "video_id": "id", # unique identifier
    "channel_id": "snippet.channelId", # foreign key from channels
    "video_published_at": "snippet.publishedAt",
    "video_title": "snippet.title",
    "video_description": "snippet.description",
    "video_thumbnail_url" : "snippet.thumbnails.standard.url",
    "video_tags": "snippet.tags",
    "video_category_id": "snippet.categoryId",
    "video_duration": "contentDetails.duration",
    "video_view_count": "statistics.viewCount",
    "video_like_count": "statistics.likeCount",
    "video_comment_count": "statistics.commentCount"
}

# YouTube API - data types - VIDEOS
data_types_videos = {
    "video_id": "str",
    "channel_id": "str",
    "video_published_at": "datetime64[ns]",
    "video_title": "str",
    "video_description": "str",
    "video_thumbnail_url": "str",
    "video_tags": "str",
    "video_category_id": "Int64",
    "video_duration": "str",
    "video_view_count": "Int64",
    "video_like_count": "Int64",
    "video_comment_count": "Int64"
}

# YouTube API - fields to extract - COMMENTS
fields_to_extract_comments = {
    "comment_id": "snippet.topLevelComment.id", # unique identifier
    "video_id": "snippet.videoId", # foreign key from videos
    "comment_text": "snippet.topLevelComment.snippet.textOriginal",
    "comment_like_count": "snippet.topLevelComment.snippet.likeCount",
    "comment_published_at": "snippet.topLevelComment.snippet.publishedAt"
}

# YouTube API - data types - COMMENTS
data_types_comments = {
    "comment_id": "str",
    "video_id": "str",
    "comment_text": "str",
    "comment_like_count": "Int64",
    "comment_published_at": "datetime64[ns]"
}

# OpenAI API - comments analysis with LLMs
number_top_videos = 3

# Maximum token length for truncation
max_token_length = 16000

# OpenAI LLM model
openai_model = "gpt-3.5-turbo-0125"

# System prompt to instruct the model
system_prompt = """Your goal is to extract insights from a list of YouTube video comments, where each one is separated by "-- || --".
Your answer must be divided into the following categories:
"**1. Sentiment**" (3 short bullets summarizing positive, neutral, negative opinions)
"**2. Keywords**" (1 short bullet with top 5 most relevant single keywords about the topics mentioned, comma-separated)
"**3. Top Positive**" (the most positive comment)
"**4. Top Negative**" (the most negative comment)
Keep it very short and concise.
If comments are not in English, translate.
"""