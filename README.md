# YouTube AI Analytics
Final project: Data Engineering Zoomcamp 2024 (by DataTalksClub).

Still working on this documentation, thanks for your patience! 😄

## Problem Statement
- Data phases (raw, clean, enriched) YouTube API
- Channels, videos, comments
- AI analysis OpenAI API

## Current Dashboard

![Dashboard Page 1](/assets/looker-studio-1.png)
<!-- ![Dashboard Page 2](/assets/looker-studio-2.png) -->
![Dashboard Page 3](/assets/looker-studio-3.png)
![Dashboard Page 4](/assets/looker-studio-4.png)
![Dashboard Page 5](/assets/looker-studio-5.png)
![Dashboard Page 6](/assets/looker-studio-6.png)

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
- **Pipeline scheduling:** Running weekly, each Sunday at 4am
- **Current Dashboard on Looker Studio:** [YouTube AI Analytics Dashboard](https://lookerstudio.google.com/reporting/6745d3eb-f9dd-4329-8d92-ecf8bd177e4d)

## Architecture Components
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