# YouTube AI Analytics

## **Automating YouTube Analytics with Custom AI Integrations**, to help creators extracting more value from their audience feedback.

## Current Dashboard

- **Looker Studio:** [YouTube AI Analytics Dashboard](https://lookerstudio.google.com/reporting/424081be-f86f-4a43-bcd9-05d61a3e007a)

![Dashboard Page 1](/assets/looker-studio-1.png)
<!-- ![Dashboard Page 2](/assets/looker-studio-2.png) -->
![Dashboard Page 3](/assets/looker-studio-3.png)
![Dashboard Page 4](/assets/looker-studio-4.png)
![Dashboard Page 5](/assets/looker-studio-5.png)
![Dashboard Page 6](/assets/looker-studio-6.png)

## The Pipeline in a Nutshell
- Provide a list of videos belonging to the YouTube channels you want to analyze and compare. Example:
```python
# YouTube API - list containing videos URLs (1 per channel) to get corresponding channels
input_videos = [
    "https://www.youtube.com/watch?v=kf8zbD6Wadc", # DataTalksClub
    "https://www.youtube.com/watch?v=QMUZ5HfWMRc", # Alex The Analyst
    "https://www.youtube.com/watch?v=VwX2ymxj5rY", # Sundas Khalid
    "https://www.youtube.com/watch?v=nB7Lo9pGzVk", # Seattle Data Guy
    "https://www.youtube.com/watch?v=-MFcNlHMLDY", # Data with Zach
]

    # "https://www.youtube.com/watch?v=m0Rc9YbunNw", # TechWithCosta (the best channel on YouTube, just kidding)
    # "https://www.youtube.com/watch?v=vUKr5O-94z0", # Luke Barousse
    # "https://www.youtube.com/watch?v=Hyhfa7z0jTk", # Ken Jee
    # "https://www.youtube.com/watch?v=RtuzJuaesmo", # Tina Huang
```
- The pipeline gets the target channels automatically
- Through YouTube API, all user-defined data is extracted regarding **channels**, **videos** and **comments**
- With pipeline inputs the user can easily specify the fields to extract and data types. Example:
```python
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
```
- The user can specify a maximum value to cap the number of videos to be extracted per channel, or not
- Raw data is then cleaned, merged and enriched, using Mage and GCP
- A seamless OpenAI API integration enables the user to specify what to extract from the audience comments. Example:
```python
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
```
Output example:
```
**1. Sentiment**
- Positive opinions: Some individuals express their love for the field of data science and find it rewarding.
- Neutral opinions: There is a mixed feeling among commenters regarding the challenges and ambiguity in data science roles.
- Negative opinions: Some express frustration with the unrealistic expectations set by companies and the lack of clarity in the job descriptions and roles.

**2. Keywords**
- Data Science, Job Descriptions, Experience, Skills, Ambiguity

**3. Top Positive**
"I love being a Data Scientist and have never had a better job. To me the job of a Data Scientist is to translate a business problem into a math problem which can be solved with the available data."

**4. Top Negative**
"The biggest problem I’ve had so far is working with my manager. We both have very different perspectives on various problems but he simply doesn’t even want to hear my perspective even when my perspective is usually right."
```
- The most commented videos and most liked comments are being prioritized, and the user can also specify a number to cap the number of videos to be subjected to this AI analysis. Everything is customizable :)

This started as my final project for the **Data Engineering Zoomcamp 2024 (by DataTalksClub)**.

## Introduction
In today's digital landscape, YouTube serves as a powerhouse for content creators to share their videos and engage with audiences worldwide.

However, with the sheer volume of content uploaded daily, extracting meaningful insights from viewer comments and understanding audience sentiment poses a significant challenge.

The project harnesses the power of the **YouTube Data API** and **OpenAI's Language Models (LLMs)** to automate the analysis of user-defined YouTube **channels**, **videos**, and **comments**.

## Problem Statement
Manual analysis of viewer comments on YouTube is time-consuming and labor-intensive, making it difficult for content creators to extract valuable insights about audience sentiment, preferences, and engagement patterns.

**This is not to say that creators should stop reading their audiences' feedback and use AI instead! The goal here is just to enrich the overall analysis results, enabling search and extraction of specific feedback, without reading through thousands of comments, in some cases.**

Additionally, the sheer volume of comments makes it challenging to identify and prioritize critical feedback effectively.

## Solution
This project offers an innovative solution by automating the analysis of viewer comments using OpenAI's Language Models (LLMs) integrated with the YouTube Data API.

By leveraging AI-driven natural language processing, the system automatically extracts insights from user-defined YouTube channels, including sentiment analysis, topic modeling, and audience engagement metrics.

This automation empowers content creators to gain deeper insights into their audience's preferences, sentiment, and engagement patterns, allowing them to tailor their content strategy, optimize engagement tactics, and enhance audience targeting effectively.

