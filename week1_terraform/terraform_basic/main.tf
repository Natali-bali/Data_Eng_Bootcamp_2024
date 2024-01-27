terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
# Credentials only needs to be set if you do not have the GOOGLE_APPLICATION_CREDENTIALS set
  credentials = "/home/Natalia/Data_Eng_Bootcamp_2024/keys/my-cred.json"
  project = "ny-taxi-zoomcamp-411215"
  region  = "europe-west1-b"
}



resource "google_storage_bucket" "data-lake-bucket" {
  name          = "ny-taxi-zoomcamp-411215-data-lake"
  location      = "EU"

  # Optional, but recommended settings:
  storage_class = "STANDARD"
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  // days
    }
  }

  force_destroy = true
}


resource "google_bigquery_dataset" "dataset" {
  dataset_id = "ny-taxi"
  project    = "ny-taxi-zoomcamp-411215"
  location   = "EU"
}