resource "google_storage_bucket" "data_bucket" {
  name          = "${var.project_id}databucket"
  location      = "US"
  project = data.google_project.kbs_project.project_id

  force_destroy = true
}
