variable "credentials" {
  description = "My Credentials"
  default     = "./keys/my-creds.json"
}

variable "project" {
  description = "Project"
  default     = "youtube-ai-analytics"
}

variable "region" {
  description = "Region"
  default     = "europe-southwest1"
}

variable "location" {
  description = "Project Location"
  default     = "EU"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "youtube-ai-analytics-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "youtube_dataset"
}