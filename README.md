# YouTube AI Analytics
Final project: Data Engineering Zoomcamp 2024 (by DataTalksClub).

Still working on this documentation, thanks for your patience! 😄

# Current Dashboard

![Dashboard Page 1](/assets/looker-studio-1.png)
<!-- ![Dashboard Page 1](/assets/looker-studio-2.png) -->
![Dashboard Page 1](/assets/looker-studio-3.png)
![Dashboard Page 1](/assets/looker-studio-4.png)
![Dashboard Page 1](/assets/looker-studio-5.png)
![Dashboard Page 1](/assets/looker-studio-6.png)

# Instructions

## My Local Dev Setup
- **Operating systems:** Windows 11 + WSL (Ubuntu 22.04)
- **Version control system:** Git + GitHub, create account, setup SSH, clone this repository
- **Git folder:** Go to your projects folder (example "git") ```cd git```
- **Git clone:** ```git clone git@github.com:techwithcosta/youtube-ai-analytics.git```
- **Go into the project folder:** ```cd youtube-ai-analytics```
- **Some steps here:** [TechWithCosta: Data Engineering Zoomcamp](https://www.youtube.com/playlist?list=PLtU3RENZyLgoe-ptQhZy_mDgdZOMlTLNt)
- **IDE:** VSCode, install it on Windows
- **(Optional) Python:** Miniconda, install it on Ubuntu to run Python environments and isolate packages
- **Run VSCode from there:** ```code .```
- **Docker:** install Docker Desktop and set it up with WSL2
- Terraform (IaC)
- Mage (orchestrator) http://localhost:6789/
- GCP (setup trial if possible)
- YouTube API
- OpenAI
- config.py contains pipeline inputs
- rename ```example_my-creds``` into ```my-creds.json``` and update content with GCP service account key (both on ```terraform/keys/``` and ```mage/keys/```)
- rename ```example_env``` into ```.env``` and update content with both YouTube API and OpenAI API keys
- YouTube API must be enabled on GCP
- OpenAI API key is retrieved from an OpenAI account (free or paid)
- Dashboard on Looker Studio [YouTube AI Analytics Dashboard](https://lookerstudio.google.com/reporting/6745d3eb-f9dd-4329-8d92-ecf8bd177e4d)

## Architecture Components
- **Cloud Provider:** Google Cloud Platform (GCP)
- **Infrastructure as Code (IaC):** Terraform
- **Containerization:** Docker
- **Orchestrator:** Mage
- **Data Transformations:** Python + SQL
- **Data Lake:** Google Cloud Storage
- **Data Warehouse:** BigQuery
- **Data Visualization:** Looker Studio

## Notes
- Store inputs in same place (config.py)
- Data phases (raw, clean, enriched) YouTube API
- Channels, videos, comments
- AI analysis OpenAI API

## TODO
- Create .sh file to rename secrets files
- Add trigger to run pipeline weekly
- Partitioning and clustering
- Get comment replies (currently getting top level comment only)
- Differentiate between regular video and short (specify on inputs what to get) (currently getting both)
- Implement categories to replace integers on df_videos by category string descriptions (youtube.videoCategories())
- Optimize videos API call from single video to batch ids
- Incremental loading
- Environments: Dev, Test, Prod (reflected on Terraform templates)
- Reproducibility: Dockerfile, docker-compose file


# README example to improve current

<div>
<img src="https://github.com/mage-ai/assets/blob/main/mascots/mascots-shorter.jpeg?raw=true">
</div>

## Data Engineering Zoomcamp - Week 2

Welcome to DE Zoomcamp with Mage! 

Mage is an open-source, hybrid framework for transforming and integrating data. ✨

In this module, you'll learn how to use the Mage platform to author and share _magical_ data pipelines. This will all be covered in the course, but if you'd like to learn a bit more about Mage, check out our docs [here](https://docs.mage.ai/introduction/overview). 

[Get Started](https://github.com/mage-ai/mage-zoomcamp?tab=readme-ov-file#lets-get-started)
[Assistance](https://github.com/mage-ai/mage-zoomcamp?tab=readme-ov-file#assistance)

## Let's get started

This repo contains a Docker Compose template for getting started with a new Mage project. It requires Docker to be installed locally. If Docker is not installed, please follow the instructions [here](https://docs.docker.com/get-docker/). 

You can start by cloning the repo:

```bash
git clone https://github.com/mage-ai/mage-zoomcamp.git mage-zoomcamp
```

Navigate to the repo:

```bash
cd mage-data-engineering-zoomcamp
```

Rename `dev.env` to simply `.env`— this will _ensure_ the file is not committed to Git by accident, since it _will_ contain credentials in the future.

Now, let's build the container

```bash
docker compose build
```

Finally, start the Docker container:

```bash
docker compose up
```

Now, navigate to http://localhost:6789 in your browser! Voila! You're ready to get started with the course. 

### What just happened?

We just initialized a new mage repository. It will be present in your project under the name `magic-zoomcamp`. If you changed the varable `PROJECT_NAME` in the `.env` file, it will be named whatever you set it to.

This repository should have the following structure:

```
.
├── mage_data
│   └── magic-zoomcamp
├── magic-zoomcamp
│   ├── __pycache__
│   ├── charts
│   ├── custom
│   ├── data_exporters
│   ├── data_loaders
│   ├── dbt
│   ├── extensions
│   ├── interactions
│   ├── pipelines
│   ├── scratchpads
│   ├── transformers
│   ├── utils
│   ├── __init__.py
│   ├── io_config.yaml
│   ├── metadata.yaml
│   └── requirements.txt
├── Dockerfile
├── README.md
├── dev.env
├── docker-compose.yml
└── requirements.txt
```

## Assistance

1. [Mage Docs](https://docs.mage.ai/introduction/overview): a good place to understand Mage functionality or concepts.
2. [Mage Slack](https://www.mage.ai/chat): a good place to ask questions or get help from the Mage team.
3. [DTC Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_2_workflow_orchestration): a good place to get help from the community on course-specific inquireies.
4. [Mage GitHub](https://github.com/mage-ai/mage-ai): a good place to open issues or feature requests.
