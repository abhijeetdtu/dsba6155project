resource "google_bigquery_dataset" "dataset" {
  dataset_id                  = "nlpdataset"
  friendly_name               = "nlpdataset"
  description                 = "Will store everything that will be needed for the project"
  location                    = "US"
  #default_table_expiration_ms = 3600000
  project = data.google_project.kbs_project.project_id
}