By automating the analysis process, the pipeline enables creators to make data-driven decisions efficiently, saving time and resources while maximizing the impact of their content.

## Instructions
- **Operating systems:** Windows 11 + WSL (Ubuntu 22.04)
- **Version control system:** Git + GitHub, create account, setup SSH, clone this repository
- **Git folder:** Go to your projects folder (example "git")
```bash
cd git
```
- **Git clone:** Clone the repository to your machine
```bash
git clone git@github.com:techwithcosta/youtube-ai-analytics.git
```
- **Go into the project folder:**
```bash
cd youtube-ai-analytics
```
- **Some steps here:** [TechWithCosta: Data Engineering Zoomcamp](https://www.youtube.com/playlist?list=PLtU3RENZyLgoe-ptQhZy_mDgdZOMlTLNt)
- **IDE:** VSCode, install it on Windows
- **(Optional) Python:** Miniconda, install it on Ubuntu to run Python environments and isolate packages
- **Start IDE:** Run VSCode from there
```bash
code .
```
- **Cloud:** GCP (setup trial if possible)
- **Setup secrets files:** From the project root folder execute
```bash
chmod +x setup.sh && ./setup.sh
```
- On ```terraform/keys/``` and ```mage/keys/``` update ```my-creds.json``` with GCP service account
- Enable YouTube Data API v3 on GCP to get API key
- Get OpenAI API key from OpenAI account (free or paid)
- On ```mage/``` update ```.env``` with both YouTube API and OpenAI API keys
- ```config.py``` contains all pipeline inputs, adjust if needed
- **Terraform (IaC):** install Terraform on Ubuntu, then adjust ```variables.tf``` from ```terraform/```
```bash
terraform plan
terraform apply
terraform destroy # if needed in the end
```
- **Docker:** install Docker Desktop and set it up with WSL2, make sure it is running
- From ```mage/``` folder:
```bash
docker compose build
docker compose up
```
- **Run orchestrator:** Open browser and Mage http://localhost:6789/
- **Pipeline scheduling:** Ideally running weekly, each Sunday at 4am for example. This is still to be deployed in the cloud, and integrated with CI/CD. In Dev phase yet :)

## Architecture Components
- **Data Layers:** Bronze - Silver - Gold
- **Data Phases:** Raw - Cleaned - Merged - Enriched
- **Cloud Provider:** Google Cloud Platform (GCP)
- **Infrastructure as Code (IaC):** Terraform
- **Containerization:** Docker
- **Orchestrator:** Mage
- **Data Transformations:** Python + SQL
- **Data Lake:** Google Cloud Storage
- **Data Warehouse:** BigQuery
- **Data Visualization:** Looker Studio

![Pipeline Trigger](/assets/pipeline-trigger-1.png)
![Pipeline Scheduling](/assets/pipeline-trigger-2.png)

## Main Repository Files
This repository should have the following structure:
```bash
# generated with the following (ignoring specific folders / files)
tree -I 'charts|custom|extensions|dbt|interactions|utils|assets|__init__.py|README.md'
```
```
.
├── mage
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── keys
│   │   └── my-creds.json
│   ├── requirements.txt
│   └── youtube-ai-analytics
│       ├── config.py
│       ├── data_exporters
│       │   ├── cleaned_data_to_bq.py
│       │   ├── enriched_data_to_bq.sql
│       │   ├── merged_data_to_bq.sql
│       │   └── raw_data_to_gcs.py
│       ├── data_loaders
│       │   ├── raw_data_from_gcs.py
│       │   └── raw_data_from_youtube_api.py
│       ├── io_config.yaml
│       ├── metadata.yaml
│       ├── pipelines
│       │   └── pl_youtube_to_gcp
│       │       └── metadata.yaml
│       ├── requirements.txt
│       └── transformers
│           ├── clean_raw_data.py
│           ├── enrich_cleaned_data.py
│           └── merge_cleaned_data.sql
├── setup.sh
└── terraform
    ├── keys
    │   └── my-creds.json
    ├── main.tf
    └── variables.tf
```

## Improvements
- Deploy Mage to cloud (GCP VM)
- Partitioning and clustering
- Get comment replies (currently getting top level comment only)
- Differentiate between regular video and short (specify on inputs what to get) (currently getting both)
- Enrich data with video categories. Replace integers on df_videos by category string descriptions (youtube.videoCategories())
- Optimize videos API call from single video to batch ids
- Incremental loading
- Environments: Dev, Test, Prod (reflected on Terraform templates)
- Reproducibility: Dockerfile, docker-compose file
- Instead of truncating exceeding tokens, implement chunking and iterative summarization
- Cannot pass dfs with dictionary, between Mage blocks?