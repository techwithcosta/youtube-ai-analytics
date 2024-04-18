WITH comments AS (
  SELECT
  video_id,
  SUM(comment_like_count) AS comment_like_count
FROM `youtube-ai-analytics.youtube_dataset.comments`
GROUP BY
  video_id
)
SELECT
  ch.channel_id,
  ch.channel_title,
  ch.channel_description,
  ch.channel_custom_url,
  ch.channel_published_at,
  ch.channel_thumbnail_url,
  ch.channel_view_count,
  ch.channel_subscriber_count,
  ch.channel_video_count,
  
  vi.video_id,
  vi.video_published_at,
  vi.video_title,
  vi.video_description,
  vi.video_thumbnail_url,
  vi.video_tags,
  vi.video_category_id,
  vi.video_duration,
  vi.video_view_count,
  vi.video_like_count,
  vi.video_comment_count,
  vi.video_url,
  vi.video_duration_seconds,

  IFNULL(comment_like_count, 0) AS comment_like_count
FROM `youtube-ai-analytics.youtube_dataset.channels` ch
LEFT JOIN `youtube-ai-analytics.youtube_dataset.videos` vi
  ON ch.channel_id = vi.channel_id
LEFT JOIN comments co
  ON vi.video_id = co.video_id